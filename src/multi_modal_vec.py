import asyncio
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from lib import mongo
from lib.documents import IMG_VEC_FIELD, TXT_VEC_FIELD, STF_VEC_FIELD, Doc
from lib.logger import init_logger, log
from lib.multi_modal_embed import img_vector, txt_vector, init_multi_modal_model

async def img(img_root: str, url: str):
    if len(url) == 0:
        raise ValueError('null url')

    path = img_root + urlparse(url).path.removesuffix('/')
    if not os.path.exists(path):
        log().warning(f'image not found {path}')
        return

    v = img_vector(path)
    log().info(v.shape)

async def txt(text: str):
    if len(text) == 0:
        raise ValueError('null text')

    v = txt_vector(text)
    log().info(v.shape)


async def multi_modal_vec(iteration: int, batch_size: int, img_root: str):
    l = log()
    db = mongo.db('DATABASE')
    cl: AsyncCollection[Doc] = mongo.collection(db, 'COLLECTION')
    stream: AsyncCursor[Doc] = cl.find({})

    it = 0
    total = 0
    batch = []
    async for doc in stream:
        if doc.get(IMG_VEC_FIELD) is None:
            await img(img_root, doc['img'])

        # if doc.get(TXT_VEC_FIELD) is None:
        #     txt(doc['description'])

        # if doc.get(STF_VEC_FIELD) is None:
        #     txt(doc['staff'])
    
        it += 1
        if it >= iteration:
            l.info('iteration limit')
            break

    l.info('done')

if __name__ == '__main__':
    init_logger(__name__)

    try:
        if not load_dotenv():
            raise RuntimeError('failed to initialize dotenv')

        itenv = os.getenv('ITERATION')
        iteration = 100
        if itenv is not None:
            iteration = int(itenv)

        batchenv = os.getenv('BATCH_SIZE')
        batch_size = 200
        if batchenv is not None:
            batch_size = int(batchenv)

        img_root = os.getenv('IMG_ROOT')
        if img_root is None:
            raise ValueError('env for image root is not set')

        init_multi_modal_model()
        mongo.connect()
        asyncio.run(multi_modal_vec(iteration, batch_size, img_root))
    except Exception as e:
        log().error(e)