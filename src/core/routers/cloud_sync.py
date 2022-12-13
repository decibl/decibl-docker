import sys,os
  
import main
from fastapi import APIRouter
import json
from deepdiff import DeepDiff

router = APIRouter(
    prefix="/sync",
    tags=["sync"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_remote_sync():
   return main.remoteTree.get_json()

@router.get("/{local_tree}")
async def read_remote_sync(local_tree):
    diff = DeepDiff(local_tree,main.remoteTree.get_json())
    

@router.put("/{changes}")
async def edit_remote_branch(changes):
    for change in changes["additions"]:
        main.remoteTree.insertFile(change)
    
    for change in changes["deletions"]:
        main.remoteTree.insertFile(change)