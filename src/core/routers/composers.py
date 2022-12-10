from fastapi import APIRouter


router = APIRouter(
    prefix="/composers",
    tags=["composers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{song_id}")
async def read_composers_by_song_id():
    pass

@router.get("/")
async def read_all_composers():
    pass

@router.post("/")
async def create_composer():
    pass




