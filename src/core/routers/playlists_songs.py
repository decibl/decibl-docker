from fastapi import APIRouter


router = APIRouter(
    prefix="/playlist_songs",
    tags=["playlist_songs"],
    responses={404: {"description": "Not found"}},
)