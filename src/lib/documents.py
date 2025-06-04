from typing import TypedDict #, override
from bson import ObjectId

ITEM_T_ANIME = 1
ITEM_T_CHARACTER = 2

class ItemId(TypedDict):
    id: int
    item_type: int

    # @override
    # def __eq__(self, other) -> bool:
    #     if isinstance(other, ItemId):
    #         return self.item_type == other.item_type and self.id == other.id
    #     elif isinstance(other, dict):
    #         return self.item_type == other['item_type'] and self.id == other['id']
    #     else:
    #         raise ValueError('unexpected instance type')

class Doc(TypedDict):
    _id: ObjectId
    img: str
    description: str
