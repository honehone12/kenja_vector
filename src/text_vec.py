import asyncio
from dotenv import load_dotenv
import lib.jsonio as jsonio
from lib.logger import log, loginit
import lib.mongo as mongo
from lib.documents import Img, Done

async def text_vec():
    mongo.connect()
    db = mongo.db('DB')
    source_colle = mongo.colle(db, 'SOURCE_CL')
    dist_colle = mongo.colle(db, 'DIST_CL')

    img_dict = jsonio.parse('IMG_LIST')
    img_list = [Img(**img) for img in img_dict]
    done_dict = jsonio.parse('DONE_LIST')
    done_list = [Done(**done) for done in done_dict]

if __name__ == '__main__':
    loginit(__name__)
    load_dotenv()
    
    try:
        asyncio.run(text_vec())
    except Exception as e:
        log().error(e)
