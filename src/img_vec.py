import os
import asyncio
from urllib.parse import urlparse
from dotenv import load_dotenv
from pymongo import DeleteOne, UpdateOne
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from lib.logger import log, init_logger
from lib.documents import RATING_ALL_AGES, RATING_HENTAI, IMG_VEC_FIELD, Doc
import lib.mongo as mongo
from lib.mongo import compress_bin
from lib.image_tsfm import init_image_tsfm_model, image_vector

async def img_vec(iteration: int, batch_size: int, img_root: str):
    db = mongo.db('DATABASE')
    colle: AsyncCollection[Doc] = mongo.collection(db, 'COLLECTION')

    stream: AsyncCursor[Doc] = colle.find({})
    it = 0
    total = 0
    batch = []
    async for doc in stream:
        if doc.get(IMG_VEC_FIELD) is not None:
            total += 1
            continue
        
        url = urlparse(doc['img'])
        if len(url) == 0:
            raise ValueError(f'null image: {doc}')

        rating = doc['rating']
        path = url.path
        path = path.removesuffix('/')
        if rating == RATING_ALL_AGES:
            path = img_root + path
        elif rating == RATING_HENTAI:
            path = img_root + '/H' + path
        else: 
            raise ValueError('unexpected rating')

        if not os.path.exists(path):
            log().warning(f'img not found {path}')
            total += 1
            d = DeleteOne(
                filter={'_id': doc['_id']}
            )
            batch.append(d)
            continue

        it += 1
        total += 1
        if it > iteration:
            log().info('quit on max iteration')
            break
        log().info(f'iteration {it} ({total})')
        v = image_vector(path)
        compressed = compress_bin(v)
        
        u = UpdateOne(
            filter={'_id': doc['_id']},
            update={
                '$set': {IMG_VEC_FIELD: compressed},
                '$unset': {'img': ''}
            }
        )
        batch.append(u)
        
        if len(batch) >= batch_size:
            res = await colle.bulk_write(batch)
            log().info(f'{res.modified_count} updated')
            batch.clear()
    
    if len(batch) > 0:
        res = await colle.bulk_write(batch)
        log().info(f'{res.modified_count} updated')
    log().info('done')

if __name__ == '__main__':
    init_logger(__name__)
    
    try:
        if not load_dotenv():
            raise RuntimeError('failed to initialize dotenv')

        itstr = os.getenv('ITERATION')
        iteration = 100
        if itstr is not None:
            iteration = int(itstr)

        batchstr = os.getenv('BATCH_SIZE')
        batch_size = 100
        if batchstr is not None:
            batch_size = int(batchstr)

        img_root = os.getenv('IMG_ROOT')
        if img_root is None:
            raise ValueError('env for image root is not set')

        init_image_tsfm_model()
        mongo.connect()
        asyncio.run(img_vec(iteration, batch_size, img_root))
    except Exception as e:
        log().error(e)