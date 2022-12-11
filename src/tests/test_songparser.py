import pytest
import sys
import os
import sqlite3
import random
import zipfile

# add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "core")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "backups")))
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "databases")))
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "soundfiles")))

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "testsongs")))

import config
import analyticsdb
import songparser


def test_file_to_hash():
    filepath = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "testsongs", "02 - Gemstone.flac"))
    hash = songparser.file_to_hash(filepath)
    assert hash == "23fb2258052511a4d07bc555a1b45a41fbd8da0f3ec4a887c9c7282351672956"


