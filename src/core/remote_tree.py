from fastapi import HTTPException
import uuid
import json

import os
import songparser
import api


class FileNode:
    def __init__(self, filename: str, file_id: str, isFile: bool):
        self.children = []
        self.isFile = isFile
        self.filename = filename
        self.file_id = file_id

    def __str__(self) -> str:
        return (
            "{"
            + '"filename": "'
            + self.filename
            + '", "children": "'
            + str(self.children)
            + '", "file_id": "'
            + self.file_id
            + '", "isFile": "'
            + str(self.isFile)
            + '"}'
        )

class RemoteTree:
    def __init__(self,dir):
        self.tree = {}
        self.abs_dir = dir
        self.tree[dir] = FileNode("soundfiles",str(uuid.uuid4()),False)
        self.populate_with_files(dir)

    def get_json(self):
        visited = set()
        def dfs(root,curr): 
            if root in visited:
                return None
            visited.add(root)
            curr["filename"] = self.tree[root].filename
            curr["file_id"] = self.tree[root].file_id
            curr["isFile"] = self.tree[root].isFile
            curr["children"] = [dfs(child,{}) for child in self.tree[root].children]
            return curr
        
        return dfs(self.abs_dir,{})

    def insertFile(self, dir: str, data: dict):
        if dir in self.tree:
            raise HTTPException(
                status_code=400, detail="File already Exists In This Directory"
            )

        location = dir.split("/")
        parentDir = "/".join(location[:-1])
        self.tree[dir] = FileNode(location[-1],data["file_id"],data["isFile"])

        if location[-1] != "soundfiles":
            self.tree[parentDir].children.append(dir)

    def removeFile(self,dir: str):
        if dir == api.path:
            raise HTTPException(status_code=400, detail="Action Not Allowed: Cannot delete root folder") 
        elif dir not in self.tree:
            raise HTTPException(
                status_code=400, detail="Action Not Allowed: File Not Found"
            )
        self.recurDelete(dir)
        location = dir.split("/")
        parentDir = "/".join(location[:-1])
        if location[-1] != "soundfiles":
            self.tree[parentDir].children.remove(dir)

    def recurDelete(self, dir: str):

        for child in self.tree[dir].children:
            if child in self.tree:
                if self.tree[child].children == []:
                    del self.tree[child]
                else:
                    self.recurDelete(child)
        del self.tree[dir]

    def checkIsFile(self, dir: str):
        for i in range(len(dir) - 1, -1, -1):
            if dir[i] == ".":
                return True
        return False

    def populate_with_files(self, dir: str):
        for root, dirs, files in os.walk(dir):
            for file in files:
                res = root.replace('\\','/')
                new_dir = str(res.encode('utf-8'))[2:-1]
                if (self.checkIsFile and (new_dir not in self.tree)):
                    self.insertFile(new_dir,{
                        "file_id": str(uuid.uuid4()),
                        "isFile": False
                    })
                filehash = songparser.file_to_hash(os.path.join(root, file))
                self.insertFile(new_dir+"/"+file,{
                    "file_id": str(filehash),
                    "isFile": True
                })
        


if __name__ =="__main__":

    # tree.removeFile("soundfiles/test1/mommy")
    # print(tree.tree["soundfiles/test1"].children)
    tree = RemoteTree(api.path)
    path = os.path.join(api.path,"balls")
    path = path.replace("\\","/")
    try:
        tree.removeFile(path)
    except:
        pass 

    print(tree.tree)
