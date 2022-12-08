from fastapi import APIRouter


router = APIRouter(
    prefix="/plays",
    tags=["plays"],
    responses={404: {"description": "Not found"}},
)