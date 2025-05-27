import asyncio
from dotenv import load_dotenv
from lib.jsonio import parse_from_env
from lib.logger import log, init_logger
import lib.mongo as mongo

async def text_vec():
    mongo.connect()
    db = mongo.db_from_env('DB')
    source_colle = mongo.colle_from_env(db, 'SOURCE_CL')
    dist_colle = mongo.colle_from_env(db, 'DIST_CL')

    img_list = parse_from_env('IMG_LIST')
    done_list = parse_from_env('DONE_LIST')    



if __name__ == '__main__':
    init_logger(__name__)
    load_dotenv()
    
    try:
        asyncio.run(text_vec())
    except Exception as e:
        log().error(e)
