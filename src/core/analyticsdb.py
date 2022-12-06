import datetime
import os
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
# 
# SONG_ARTISTS
# ARTIST_NAME SONG_ID DT_ADDED
# ALBUM_ARTISTS
# ARTIST_NAME song_id DT_ADDED
# COMPOSERS
# COMPOSER_NAME SONG_ID DT_ADDED
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
        # This is going to be a LOT of data, make a table with the following:
        # Create the table
        cursor.execute("""CREATE TABLE songs (
            song_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT,
            filesize INTEGER,
            padding INTEGER,
            album_artwork_bit_depth INTEGER,
            album_artwork_colors INTEGER,
            album_artwork_height INTEGER,
            album_artwork_width INTEGER,
            bit_depth INTEGER,
            bitrate INTEGER,
            channels INTEGER,
            duration INTEGER,
            sample_rate INTEGER,
            album TEXT,
            barcode TEXT,
            date_created TEXT,
            disc_number INTEGER,
            disc_total INTEGER,
            genre TEXT,
            isrc TEXT,
            itunesadvisory TEXT,
            length INTEGER,
            publisher TEXT,
            rating INTEGER,
            title TEXT,
            track_number INTEGER,
            track_total INTEGER,
            source TEXT,
            favorited BOOLEAN
        )""")
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

    def create_song_artists_table(self) -> bool:
        """Create the song_artists table, returns True if successful, False if not."""

        # Song_id is a foreign key to the songs table
        logging.info("Creating song_artists table")
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS song_artists (
                artist_name TEXT NOT NULL,
                song_id INTEGER NOT NULL,
                dt_added TEXT NOT NULL
            );"""
        )
        self.conn.commit()
        logging.info("Created song_artists table")
        return True

    def create_album_artists_table(self) -> bool:
        """Create the album_artists table, returns True if successful, False if not."""

        # Album_id is a foreign key to the songs table
        logging.info("Creating album_artists table")
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS album_artists (
                artist_name TEXT NOT NULL,
                song_id INTEGER NOT NULL,
                dt_added TEXT NOT NULL
            );"""
        )
        self.conn.commit()
        logging.info("Created album_artists table")
        return True

    def create_composers_table(self) -> bool:
        """Create the composers table, returns True if successful, False if not."""

        # Song_id is a foreign key to the songs table
        logging.info("Creating composers table")
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS composers (
                composer_name TEXT NOT NULL,
                song_id INTEGER NOT NULL,
                dt_added TEXT NOT NULL
            );"""
        )
        self.conn.commit()
        logging.info("Created composers table")
        return True

    def create_all_tables(self) -> bool:
        """Create all the tables, returns True if successful, False if not."""
        logging.info("Creating all tables")
        self.create_songs_table()
        self.create_plays_table()
        self.create_playlists_table()
        self.create_playlists_songs_table()
        self.create_song_artists_table()
        self.create_album_artists_table()
        self.create_composers_table()
        logging.info("Created all tables")
        return True

    def clear_all_tables(self) -> bool:
        """Clear all the tables, returns True if successful, False if not."""
        logging.info("Clearing all tables")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM songs;")
        cursor.execute("DELETE FROM plays;")
        cursor.execute("DELETE FROM playlists;")
        cursor.execute("DELETE FROM playlists_songs;")
        cursor.execute("DELETE FROM song_artists;")
        cursor.execute("DELETE FROM album_artists;")
        cursor.execute("DELETE FROM composers;")
        self.conn.commit()
        logging.info("Cleared all tables")
        return True

    def delete_database(self) -> bool:
        """Delete the database, returns True if successful, False if not."""
        logging.info("Deleting database")
        os.remove(config.DATABASE_PATH)
        logging.info("Deleted database")
        return True
    
    # --------------------------------------------------------------------------------------------
    #                                    RETRIEVE DATA
    # --------------------------------------------------------------------------------------------

    def get_all_tables(self) -> list:
        """Get all the tables in the database, returns a list of table names."""
        logging.info("Getting all tables")
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logging.info("Got all tables")
        return tables

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


    # --------------------------------------------------------------------------------------------
    #                                    INSERT DATA
    # --------------------------------------------------------------------------------------------
       
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

        # Zip the database file and name it with the current date
        # then move it to config.DATABASE_BACKUP_PATH
        # database is at config.DATABASE_PATH

        with zipfile.ZipFile(f"{config.DATABASE_BACKUP_PATH}/{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.zip", 'w') as zip:
            zip.write(config.DATABASE_PATH, arcname="analytics.db")

        logging.info("Backed up database")
        return True


if __name__ == "__main__":
    # create an instance of the database handler
    db_handler = AnalyticsDBHandler()
    db_handler.create_all_tables()
