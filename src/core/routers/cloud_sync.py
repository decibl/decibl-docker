from fastapi import APIRouter
from ..main import remoteTree
import json

router = APIRouter(
    prefix="/sync",
    tags=["sync"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_remote_sync():
    pass

@router.put("/")
async def edit_remote_branch():
    pass