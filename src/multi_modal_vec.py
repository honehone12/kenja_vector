import asyncio
import os
from urllib.parse import urlparse
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import DeleteOne, UpdateOne
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from lib import mongo
from lib.documents import IMG_VEC_FIELD, TXT_VEC_FIELD, STF_VEC_FIELD, Doc
from lib.colpali import init_multi_modal_model, img_vector, txt_vector

def img(img_root: str, url: str, id: ObjectId):
    if len(url) == 0:
        raise ValueError('empty url')

    path = img_root + urlparse(url).path.removesuffix('/')
    if not os.path.exists(path):
        print(f'image not found {path}')
        d = DeleteOne(
            filter={'_id': id}
        )
        return d, False

    v = img_vector(path)
    b = mongo.compress_bin(v)
    u = UpdateOne(
        filter={'_id': id},
        update={
            '$set': {IMG_VEC_FIELD: b},
            '$unset': {'img': ''}
        }
    )
    return u, True

def txt(field: str, text: str, id: ObjectId):
    if len(text) == 0:
        raise ValueError('empty text')

    v = txt_vector(text)
    b = mongo.compress_bin(v)
    u = UpdateOne(
        filter={'_id': id},
        update={'$set': {field: b}}
    )
    return u
    

async def multi_modal_vec(iteration: int, batch_size: int, img_root: str):
    db = mongo.db('DATABASE')
    cl: AsyncCollection[Doc] = mongo.collection(db, 'COLLECTION')
    stream: AsyncCursor[Doc] = cl.find({})

    it = 0
    batch = []
    async for doc in stream:
        id = doc['_id']

        if doc.get(IMG_VEC_FIELD) is None:
            op, ok = img(img_root, doc['img'], id)
            batch.append(op)
            if not ok:
                continue
            
        if doc.get(TXT_VEC_FIELD) is None:
            op = txt(TXT_VEC_FIELD, doc['description'], id)
            batch.append(op)

        if doc.get(STF_VEC_FIELD) is None:
            op = txt(STF_VEC_FIELD, doc['staff'], id)
            batch.append(op)

        if len(batch) >= batch_size:
            res = await cl.bulk_write(batch)
            print(f'{res.modified_count} updated')
            batch.clear()

        it += 1
        print(f'iteration {it} done')
        if it >= iteration:
            print('iteration limit')
            break

    if len(batch) > 0:
        res = await cl.bulk_write(batch)
        print(f'{res.modified_count} updated')
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
        batch_size = 100
        if batchenv is not None:
            batch_size = int(batchenv)

        img_root = os.getenv('IMG_ROOT')
        if img_root is None:
            raise ValueError('env for image root is not set')

        init_multi_modal_model()
        mongo.connect()
        asyncio.run(multi_modal_vec(iteration, batch_size, img_root))
    except Exception as e:
        print(e)