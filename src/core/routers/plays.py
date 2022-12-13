from fastapi import APIRouter


router = APIRouter(
    prefix="/plays",
    tags=["plays"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{song_id}")
async def read_plays_by_song_id(song_id: str):
    pass

@router.get("/")
async def read_all_plays():
    pass

@router.post("/")
async def create_plays():
    pass