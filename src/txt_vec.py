import os
import asyncio
from dotenv import load_dotenv
from pymongo import UpdateOne
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from bson.binary import BinaryVectorDtype
from lib.logger import log, init_logger
from lib.documents import Doc, Img, Done
from lib.logger import log
import lib.mongo as mongo
from lib.mongo import compress_bin
from lib.txt_embed import init_txt_model, txt_vector

async def txt_vec(iteration: int, batch_size: int):
    db = mongo.db('DATABASE')
    colle: Collection[Doc] = mongo.colle(db, 'COLLECTION')

    stream: Cursor[Doc] = colle.find({})
    it = 0
    total = 0
    batch = []
    async for doc in stream:
        if doc.get('text_vector') is not None:
            total += 1
            continue

        it += 1
        total += 1
        if it > iteration:
            log().info('quit on max iteration')
            break

        desc = doc['description']
        v = txt_vector(desc)
        compressed = compress_bin(v)

        u = UpdateOne(
            filter={'_id': doc['_id']},
            update={'$set': {'text_vector': compressed}}
        )
        batch.append(u)
        if len(batch) >= batch_size:
            res = await colle.bulk_write(batch)
            log().info(f'{res.modified_count} updated')
            batch.clear()
        
        log().info(f'iteration {it} ({total})')
    
    if len(batch) > 0:
        res = await colle.bulk_write(batch)
        log().info(f'{res.modified_count} updated')
    log().info('done')

if __name__ == '__main__':
    init_logger(__name__)
    load_dotenv()

    try:
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
