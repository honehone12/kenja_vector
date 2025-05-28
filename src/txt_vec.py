import os
import asyncio
from dotenv import load_dotenv
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

async def txt_vec(iteration: int):
    db = mongo.db('DATABASE')
    colle: Collection[Doc] = mongo.colle(db, 'COLLECTION')

    stream: Cursor[Doc] = colle.find({})
    it = 0
    async for doc in stream:
        if doc.get('text_vector') is not None:
            continue

        it += 1
        if it > iteration:
            log().info('quit on max iteration')
            break
        log().info(f'iterating {it}')

        desc = doc['description']
        v = txt_vector(desc)
        compressed = compress_bin(v)

        res = await colle.update_one(
            {'_id': doc['_id']}, 
            {'$set': {'text_vector': compressed}}
        )
        if res.modified_count != 1:
            raise AssertionError(f'failed to update {doc['_id']}')
            
    log().info('done')

if __name__ == '__main__':
    init_logger(__name__)
    load_dotenv()

    try:
        itstr = os.getenv('ITERATION')
        iteration = 0
        if itstr is None:
            iteration = 100
        else:
            iteration = int(itstr)

        mongo.connect()
        init_txt_model()
        asyncio.run(txt_vec(iteration))
    except Exception as e:
        log().error(e)
