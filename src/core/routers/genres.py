from fastapi import APIRouter


router = APIRouter(
    prefix="/genres",
    tags=["genres"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{song_id}")
async def read_genre_by_song_id(song_id: str):
    pass

@router.get("/")
async def read_all_genres():
    pass

@router.get("/{genre_name}")
async def read_all_songs_by_genre_name(genre_bame: str):
    pass

@router.post("/")
async def create_album_artist():
    pass