import os
import asyncio
from dotenv import load_dotenv
from pymongo import UpdateOne
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from lib.logger import log, init_logger
from lib.documents import TXT_VEC_FIELD, Doc
import lib.mongo as mongo
from lib.mongo import compress_bin
from lib.txt_embed import init_txt_model, txt_vector

async def txt_vec(iteration: int, batch_size: int):
    db = mongo.db('DATABASE')
    colle: AsyncCollection[Doc] = mongo.collection(db, 'COLLECTION')

    stream: AsyncCursor[Doc] = colle.find({})
    it = 0
    total = 0
    batch = []
    async for doc in stream:
        if doc.get(TXT_VEC_FIELD) is not None:
            total += 1
            continue

        it += 1
        total += 1
        if it > iteration:
            log().info('quit on max iteration')
            break
        log().info(f'iteration {it} ({total})')

        desc = doc['description']
        if len(desc) == 0:
            raise ValueError(f'null text: {doc}')
        
        v = txt_vector(desc)
        compressed = compress_bin(v)

        u = UpdateOne(
            filter={'_id': doc['_id']},
            update={'$set': {TXT_VEC_FIELD: compressed}}
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
        
        mongo.connect()
        init_txt_model()
        asyncio.run(txt_vec(iteration, batch_size))
    except Exception as e:
        log().error(e)
