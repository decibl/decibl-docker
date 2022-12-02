import os
import sys
import logging
import sqlite3

# add current file to system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import config

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
# ╔════════════════════════════════════════════╗
# ║                    PLAYS                   ║
# ╠═══════════╦════════════╦══════════╦════════╣
# ║ **PLAY_ID ║ SONG_TITLE ║ START_DT ║ END_DT ║
# ║           ║            ║          ║        ║
# ║           ║            ║          ║        ║
# ╚═══════════╩════════════╩══════════╩════════╝
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

    def __init__(self) -> None:
        self.conn = sqlite3.connect(config.DATABASE_PATH)

    def create_songs_table(self) -> bool:
        """Create the songs table, returns True if successful, False if not."""
        logging.info("Creating songs table")
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT NOT NULL,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                album TEXT NOT NULL
            );"""
        )

        self.conn.commit()
        logging.info("Created songs table")
        return True

    def create_plays_table(self) -> bool:
        """Create the plays table, returns True if successful, False if not."""
        pass

    def create_playlists_table(self) -> bool:
        """Create the playlists table, returns True if successful, False if not."""
        pass

    def create_playlists_songs_table(self) -> bool:
        """Create the playlists_songs table, returns True if successful, False if not."""
        pass

    def create_all_tables(self) -> bool:
        """Create all the tables, returns True if successful, False if not."""
        pass

    def backup_database(self) -> bool:
        """Backup the database, returns True if successful, False if not."""
        pass

    def restore_database(self) -> bool:
        """Restore the database, returns True if successful, False if not."""
        pass


if __name__ == "__main__":
    # create an instance of the database handler
    db_handler = AnalyticsDBHandler()

    # create the songs table
    db_handler.create_songs_table()