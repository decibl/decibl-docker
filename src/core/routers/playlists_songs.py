from fastapi import APIRouter


router = APIRouter(
    prefix="/playlist_songs",
    tags=["playlist_songs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_all_playlist_songs():
    pass

@router.post("/")
async def create_playlist_songs():
    pass