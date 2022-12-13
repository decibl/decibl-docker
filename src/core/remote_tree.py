from fastapi import HTTPException
import uuid
import json
import os,sys

import config
import songparser

class FileNode():
    """
    FileNode is a class that represents a file or a directory in the remote tree
    
    """
    def __init__(self, filename: str, file_id: str, isFile: bool, file_path: str = ""):
        self.children = []
        self.isFile = isFile
        self.filename = filename
        self.file_id = file_id
        self.file_path = file_path

    def __str__(self) -> str:
        return self.filename

    def __repr__(self) -> str:
        return self.filename


class RemoteTree():

    def __init__(self, soundfiles_path: str = config.SOUNDFILES_PATH):
        self.tree = {
            "root": FileNode("root", "DIR", False, config.SOUNDFILES_PATH)
        }
        self.soundfiles_path = soundfiles_path
        

    def insertFile(self, fileNode: FileNode):
        """
        Inserts a file into the tree. Look at the path of the file and cut off the root path. If there are any directories in the path, create them and insert them into the tree. Then insert the file into the tree.

        Args:
            fileNode (FileNode): The file node to insert
        """

        insertion_path = fileNode.file_path.replace(self.soundfiles_path + "\\", "")
        print(insertion_path)
        # turn path into an os path
        insertion_path = os.path.normpath(insertion_path)

        # split the path into a list of directories
        insertion_path = insertion_path.split(os.sep)


        current_location = self.tree["root"]

        print(insertion_path)
        
        # while there are still directories in the path, add the directory/file to the tree
        # if i wanted to add test1/lol1/split.txt, i would add test1 to root's children, then lol1 to test1's children, then split.txt to lol1's children

        while len(insertion_path) > 0:
            # get the next directory in the path
            next_item = insertion_path.pop(0)

            # add the current item to the current location's children if it doesn't exist
            if next_item not in [child.filename for child in current_location.children]:
                # if file, hash it
                if len(insertion_path) == 0:
                    current_location.children.append(FileNode(next_item, songparser.file_to_hash(fileNode.file_path), True, fileNode.file_path))
                else:
                    current_location.children.append(FileNode(next_item, "DIR", False))

            # set the current location to the next item
            current_location = [child for child in current_location.children if child.filename == next_item][0]

            



    def populateTree(self):
        """
        Populates the tree with all the files in the soundfiles directory
        """
        for root, dirs, files in os.walk(self.soundfiles_path):
            for file in files:
                filehash = songparser.file_to_hash(os.path.join(root, file))
                file_path = os.path.join(root, file)
                self.insertFile(FileNode(file, filehash, True, file_path))

    # get the tree in a json forma
    # set current node to root
    def traverse(self, current_node = None):
        """
        Traverses the tree and returns a json representation of the tree
        """

        json_dict = {}

        if current_node == None:
            current_node = self.tree["root"]

        json_dict["filename"] = current_node.filename
        json_dict["file_id"] = current_node.file_id
        json_dict["isFile"] = current_node.isFile
        json_dict["file_path"] = current_node.file_path
        json_dict["children"] = []

        for child in current_node.children:
            json_dict["children"].append(self.traverse(child))

        return json_dict
        

    def pretty_print(self):
        """
        Prints the tree in a pretty format
        """
        print(json.dumps(self.traverse(), indent=4))



    
if __name__ == "__main__":
    tree = RemoteTree()
    tree.populateTree()
    # print(tree.tree['root'].children)
    print(tree.traverse())
    tree.pretty_print()


    