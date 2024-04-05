from fastapi import FastAPI
from typing import *
from enum import Enum

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,
    item_id: str,
    q: Union[str, None],
    short: bool = False):
    
    item = {"item_id": item_id, "owner_id": user_id}

    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item."}
        )

    return item

# Pydantic 모델 사용 - 데이터검증 라이브러리
from datetime import datetime
from typing import *
from fastapi import FastAPI

from pydantic import BaseModel

# API docs 상에 설명해주는 역할.
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}

    if q:
        result.update({"q": q})
    
    return result

@app.post("/items/")
async def create_item(item: Item):
    return item