from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
# acceptable true values for a bool parameter are: 'true', 'True', '1', 'on', 'yes', 'y', 't'
async def read_item(item_id: str, q: str | None = None, short: bool = False): 
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/models/{model_name}") # model_name would be a ModelName member
async def get_item_type(model_name: ModelName):
    if model_name == ModelName.alexnet: # comparing with the member directly
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet": # comparing with the value
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}") # file_path would be a path parameter, needed to declare it as a path parameter
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10): # 'skip' and 'limit' are query parameters
#     return fake_items_db[skip : skip + limit]

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}



# Additional validation
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



# ESTE ES UN NUEVO COMENTARIO