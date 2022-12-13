from fastapi import APIRouter
import config
import os

import main

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{song_id}")
async def read_song_by_id(song_id: str):
    pass

@router.get("/get_song/{song_path}")
async def get_song(song_path: str):
    print(song_path)
    song_loc = os.path.abspath(os.path.join(
        config.SOUNDFILES_PATH, song_path))
    main.logger.info(song_loc)
    if os.path.exists(song_loc):
        with open(song_loc, "rb") as f:
            return {"song_name": song_path, "song_bytes": f.read().hex()}
    else:
        # return a not found error
        return {"error": "song not found"}


@router.get("/")
async def read_all_album_artist():
    pass

@router.post("/")
async def create_album_artist():
    pass