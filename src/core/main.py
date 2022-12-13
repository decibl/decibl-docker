from fastapi import Depends, FastAPI
from analyticsdb import init_db
from routers import album_artists,composers,genres,playlists_songs,playlists,plays,song_artists,songs,cloud_sync

app = FastAPI(
    prefix="/api",
    tags=["api"],
    dependencies=[Depends(init_db)]
)

#app.include_router(album_artists.router)
#app.include_router(composers.router)
#app.include_router(genres.router)
#app.include_router(playlists_songs.router)
#app.include_router(playlists.router)
#app.include_router(plays.router)
#app.include_router(song_artists.router)
#app.include_router(songs.router)
#app.include_router(cloud_sync.router)

'''
@router.get("/users/", tags=["users"],)
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
'''