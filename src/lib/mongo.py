import os
from pymongo import AsyncMongoClient

def connect() -> AsyncMongoClient:
    uri = os.getenv('MONGO_URI')
    if uri is None:
        raise ValueError('env for mongo uri not set')
    
    client = AsyncMongoClient(uri)
    return client
