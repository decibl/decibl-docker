import os
import shutil
import sys
import logging
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

import config
import models, schemas

# log a message
logging.info("Loading database module")


# Make Database class to hold all the data analytics
# This will be used to create and manage the database of the users activity.
# (there's lots of data in the songs table so I'm not going to put it in the graphic)
# ╔══════════════════════════════════════════════════════╗
# ║                         SONGS                        ║
# ╠═══════════╦══════════╦═══════╦════════╦═══════╦══════╣
# ║ **SONG_ID ║ FILEPATH ║ TITLE ║ ARTIST ║ ALBUM ║ ETC. ║
# ║           ║          ║       ║        ║       ║      ║
# ║           ║          ║       ║        ║       ║      ║
# ╚═══════════╩══════════╩═══════╩════════╩═══════╩══════╝
# ╔═══════════════════════════════════════════════════════════╗
# ║                           PLAYS                           ║
# ╠═══════════╦═════════════╦═════════════╦══════════╦════════╣
# ║ **PLAY_ID ║ *SONG_TITLE ║ SONG_ARTIST ║ START_DT ║ END_DT ║
# ║           ║             ║             ║          ║        ║
# ║           ║             ║             ║          ║        ║
# ║           ║             ║             ║          ║        ║
# ║           ║             ║             ║          ║        ║
# ╚═══════════╩═════════════╩═════════════╩══════════╩════════╝
# ╔════════════════════════════════════════════╗
# ║                  PLAYLISTS                 ║
# ╠═══════════════╦═══════════════╦════════════╣
# ║ **PLAYLIST_ID ║ PLAYLIST_NAME ║ CREATED_DT ║
# ║               ║               ║            ║
# ║               ║               ║            ║
# ║               ║               ║            ║
# ╚═══════════════╩═══════════════╩════════════╝
# ╔═════════════════════════════════════╗
# ║           PLAYLISTS_SONGS           ║
# ╠═══════════════╦══════════╦══════════╣
# ║ **PLAYLIST_ID ║ *SONG_ID ║ ADDED_DT ║
# ║               ║          ║          ║
# ║               ║          ║          ║
# ║               ║          ║          ║
# ╚═══════════════╩══════════╩══════════╝


class AnalyticsDBHandler:
    """Class to handle all the data analytics, especially stuff like creating tables, making backups, etc."""


    # CONSTRUCTOR

    def __init__(self) -> None:
        # The argument:
        # connect_args={"check_same_thread": False}
        # ...is needed only for SQLite. It's not needed for other databases.
        self.engine = create_engine(
            config.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )

        SessionLocal = self.get_local_session()

        # config.DBbase.metadata.create_all(bind=self.engine)
        # Create the database if it doesn't exist
        # use sqlite3 to create the database config.DATABASE_PATH
        if not os.path.exists(config.DATABASE_PATH):
            logging.info("Database not found, creating...")
            conn = sqlite3.connect(config.DATABASE_PATH)
            



    def get_local_session(self) -> sessionmaker:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return SessionLocal

    # --------------------------------------------------------------------------------------------
    #                                    CREATE TABLES
    # --------------------------------------------------------------------------------------------



    # --------------------------------------------------------------------------------------------
    #                                    GET DATA
    # --------------------------------------------------------------------------------------------

    # song will have a LOT of data
    def get_plays_by_id(self, db: Session, id: int):
        return db.query(models.Plays).filter(models.Plays.id == id).first()

    def get_plays_by_song_id(self, db: Session, song_id: int):
        return db.query(models.Plays).filter(models.Plays.song_id == song_id).all()

    def get_plays(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Plays).offset(skip).limit(limit).all()

    def get_song_by_id(self, db: Session, id: int):
        return db.query(models.Songs).filter(models.Songs.id == id).first()

    def get_songs(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Songs).offset(skip).limit(limit).all()

    def get_playlist_by_id(self, db: Session, id: int):
        return db.query(models.Playlists).filter(models.Playlists.id == id).first()

    def get_playlists(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Playlists).offset(skip).limit(limit).all()

    # --------------------------------------------------------------------------------------------
    #                                    CREATE DATA
    # --------------------------------------------------------------------------------------------

    def create_play(self, db: Session, play: schemas.PlaysCreate):
        db_play = models.Plays(**play.dict())
        db.add(db_play)
        db.commit()
        db.refresh(db_play)
        return db_play

    def create_song(self, db: Session, song: schemas.SongsCreate):
        db_song = models.Songs(**song.dict())
        db.add(db_song)
        db.commit()
        db.refresh(db_song)
        return db_song

    def create_playlist(self, db: Session, playlist: schemas.PlaylistsCreate):
        db_playlist = models.Playlists(**playlist.dict())
        db.add(db_playlist)
        db.commit()
        db.refresh(db_playlist)
        return db_playlist

    def create_playlist_song(self, db: Session, playlist_song: schemas.PlaylistSongsCreate):
        db_playlist_song = models.PlaylistsSongs(**playlist_song.dict())
        db.add(db_playlist_song)
        db.commit()
        db.refresh(db_playlist_song)
        return db_playlist_song
        


    # --------------------------------------------------------------------------------------------
    #                                  Backup and Restore
    # --------------------------------------------------------------------------------------------

    def backup_database(self) -> bool:
        """Backup the database, returns True if successful, False if not."""
        logging.info("Backing up database")
        try:
            shutil.copyfile(config.DATABASE_PATH, config.DATABASE_BACKUP_PATH)
            logging.info("Backed up database")
            return True
        except Exception as e:
            logging.error(f"Error backing up database: {e}")
            return False

    def restore_database(self) -> bool:
        """Restore the database, returns True if successful, False if not."""
        logging.info("Restoring database")
        try:
            shutil.copyfile(config.DATABASE_BACKUP_PATH, config.DATABASE_PATH)
            logging.info("Restored database")
            return True
        except Exception as e:
            logging.error(f"Error restoring database: {e}")
            return False


if __name__ == "__main__":
    # create an instance of the database handler
    db_handler = AnalyticsDBHandler()
