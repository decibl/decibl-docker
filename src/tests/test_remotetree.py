import pytest
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "core")))

import remote_tree

def test_vital_insert():
    tree = remote_tree.RemoteTree()
    '''
    tree = {
        "root": FileNode("root","id1",False),
        "root/test":FileNode("test","id2",False),
        "root/test/again":FileNode("again","id10",False),
        "root/test/poopy.mp3": FileNode("poopy.mp3","id3",True),
        "root/test/poop.mp3": FileNode("poop.mp3","id4",True),
        "root/test/poo.mp3": FileNode("poo.mp3","id5",True),
        "root/test/po.mp3": FileNode("po.mp3","id6",True),
        "root/test/p.mp3": FileNode("p.mp3","id7",True),
        "root/test.mp4": FileNode("test.mp3","id8",True),
        "root/tes.mp4": FileNode("tes.mp3","id9",True),
    }
    '''
    tree.insertFile("root/test",{
        "filename": "test",
        "file_id": "id2",
        "isFile": False
    })

    assert len(tree.tree) == 2

def test_insert_1():
    tree = remote_tree.RemoteTree()
    tree.insertFile("root/test.py",{
        "filename": "test",
        "file_id": "id2",
        "isFile": True
    })

    try:
        tree.insertFile("root/test.py",{
            "filename": "test",
            "file_id": "id2",
            "isFile": True
        })
    except:
        pass

    assert len(tree.tree) == 2

def test_vital_remove():
    tree = remote_tree.RemoteTree()
    tree.insertFile("root/test.py",{
        "filename": "test",
        "file_id": "id2",
        "isFile": True
    })

    tree.removeFile("root/test.py")

    assert len(tree.tree) == 1

def test_remove_root():
    tree = remote_tree.RemoteTree()
    try:
        tree.removeFile("root")
    except:
        pass 
    assert len(tree.tree) == 1

def test_remove_1():
    tree = remote_tree.RemoteTree()
    tree.insertFile("root/test",{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })
    tree.insertFile("root/test/test.mp3",{
        "filename": "test",
        "file_id": "id3",
        "isFile": True
    })
    tree.insertFile("root/test/tes.mp3",{
        "filename": "tes",
        "file_id": "id4",
        "isFile": True
    })
    tree.insertFile("root/test/te.mp3",{
        "filename": "te",
        "file_id": "id5",
        "isFile": True
    })
    tree.insertFile("root/second_test",{
        "filename": "second_test",
        "file_id": "id2",
        "isFile": False
    })

    tree.removeFile("root/test")

    assert len(tree.tree) == 2

def test_remove_2():
    tree = remote_tree.RemoteTree()
    tree.insertFile("root/test",{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })

    tree.removeFile("root/test")
    
    assert len(tree.tree) == 1

def test_remove_3():
    tree = remote_tree.RemoteTree()
    try:
        tree.removeFile("root/test")
    except:
        pass
    
    assert len(tree.tree) == 1

def test_remove_4():
    tree = remote_tree.RemoteTree()
    tree.insertFile("root/test",{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })
    tree.insertFile("root/test/test",{
        "filename": "test",
        "file_id": "id2",
        "isFile": False
    })

    tree.removeFile("root/test")
    
    assert len(tree.tree) == 1






   


