import os
import asyncio
import urllib
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

async def img_vec(iteration: int, img_root: str):
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
        
        url = urllib.parse.urlparse(doc['img'])
        path = url.path
        path.removesuffix
        path = img_root + path
        
        if not os.path.exists(path):
            continue

        it += 1
        if it > iteration:
            break
        log().info(f'iterating {it}')
        
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

        img_root = os.getenv('IMG_ROOT')
        if img_root is None:
            raise ValueError('env for IMG_ROOT is not set')

        mongo.connect()
        asyncio.run(img_vec(iteration, img_root))
    except Exception as e:
        log().error(e)