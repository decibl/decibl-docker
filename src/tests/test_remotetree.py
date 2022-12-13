import pytest
import sys
import os
import random
import json
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "core")))

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "soundfiles")))

import remote_tree
import config

TEST_SONGS_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "testsongs3"))

WRITE_TREE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "remotetree.json"))

def test_tree():
    tree = remote_tree.RemoteTree(TEST_SONGS_PATH)
    tree.populateTree()

    # write tree.traverse() to a file so it can be read back as a dict
    # with open(WRITE_TREE_PATH, "w") as f:
    #     f.write(json.dumps(tree.traverse()))

    # read the tree back from the file
    with open(WRITE_TREE_PATH, "r") as f:
        tree_dict = json.loads(f.read())

    # go through the tree and make sure the files are the same
    def traverse(tree_dict, current_node = None):
        if current_node == None:
            current_node = tree.tree["root"]

        assert current_node.filename == tree_dict["filename"]
        assert current_node.file_id == tree_dict["file_id"]
        assert current_node.isFile == tree_dict["isFile"]
        # assert current_node.file_path == tree_dict["file_path"]

        for child in current_node.children:
            traverse(tree_dict["children"].pop(0), child)

    traverse(tree_dict)