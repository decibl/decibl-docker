from typing import Union
from fastapi import FastAPI
import random
import analyticsdb
import os,sys

import config

app = FastAPI(debug=True)

def lmao():
    return "lmao{}".format(random.randint(0, 100))


# make a route that adds a song
@app.get("/hi")
async def hi():
    # return value of lmao()
    return lmao()

# make an endpoint that sends info of a song, song_name and bytes


@app.get("/get_song/{song_path}")
async def get_song(song_path: str):
    print(song_path)
    song_loc = os.path.abspath(os.path.join(
        config.SOUNDFILES_PATH, song_path))
    with open ("example.txt", "w") as f:
        f.write(song_loc)
    if os.path.exists(song_loc):
        with open(song_loc, "rb") as f:
            return {"song_name": song_path, "song_bytes": f.read().hex()}
    else:
        # return a not found error
        return {"error": "song not found"}