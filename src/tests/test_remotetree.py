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
        "soundfiles": FileNode("soundfiles","id1",False),
        "soundfiles/test":FileNode("test","id2",False),
        "soundfiles/test/again":FileNode("again","id10",False),
        "soundfiles/test/poopy.mp3": FileNode("poopy.mp3","id3",True),
        "soundfiles/test/poop.mp3": FileNode("poop.mp3","id4",True),
        "soundfiles/test/poo.mp3": FileNode("poo.mp3","id5",True),
        "soundfiles/test/po.mp3": FileNode("po.mp3","id6",True),
        "soundfiles/test/p.mp3": FileNode("p.mp3","id7",True),
        "soundfiles/test.mp4": FileNode("test.mp3","id8",True),
        "soundfiles/tes.mp4": FileNode("tes.mp3","id9",True),
    }
    '''
    tree.insertFile("soundfiles/test",{
        "filename": "test",
        "file_id": "id2",
        "isFile": False
    })

    assert len(tree.tree) == 25

def test_insert_1():
    tree = remote_tree.RemoteTree()
    tree.insertFile("soundfiles/test.py",{
        "filename": "test",
        "file_id": "id2",
        "isFile": True
    })

    try:
        tree.insertFile("soundfiles/test.py",{
            "filename": "test",
            "file_id": "id2",
            "isFile": True
        })
    except:
        pass

    assert len(tree.tree) == 25

def test_vital_remove():
    tree = remote_tree.RemoteTree()
    tree.insertFile("soundfiles/test.py",{
        "filename": "test",
        "file_id": "id2",
        "isFile": True
    })

    tree.removeFile("soundfiles/test.py")

    assert len(tree.tree) == 24

def test_remove_soundfiles():
    tree = remote_tree.RemoteTree()
    try:
        tree.removeFile("soundfiles")
    except:
        pass 
    assert len(tree.tree) == 24

def test_remove_1():
    tree = remote_tree.RemoteTree()
    tree.insertFile("soundfiles/test",{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })
    tree.insertFile("soundfiles/test/test.mp3",{
        "filename": "test",
        "file_id": "id3",
        "isFile": True
    })
    tree.insertFile("soundfiles/test/tes.mp3",{
        "filename": "tes",
        "file_id": "id4",
        "isFile": True
    })
    tree.insertFile("soundfiles/test/te.mp3",{
        "filename": "te",
        "file_id": "id5",
        "isFile": True
    })
    tree.insertFile("soundfiles/second_test",{
        "filename": "second_test",
        "file_id": "id2",
        "isFile": False
    })

    tree.removeFile("soundfiles/test")

    assert len(tree.tree) == 25

def test_remove_2():
    tree = remote_tree.RemoteTree()
    tree.insertFile("soundfiles/test",{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })

    tree.removeFile("soundfiles/test")
    
    assert len(tree.tree) == 24

def test_remove_3():
    tree = remote_tree.RemoteTree()
    try:
        tree.removeFile("soundfiles/test")
    except:
        pass
    
    assert len(tree.tree) == 24

def test_remove_4():
    tree = remote_tree.RemoteTree()
    tree.insertFile("soundfiles/test",{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })
    tree.insertFile("soundfiles/test/test",{
        "filename": "test",
        "file_id": "id2",
        "isFile": False
    })

    tree.removeFile("soundfiles/test")
    
    assert len(tree.tree) == 24






   


