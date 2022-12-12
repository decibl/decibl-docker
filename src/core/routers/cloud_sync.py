from fastapi import APIRouter
from ..main import remoteTree

router = APIRouter(
    prefix="/sync",
    tags=["sync"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_remote_sync():
    remoteTree.

@router.put("/")
async def edit_remote_branch():
    pass