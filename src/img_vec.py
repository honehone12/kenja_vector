import asyncio
from dotenv import load_dotenv
from lib.jsonio import parse
from lib.logger import log, loginit
import lib.mongo as mongo

async def img_vec():
    mongo.connect()
    db = mongo.db('DB')
    source_colle = mongo.colle(db, 'SOURCE_CL')
    dist_colle = mongo.colle(db, 'DIST_CL')

    img_list = parse('IMG_LIST')
    done_list = parse('DONE_LIST')    

if __name__ == '__main__':
    loginit(__name__)
    load_dotenv()
    
    try:
        asyncio.run(img_vec())
    except Exception as e:
        log().error(e)
