import datetime
import os
import shutil
import sys
import logging
import sqlite3
import zipfile

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
# ** = Primary Key
# * = Foreign Key

class AnalyticsDBHandler:
    """Class to handle all the data analytics, especially stuff like creating tables, making backups, etc."""


    # CONSTRUCTOR

    def __init__(self) -> None:
        self.conn = sqlite3.connect(config.DATABASE_PATH)

    # --------------------------------------------------------------------------------------------
    #                                    CREATE TABLES
    # --------------------------------------------------------------------------------------------

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
        logging.info("Creating plays table")
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS plays (
                play_id INTEGER PRIMARY KEY AUTOINCREMENT,
                song_title TEXT NOT NULL,
                song_artist TEXT NOT NULL,
                start_dt TEXT NOT NULL,
                end_dt TEXT NOT NULL
            );"""
        )
        self.conn.commit()
        logging.info("Created plays table")
        return True

    def create_playlists_table(self) -> bool:
        """Create the playlists table, returns True if successful, False if not."""
        logging.info("Creating playlists table")
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS playlists (
                playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_name TEXT NOT NULL,
                created_dt TEXT NOT NULL
            );"""
        )
        self.conn.commit()
        logging.info("Created playlists table")
        return True

    def create_playlists_songs_table(self) -> bool:
        """Create the playlists_songs table, returns True if successful, False if not."""

        # Song_id is a foreign key to the songs table
        logging.info("Creating playlists_songs table")
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS playlists_songs (
                playlist_id INTEGER NOT NULL,
                song_id INTEGER NOT NULL,
                added_dt TEXT NOT NULL
            );"""
        )
        self.conn.commit()
        logging.info("Created playlists_songs table")
        return True

    def create_all_tables(self) -> bool:
        """Create all the tables, returns True if successful, False if not."""
        logging.info("Creating all tables")
        self.create_songs_table()
        self.create_plays_table()
        self.create_playlists_table()
        self.create_playlists_songs_table()
        logging.info("Created all tables")
        return True
    
    # --------------------------------------------------------------------------------------------
    #                                    RETRIEVE DATA
    # --------------------------------------------------------------------------------------------

    def get_song_by_id(self, song_id: int) -> tuple:
        """Get a song by its ID, returns a Song object."""
        logging.info(f"Getting song by ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM songs WHERE song_id = ?;""",
            (song_id,)
        )
        song = cursor.fetchone()
        logging.info(f"Got song by ID: {song_id}")
        return (song[0], song[1], song[2], song[3], song[4])

    def get_songs_by_title(self, title: str) -> list:
        """Get a list of songs by their title, returns a list of Song objects."""
        logging.info(f"Getting songs by title: {title}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM songs WHERE title = ?;""",
            (title,)
        )
        songs = cursor.fetchall()
        logging.info(f"Got songs by title: {title}")
        return [(song[0], song[1], song[2], song[3], song[4]) for song in songs]

    def get_song_by_title_and_artist(self, title: str, artist: str) -> tuple:
        """Get a song by its title and artist, returns a Song object."""
        logging.info(f"Getting song by title and artist: {title} - {artist}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM songs WHERE title = ? AND artist = ?;""",
            (title, artist)
        )
        song = cursor.fetchone()
        logging.info(f"Got song by title and artist: {title} - {artist}")
        return (song[0], song[1], song[2], song[3], song[4])


    def get_play_by_title_and_artist(self, title: str, artist: str) -> tuple:
        """Get a play by its title and artist, returns a Play object."""
        logging.info(f"Getting play by title and artist: {title} - {artist}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM plays WHERE song_title = ? AND song_artist = ?;""",
            (title, artist)
        )
        play = cursor.fetchone()
        logging.info(f"Got play by title and artist: {title} - {artist}")
        return (play[0], play[1], play[2], play[3], play[4])

    # --------------------------------------------------------------------------------------------
    #                                    INSERT DATA
    # --------------------------------------------------------------------------------------------

    # song will have a LOT of data
    def insert_song(self, filepath: str, title: str, artist: str, album: str) -> bool:
        """Insert a song into the database, returns True if successful, False if not."""
        logging.info("Inserting song into songs taable")
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO songs (filepath, title, artist, album) VALUES (?, ?, ?, ?);""",
            (filepath, title, artist, album)
        )

        self.conn.commit()
        logging.info("Inserted song")
        return True

    def insert_play(self, song_title: str, song_artist: str, start_dt: str, end_dt: str) -> bool:
        """Insert a play into the database, returns True if successful, False if not."""
        logging.info("Inserting play into plays table")
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO plays (song_title, song_artist, start_dt, end_dt) VALUES (?, ?, ?, ?);""",
            (song_title, song_artist, start_dt, end_dt)
        )

        self.conn.commit()
        logging.info("Inserted play")
        return True

    def insert_playlist(self, playlist_name: str, created_dt: str) -> bool:
        """Insert a playlist into the database, returns True if successful, False if not."""
        logging.info("Inserting playlist into playlists table")
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO playlists (playlist_name, created_dt) VALUES (?, ?);""",
            (playlist_name, created_dt)
        )

        self.conn.commit()
        logging.info("Inserted playlist")
        return True

    def insert_playlist_song(self, playlist_id: int, song_id: int, added_dt: str) -> bool:
        """Insert a playlist_song into the database, returns True if successful, False if not."""
        logging.info("Inserting playlist_song into playlists_songs table")
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO playlists_songs (playlist_id, song_id, added_dt) VALUES (?, ?, ?);""",
            (playlist_id, song_id, added_dt)
        )

        self.conn.commit()
        logging.info("Inserted playlist_song")
        return True
        


    # --------------------------------------------------------------------------------------------
    #                                  Backup and Restore
    # --------------------------------------------------------------------------------------------

    def backup_database(self) -> bool:
        """Backup the database, returns True if successful, False if not."""
        logging.info("Backing up database")

        # create config.DATABASE_BACKUP_PATH if it doesn't exist
        if not os.path.exists(config.DATABASE_BACKUP_PATH):
            os.makedirs(config.DATABASE_BACKUP_PATH)

        # Zip the database file and name it with the current date
        with zipfile.ZipFile(f"backup_{datetime.now().strftime('%Y-%m-%d')}.zip", "w") as zip:
            # file is in config.DATABASE_PATH
            zip.write(config.DATABASE_PATH)



if __name__ == "__main__":
    # create an instance of the database handler
    db_handler = AnalyticsDBHandler()

    # create the songs table
    db_handler.create_all_tables()
    db_handler.insert_song("filepath", "title", "artist", "album")

    song = db_handler.get_song_by_id(1)
    print(song)
    songs = db_handler.get_songs_by_title("title")
    print(songs)
    artistsong = db_handler.get_song_by_title_and_artist("title", "artist")
    print(artistsong)
