from typing import Union

from fastapi import FastAPI

app = FastAPI()

from EXAMPLE_DB_FASTAPI import *

make_db()

# make a route that adds data to the list
@app.get("/add/{item_id}")
def add_item(item_id: int, q: str = None):
    add_data(item_id, q)
    return get_data()

# make a route that gets data from the list
@app.get("/get")
def get_item():
    return get_data()
    



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

