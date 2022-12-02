import os, sys, logging

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
        pass

    def create_songs_table(self) -> bool:
        """Create the songs table, returns True if successful, False if not."""
        pass

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