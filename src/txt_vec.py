import os
import asyncio
from dotenv import load_dotenv
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
import lib.jsonio as jsonio
from lib.logger import log, init_logger
from lib.documents import Doc, Img, Done
from lib.logger import log
import lib.mongo as mongo
from lib.mongo import compress_bin
from lib.txt_embed import init_model, vector
from bson.binary import BinaryVectorDtype

async def text_vec():
    db = mongo.db('DATABASE')
    colle: Collection[Doc] = mongo.colle(db, 'COLLECTION')

    img_list = [Img(**img) for img in jsonio.parse('IMG_LIST')]
    done_list = [Done(**done) for done in jsonio.parse('DONE_LIST')]

    stream: Cursor[Doc] = colle.find({})
    async for doc in stream:
        done_found = [d for d in done_list if d.item_id == doc.item_id]
        l = len(done_found)
        if l > 1:
            raise AssertionError(f'{l} same item id found in done list')
        elif l == 1:
            continue
        
        # img_found = [i for i in img_list if i.item_id == doc.item_id]
        # l = len(img_found)
        # if l > 1:
        #     raise AssertionError(f'{l} same item id found in img list')
        # elif l == 0:
        #     res = await colle.delete_one({_id: doc._id})
        #     log().warn(f'deleted {res.deleted_count} item without img')

        desc = doc['description']
        v = vector(desc)
        compressed = compress_bin(v, BinaryVectorDtype.FLOAT32)
        

if __name__ == '__main__':
    try:
        init_logger(__name__)
        load_dotenv()
        mongo.connect()
        init_model()
        asyncio.run(text_vec())
    except Exception as e:
        log().error(e)
