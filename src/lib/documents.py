from typing import TypedDict
from pydantic import BaseModel
from bson import ObjectId

ITEM_T_ANIME = 1
ITEM_T_CHARACTER = 2

class ItemId(BaseModel):
    id: int
    item_type: int

    def __eq__(self, other) -> bool:
        if isinstance(other, ItemId):
            return self.item_type == other.item_type and self.id == other.id
        else:
            raise ValueError('unexpected instance type')

class Done(BaseModel):
    item_id: ItemId

class Img(BaseModel):
    item_id: ItemId
    path: str

class Doc(TypedDict):
    _id: ObjectId
    item_id: ItemId
    description: str
    