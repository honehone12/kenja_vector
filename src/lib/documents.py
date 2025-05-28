from typing import TypedDict
from bson import ObjectId

ITEM_T_ANIME = 1
ITEM_T_CHARACTER = 2

class ItemId(TypedDict):
    id: int
    item_type: int

    def __eq__(self, other) -> bool:
        if isinstance(other, ItemId):
            return self.item_type == other.item_type and self.id == other.id
        elif isinstance(other, dict):
            return self.item_type == other['item_type'] and self.id == other['id']
        else:
            raise ValueError('unexpected instance type')

class Img(TypedDict):
    _id: ObjectId
    item_id: ItemId
    img: str

class Doc(TypedDict):
    _id: ObjectId
    item_id: ItemId
    description: str
