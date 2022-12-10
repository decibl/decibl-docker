from fastapi import APIRouter


router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{song_id}")
async def read_song_by_id():
    pass



@router.get("/")
async def read_all_album_artist():
    pass

@router.post("/")
async def create_album_artist():
    pass