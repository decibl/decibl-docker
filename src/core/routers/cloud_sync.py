import sys

sys.path.append("..")

from fastapi import APIRouter
from remote_tree import RemoteTree
import json
from deepdiff import DeepDiff

router = APIRouter(
    prefix="/sync",
    tags=["sync"],
    responses={404: {"description": "Not found"}},
)

remoteTree = RemoteTree()

@router.get("/{local_tree}")
async def read_remote_sync(local_tree):
    diff = DeepDiff(local_tree,remoteTree.get_json())
    

@router.put("/{changes}")
async def edit_remote_branch(changes):
    for change in changes["additions"]:
        remoteTree.insertFile(change)
    
    for change in changes["deletions"]:
        remoteTree.insertFile(change)