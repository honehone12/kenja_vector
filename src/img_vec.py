import os
import asyncio
import urllib
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

async def img_vec(iteration: int, batch_size: int, img_root: str):
    db = mongo.db('DATABASE')
    colle: Collection[Doc] = mongo.colle(db, 'COLLECTION')

    stream: Cursor[Doc] = colle.find({})
    it = 0
    total = 0
    async for doc in stream:
        if doc.get('img_vector') is not None:
            total += 1
            continue
        
        url = urllib.parse.urlparse(doc['img'])
        path = url.path
        path.removesuffix
        path = img_root + path
        
        if not os.path.exists(path):
            total += 1
            continue

        it += 1
        total += 1
        if it > iteration:
            log().info('quit on max iteration')
            break

        
        log().info(f'iteration {it} ({total})')
        
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

        img_root = os.getenv('IMG_ROOT')
        if img_root is None:
            raise ValueError('env for IMG_ROOT is not set')

        mongo.connect()
        asyncio.run(img_vec(iteration, batch_size, img_root))
    except Exception as e:
        log().error(e)