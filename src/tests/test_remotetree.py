import pytest
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "core")))

import api

import remote_tree

def test_sanity():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test1","mommy")
    path = path.replace("\\","/")
    tree.removeFile(path)

def test_vital_insert():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id2",
        "isFile": False
    })

    assert len(tree.tree) == 25

def test_insert_1():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test.py")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id2",
        "isFile": True
    })

    try:
        tree.insertFile(path,{
            "filename": "test",
            "file_id": "id2",
            "isFile": True
        })
    except:
        pass

    assert len(tree.tree) == 25

def test_vital_remove():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test.py")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id2",
        "isFile": True
    })

    tree.removeFile(path)

    assert len(tree.tree) == 24

def test_remove_soundfiles():
    tree = remote_tree.RemoteTree(api.path)
    try:
        tree.removeFile(api.path)
    except:
        pass 
    assert len(tree.tree) == 24

def test_remove_1():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })
    path = os.path.join(api.path,"test","test.mp3")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id3",
        "isFile": True
    })
    path = os.path.join(api.path,"test","tes.mp3")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "tes",
        "file_id": "id4",
        "isFile": True
    })
    path = os.path.join(api.path,"test","te.mp3")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "te",
        "file_id": "id5",
        "isFile": True
    })
    path = os.path.join(api.path,"test","second_test")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "second_test",
        "file_id": "id2",
        "isFile": False
    })
    path = os.path.join(api.path,"test")
    path = path.replace("\\","/")
    tree.removeFile(path)

    assert len(tree.tree) == 24

def test_remove_2():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })

    tree.removeFile(path)
    
    assert len(tree.tree) == 24

def test_remove_3():
    tree = remote_tree.RemoteTree(api.path)
    try:
        tree.removeFile("soundfiles/test")
    except:
        pass
    
    assert len(tree.tree) == 24

def test_remove_4():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id1",
        "isFile": False
    })
    path = os.path.join(api.path,"test","test")
    path = path.replace("\\","/")
    tree.insertFile(path,{
        "filename": "test",
        "file_id": "id2",
        "isFile": False
    })
    path = os.path.join(api.path,"test")
    path = path.replace("\\","/")
    tree.removeFile(path)
    
    assert len(tree.tree) == 24

def test_remove_5():
    tree = remote_tree.RemoteTree(api.path)
    path = os.path.join(api.path,"test1","mommy")
    path = path.replace("\\","/")
    tree.removeFile(path)
    
    assert len(tree.tree) == 22

    path = os.path.join(api.path,"test1")
    path = path.replace("\\","/")
    assert len(tree.tree[path].children) == 1






   


