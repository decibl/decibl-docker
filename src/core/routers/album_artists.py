from fastapi import APIRouter


router = APIRouter(
    prefix="/album_artists",
    tags=["album_artists"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{song_id}")
async def read_album_artist_by_song():
    pass

@router.get("/")
async def read_all_album_artist():
    pass

@router.post("/")
async def create_album_artist():
    pass




