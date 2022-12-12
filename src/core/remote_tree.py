from fastapi import HTTPException
import uuid
import json

class FileNode():
    def __init__(self,filename: str,file_id: str,isFile: bool):
        self.children = []
        self.isFile = isFile
        self.filename = filename
        self.file_id = file_id
    
    def __str__(self) -> str:
        return(
            "{"+
            "\"filename\": \""+self.filename+
            "\", \"children\": \""+str(self.children)+
            "\", \"file_id\": \""+self.file_id+
            "\", \"isFile\": \""+str(self.isFile)+
            "\"}"
        )
    
class RemoteTree():

    def __init__(self):
        self.tree = {
            "root": FileNode("root",str(uuid.uuid4()),False)
        }
    def __str__(self) -> str:
        res = self.tree.copy()

        for node in self.tree:
            res[node] = json.loads(str(self.tree[node]))

        return str(res)

    def insertFile(self,dir: str,data: dict):
        if dir in self.tree:
            raise HTTPException(status_code=400, detail="File already Exists In This Directory")

        location = dir.split("/")
        parentDir = "/".join(location[:-1])
        self.tree[dir] = FileNode(data["filename"],data["file_id"],data["isFile"])
        self.tree[parentDir].children.append(dir)

    def removeFile(self,dir: str):
        if dir == "root":
            raise HTTPException(status_code=400, detail="Action Not Allowed: Cannot delete root folder") 
        elif dir not in self.tree:
            raise HTTPException(status_code=400, detail="Action Not Allowed: File Not Found") 
        self.recurDelete(dir)

    def recurDelete(self,dir: str):
        
        for child in self.tree[dir].children:
            if child in self.tree:
                if self.tree[child].isFile:
                    del self.tree[child]
                elif (not self.tree[child].isFile and self.tree[child].children == []):
                    del self.tree[child]
                else:
                    self.recurDelete(self.tree[child])
        del self.tree[dir]

if __name__ =="__main__":
    tree = RemoteTree()
    #res =json.loads(str(tree.tree["root"]))
    tree.insertFile("root/test.py",{
        "filename": "test",
        "file_id": "id2",
        "isFile": True
    })
    tree.insertFile("root/test.py3",{
        "filename": "test3",
        "file_id": "id2",
        "isFile": True
    })
    tree.insertFile("root/test.py2",{
        "filename": "test2",
        "file_id": "id2",
        "isFile": True
    })
    res = tree.tree.copy()

    for node in tree.tree:
        res[node] = json.loads(str(tree.tree[node]))
        
    print(res)

        

