from typing import TypedDict
from bson import ObjectId

RATING_ALL_AGES = 1
RATING_HENTAI = 2

class Doc(TypedDict):
    _id: ObjectId
    rating: int
    img: str
    description: str
