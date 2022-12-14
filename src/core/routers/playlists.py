from fastapi import APIRouter


router = APIRouter(
    prefix="/playlists",
    tags=["playlists"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{playlist_name}")
async def read_songs_by_playlist_name(playlist_name: str):
    pass

@router.get("/{playlist_id}")
async def read_playlist_by_id(playlists_id: str):
    pass

@router.post("/")
async def create_playlist():
    pass