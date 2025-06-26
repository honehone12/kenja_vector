import asyncio
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from lib import mongo
from lib.documents import IMG_VEC_FIELD, TXT_VEC_FIELD, STF_VEC_FIELD, Doc
from lib.clip import init_clip_model, image_vector
from lib.sentence_tsfm import init_sentence_tsfm_model, sentence_vector

def process_image(img_root: str, url: str):
    if len(url) == 0:
        raise ValueError('empty url')

    path = img_root + urlparse(url).path.removesuffix('/')
    if not os.path.exists(path):
        print(f'image not found {path}')
        return

    v = image_vector(path)
    print('image', v.shape)

def process_text(text: str):
    if len(text) == 0:
        raise ValueError('empty text')

    v = sentence_vector(text)
    print('text', v.shape)

def process_name(text: str):
    if len(text) == 0:
        raise ValueError('empty text')

    v = sentence_vector(text)
    print('name', v.shape)    
    

async def process_vecs(iteration: int, img_root: str):
    db = mongo.db('DATABASE')
    cl: AsyncCollection[Doc] = mongo.collection(db, 'COLLECTION')
    stream: AsyncCursor[Doc] = cl.find({})

    it = 0
    async for doc in stream:
        if doc.get(IMG_VEC_FIELD) is None:
            process_image(img_root, doc['img'])
            
        if doc.get(TXT_VEC_FIELD) is None:
            process_text(doc['description'])

        if doc.get(STF_VEC_FIELD) is None:
            process_text(doc['staff'])

        it += 1
        print(f'iteration {it} done')
        if it >= iteration:
            print('iteration limit')
            break

    print('done')

if __name__ == '__main__':
    try:
        if not load_dotenv():
            raise RuntimeError('failed to initialize dotenv')

        itenv = os.getenv('ITERATION')
        iteration = 100
        if itenv is not None:
            iteration = int(itenv)

        batchenv = os.getenv('BATCH_SIZE')
        if batchenv is not None:
            batch_size = int(batchenv)

        img_root = os.getenv('IMG_ROOT')
        if img_root is None:
            raise ValueError('env for image root is not set')

        init_clip_model()
        init_sentence_tsfm_model()
        mongo.connect()
        asyncio.run(process_vecs(iteration, img_root))
    except Exception as e:
        print(e)
