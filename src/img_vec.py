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

async def img_vec():
    db = mongo.db('DATABASE')
    colle: Collection[Doc] = mongo.colle(db, 'COLLECTION')

    img_list = [Img(**img) for img in jsonio.parse('IMG_LIST')]
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
        
        img_found = [i for i in img_list if i.item_id == doc.item_id]
        l = len(img_found)
        if l > 1:
            raise AssertionError(f'{l} same item id found in img list')
        elif l == 0:
            log().warn(f'could not find img for {doc.item_id.item_type}:{doc.item_id.id}')
            continue

        it += 1
        log().info(f'iterating {it}')
        
    log().info('done')

if __name__ == '__main__':
    try:
        init_logger(__name__)
        load_dotenv()
        mongo.connect()
        asyncio.run(img_vec())
    except Exception as e:
        log().error(e)