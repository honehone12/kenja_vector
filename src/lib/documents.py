from typing import TypedDict
from bson import ObjectId

class Doc(TypedDict):
    _id: ObjectId
    img: str
    description: str
