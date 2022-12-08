from typing import Union
from fastapi import FastAPI

from EXAMPLE_DB_FASTAPI import *
from analyticsdb import *

app = FastAPI()

# make a route that adds a song
@app.get("/add/{item_id}")
def add_item(item_id: int, q: str = None):
    add_data(item_id, q)
    return get_data()

# make a route that gets a song
@app.get("/get")
def get_item():
    return get_data()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
