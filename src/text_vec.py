import os
import asyncio
from dotenv import load_dotenv
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
import lib.jsonio as jsonio
from lib.logger import log, loginit
from lib.documents import Doc, Img, Done
from lib.logger import log
import lib.mongo as mongo

async def text_vec():
    mongo.connect()
    db = mongo.db('DATABASE')
    colle: Collection[Doc] = mongo.colle(db, 'COLLECTION')

    img_raw = jsonio.parse('IMG_LIST')
    img_list = [Img(**img) for img in img_raw]
    done_raw = jsonio.parse('DONE_LIST')
    done_list = [Done(**done) for done in done_raw]

    stream: Cursor[Doc] = colle.find({})
    async for document in stream:
        log().info(document)

if __name__ == '__main__':
    loginit(__name__)
    load_dotenv()
    
    try:
        asyncio.run(text_vec())
    except Exception as e:
        log().error(e)
