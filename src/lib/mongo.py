import os
from pymongo import AsyncMongoClient
from pymongo.database import Database
from pymongo.collection import Collection

__client = None

def connect():
    global __client

    uri = os.getenv('MONGO_URI')
    if uri is None:
        raise ValueError('env for MONGO_URI not set')
    __client = AsyncMongoClient(uri)

def db(key: str) -> Database:
    if __client is None:
        raise ValueError('client is not initialized')

    db = os.getenv('DATABASE')
    if db is None:
        raise ValueError(f'env for {key} not set')
    return __client[db]

def colle(db: Database, key: str) -> Collection:
    collection = os.getenv(key)
    if collection is None:
        raise ValueError(f'env for {key} is not set')
    return db[collection]
