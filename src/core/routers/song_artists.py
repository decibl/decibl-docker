from fastapi import APIRouter


router = APIRouter(
    prefix="/song_artists",
    tags=["song_artists"],
    responses={404: {"description": "Not found"}},
)