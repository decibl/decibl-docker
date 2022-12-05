import os
import shutil
import sys
import logging
import sqlite3

# add current file to system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# log a message
logging.info("Loading database module")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///../analyticsdb/analyticsdb.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
'''
The argument:
connect_args={"check_same_thread": False}
...is needed only for SQLite. It's not needed for other databases.
'''
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

