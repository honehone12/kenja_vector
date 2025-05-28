import os
import asyncio
from dotenv import load_dotenv
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from bson.binary import BinaryVectorDtype
import lib.jsonio as jsonio
from lib.logger import log, init_logger
from lib.documents import Doc, Img, Done
from lib.logger import log
import lib.mongo as mongo
from lib.mongo import compress_bin
from lib.txt_embed import init_model, txt_vector

async def txt_vec():
    db = mongo.db('DATABASE')
    colle: Collection[Doc] = mongo.colle(db, 'COLLECTION')

    done_list = [Done(**done) for done in jsonio.parse('DONE_LIST')]

    stream: Cursor[Doc] = colle.find({})
    it = 0
    async for doc in stream:
        done_found = [d for d in done_list if d.item_id == doc.item_id]
        l = len(done_found)
        if l > 1:
            raise AssertionError(f'{l} same item id found in done list')
        elif l == 1:
            continue

        it += 1
        log().info(f'iterating {it}')

        desc = doc['description']
        v = txt_vector(desc)
        compressed = compress_bin(v, BinaryVectorDtype.FLOAT32)
        

if __name__ == '__main__':
    try:
        init_logger(__name__)
        load_dotenv()
        mongo.connect()
        init_model()
        asyncio.run(txt_vec())
    except Exception as e:
        log().error(e)
