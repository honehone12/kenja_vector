import os
from pymongo import AsyncMongoClient

__client = None

def connect() -> AsyncMongoClient:
    uri = os.getenv('MONGO_URI')
    if uri is None:
        raise ValueError('env for mongo uri not set')
    
    __client = AsyncMongoClient(uri)
    return __client

def db(key: str):
    if __client is None:
        raise ValueError('client is not initialized')

    db_name = os.getenv(key)
    if db_name is None:
        raise ValueError(f'env for {key} not set')
    
    return __client[db_name] 

def colle(db, key: str):
    colle_name = os.getenv(key)
    if colle_name is None:
        raise ValueError(f'env for {key} is not set')
    
    return db[colle_name]
