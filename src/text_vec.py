import asyncio
from dotenv import load_dotenv

from lib.logger import init_logger
import lib.mongo as mongo

async def main():
    log = init_logger(__name__)
    load_dotenv()

    try:
        log.info('hello')
        mongo_client = mongo.connect()

    except Exception as e:
        log.error(e)

if __name__ == '__main__':
    asyncio.run(main())
