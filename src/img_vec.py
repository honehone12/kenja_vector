import asyncio
import json
import os
from dotenv import load_dotenv
from lib.logger import log, init_logger
import lib.mongo as mongo

async def main():
    img_list_file = os.getenv("IMG_LIST")
    if img_list_file is None:
        raise ValueError('env for img list is not set')

    done_list_file = os.getenv('DONE_LIST')
    if done_list_file is None:
        raise ValueError('env for done list is not set')    

    img_list = None
    if os.path.exists(img_list_file):
        with open(img_list_file, 'r') as file:
            img_list = json.load(file)

    done_list = None
    if os.path.exists(done_list_file):
        with open(done_list_file, 'r') as file:
            done_list = json.load(file)
    else:
        done_list = []

    mongo_client = mongo.connect()

if __name__ == '__main__':
    init_logger(__name__)
    load_dotenv()
    try:
        asyncio.run(main())
    except Exception as e:
        log().error(e)
