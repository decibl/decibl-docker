from fastapi import APIRouter


router = APIRouter(
    prefix="/song_artists",
    tags=["song_artists"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{song_id}")
async def read_song_artists_by_song_id(song_id: str):
    pass

@router.get("/")
async def read_all_song_artists():
    pass

@router.post("/")
async def create_song_artist():
    pass