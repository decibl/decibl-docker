import datetime
import os
import sys
import sqlite3
from typing import Dict, List
import zipfile
# add current file to system path

import logging
import config
import songparser

from fastapi import HTTPException

# log a message
logging.info("Loading database module")

# Make Database class to hold all the data analytics
# This will be used to create and manage the database of the users activity.
# (there's lots of data in the songs table so I'm not going to put it in the graphic)


class AnalyticsDBHandler:
    """Class to handle all the data analytics, especially stuff like creating tables, making backups, etc."""

    # CONSTRUCTOR

    def __init__(self, debug_path=None) -> None:
        """
        __init__ Initialize the database handler. Creates the database at the path specified in config.py

        Args:
            debug_path (str, optional): Path to the database for debug. Defaults to None.
        """
        if debug_path is None:
            self.conn = sqlite3.connect(config.DATABASE_PATH)
        else:
            self.conn = sqlite3.connect(debug_path)

    # ------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------
    #                                    Error Handling
    # --------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    def raise_table_not_created(self, table, details):
        err = "Unable to create "+table+" table: "+details
        logging.info(err)
        raise HTTPException(status_code=400, detail=err)

    # ------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------
    #                                    CREATE TABLES
    # --------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    def create_songs_table(self):
        """
        create_songs_table Creates the songs table in the database.
        """
        try:
            logging.info("Creating songs table")
            cursor = self.conn.cursor()
            # This is going to be a LOT of data, make a table with the following:
            # Create the table
            cursor.execute("""CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT,
                filesize BIGINT,
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
                isrc TEXT,
                itunesadvisory TEXT,
                length INTEGER,
                publisher TEXT,
                rating INTEGER,
                title TEXT,
                track_number INTEGER,
                track_total INTEGER,
                source TEXT,
                main_artist TEXT
            )""")
            self.conn.commit()
            logging.info("Created songs table")
        except:
            self.raise_table_not_created("song", "unable to create table")

    def create_plays_table(self):
        """
        create_plays_table Creates the plays table in the database.
        """
        try:
            logging.info("Creating plays table")
            cursor = self.conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS plays (
                    play_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    song_title TEXT NOT NULL,
                    song_primary_artist TEXT NOT NULL,
                    filesize BIGINT,
                    start_dt TEXT NOT NULL,
                    end_dt TEXT NOT NULL
                );"""
            )
            self.conn.commit()
            logging.info("Created plays table")
        except:
            self.raise_table_not_created("plays", "unable to create table")

    def create_playlists_table(self) -> bool:
        """
        create_playlists_table Creates the playlists table in the database.

        Returns:
            bool: True if successful, False if not.
        """
        try:
            logging.info("Creating playlists table")
            cursor = self.conn.cursor()

            # description is a text that is
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS playlists (
                    playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    playlist_name TEXT NOT NULL,
                    playlist_desc TEXT,
                    created_dt TEXT NOT NULL
                );"""
            )
            self.conn.commit()
            logging.info("Created playlists table")
        except:
            self.raise_table_not_created("playlists", "unable to create table")

    def create_playlists_songs_table(self) -> bool:
        """
        create_playlists_songs_table Creates the playlists_songs table in the database.

        Returns:
            bool: True if successful, False if not.
        """
        try:
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
        except:
            self.raise_table_not_created(
                "playlists_songs", "unable to create table")

    def create_song_artists_table(self):
        """
        create_song_artists_table Creates the song_artists table in the database.
        """
        try:
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
        except:
            self.raise_table_not_created(
                "song_artists", "unable to create table")

    def create_album_artists_table(self):
        """Create the album_artists table, returns True if successful, False if not."""
        try:
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
        except:
            self.raise_table_not_created(
                "album_artists", "unable to create table")

    def create_composers_table(self) -> bool:
        """
        create_composers_table Creates the composers table in the database.

        Returns:
            bool: True if successful, False if not.
        """
        try:
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
        except:
            self.raise_table_not_created("composers", "unable to create table")

    def create_genres_table(self):
        """
        create_genres_table Creates the genres table in the database.
        """
        try:
            # Song_id is a foreign key to the songs table
            logging.info("Creating genres table")
            cursor = self.conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS genres (
                    genre_name TEXT NOT NULL,
                    song_id INTEGER NOT NULL,
                    dt_added TEXT NOT NULL
                );"""
            )
            self.conn.commit()
            logging.info("Created genres table")
        except:
            self.raise_table_not_created("genres", "unable to create table")

    def create_all_tables(self):
        """Create all the tables, returns True if successful, False if not."""
        logging.info("Creating all tables")
        self.create_songs_table()
        self.create_plays_table()
        self.create_playlists_table()
        self.create_playlists_songs_table()
        self.create_song_artists_table()
        self.create_album_artists_table()
        self.create_composers_table()
        self.create_genres_table()
        logging.info("Created all tables")


    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                                          DELETE TABLES & INFO  
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    def clear_songs_table(self):
        """
        clear_songs_table Clears the songs table in the database.
        """
        logging.info("Clearing songs table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM songs;")
        self.conn.commit()
        logging.info("Cleared songs table")

    def clear_plays_table(self):
        """
        clear_plays_table Clears the plays table in the database.
        """
        logging.info("Clearing plays table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM plays;")
        self.conn.commit()
        logging.info("Cleared plays table")

    def clear_playlists_table(self):
        """
        clear_playlists_table Clears the playlists table in the database.
        """
        logging.info("Clearing playlists table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM playlists;")
        self.conn.commit()
        logging.info("Cleared playlists table")

    def clear_playlists_songs_table(self):
        """
        clear_playlists_songs_table Clears the playlists_songs table in the database.
        """
        logging.info("Clearing playlists_songs table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM playlists_songs;")
        self.conn.commit()
        logging.info("Cleared playlists_songs table")

    def clear_song_artists_table(self):
        """
        clear_song_artists_table Clears the song_artists table in the database.
        """
        logging.info("Clearing song_artists table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM song_artists;")
        self.conn.commit()
        logging.info("Cleared song_artists table")

    def clear_album_artists_table(self):
        """
        clear_album_artists_table Clears the album_artists table in the database.
        """
        logging.info("Clearing album_artists table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM album_artists;")
        self.conn.commit()
        logging.info("Cleared album_artists table")

    def clear_composers_table(self):
        """
        clear_composers_table Clears the composers table in the database.
        """
        logging.info("Clearing composers table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM composers;")
        self.conn.commit()
        logging.info("Cleared composers table")

    def clear_genres_table(self):
        """
        clear_genres_table Clears the genres table in the database.
        """
        logging.info("Clearing genres table")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM genres;")
        self.conn.commit()
        logging.info("Cleared genres table")

        
    def clear_all_tables(self) -> bool:
        """Clear all the tables, returns True if successful, False if not."""
        logging.info("Clearing all tables")
        self.clear_songs_table()
        self.clear_plays_table()
        self.clear_playlists_table()
        self.clear_playlists_songs_table()
        self.clear_song_artists_table()
        self.clear_album_artists_table()
        self.clear_composers_table()
        self.clear_genres_table()
        logging.info("Cleared all tables")
        return True

    def delete_database(self) -> bool:
        """Delete the database, returns True if successful, False if not.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info("Deleting database")
        os.remove(config.DATABASE_PATH)
        logging.info("Deleted database")
        return True

    def delete_song_by_id(self, song_id: int) -> bool:
        """Delete a song from the database by its ID.

        Args:
            song_id (int): ID of the song to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting song by ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM songs WHERE song_id = ?;""",
            (song_id,)
        )
        self.conn.commit()
        logging.info(f"Deleted song by ID: {song_id}")
        return True

    def delete_playlist_by_id(self, playlist_id: int) -> bool:
        """Delete a playlist from the database by its ID.

        Args:
            playlist_id (int): ID of the playlist to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting playlist by ID: {playlist_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM playlists WHERE playlist_id = ?;""",
            (playlist_id,)
        )
        self.conn.commit()
        logging.info(f"Deleted playlist by ID: {playlist_id}")
        return True

    def delete_playlist_by_name(self, playlist_name: str) -> bool:
        """Delete a playlist from the database by its name.

        Args:
            playlist_name (str): Name of the playlist to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting playlist by name: {playlist_name}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM playlists WHERE playlist_name = ?;""",
            (playlist_name,)
        )
        self.conn.commit()
        logging.info(f"Deleted playlist by name: {playlist_name}")
        return True

    def delete_playlist_song_by_id(self, playlist_id: int, song_id: int) -> bool:
        """Delete a song from a playlist by its ID.

        Args:
            playlist_id (int): ID of the playlist to delete the song from.
            song_id (int): ID of the song to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting song from playlist by ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM playlists_songs WHERE playlist_id = ? AND song_id = ?;""",
            (playlist_id, song_id)
        )
        self.conn.commit()
        logging.info(f"Deleted song from playlist by ID: {song_id}")
        return True

    def delete_playlist_song_by_name(self, playlist_name: str, song_name: str) -> bool:
        """Delete a song from a playlist by its name.

        Args:
            playlist_name (str): Name of the playlist to delete the song from.
            song_name (str): Name of the song to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting song from playlist by name: {song_name}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM playlists_songs WHERE playlist_id = (SELECT playlist_id FROM playlists WHERE playlist_name = ?) AND song_id = (SELECT song_id FROM songs WHERE song_name = ?);""",
            (playlist_name, song_name)
        )
        self.conn.commit()
        logging.info(f"Deleted song from playlist by name: {song_name}")
        return True

    def delete_playlist_song_by_playlist_id_song_id(self, playlist_id: int, song_id: int) -> bool:
        """Delete a song from a playlist by its ID.

        Args:
            playlist_id (int): ID of the playlist to delete the song from.
            song_id (int): ID of the song to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting song from playlist by ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM playlists_songs WHERE playlist_id = ? AND song_id = ?;""",
            (playlist_id, song_id)
        )
        self.conn.commit()
        logging.info(f"Deleted song from playlist by ID: {song_id}")
        return True

    def delete_song_artist_by_artist_song_id(self, artist_id: int, song_id: int) -> bool:
        """Delete a song from a playlist by its ID.

        Args:
            artist_id (int): ID of the artist to delete the song from.
            song_id (int): ID of the song to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting song from artist by ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM songs_artists WHERE artist_id = ? AND song_id = ?;""",
            (artist_id, song_id)
        )
        self.conn.commit()
        logging.info(f"Deleted song from artist by ID: {song_id}")
        return True

    def delete_album_artist_by_artist_album_id(self, artist_id: int, album_id: int) -> bool:
        """Delete an album from an artist by its ID.

        Args:
            artist_id (int): ID of the artist to delete the album from.
            album_id (int): ID of the album to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting album from artist by ID: {album_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM albums_artists WHERE artist_id = ? AND album_id = ?;""",
            (artist_id, album_id)
        )
        self.conn.commit()
        logging.info(f"Deleted album from artist by ID: {album_id}")
        return True

    def delete_composer_by_name_song_id(self, composer_name: str, song_id: int) -> bool:
        """Delete a composer from a song by its name.

        Args:
            composer_name (str): Name of the composer to delete the song from.
            song_id (int): ID of the song to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting composer from song by name: {composer_name}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM songs_composers WHERE composer_id = (SELECT composer_id FROM composers WHERE composer_name = ?) AND song_id = ?;""",
            (composer_name, song_id)
        )
        self.conn.commit()
        logging.info(f"Deleted composer from song by name: {composer_name}")
        return True

    def delete_genre_by_name_song_id(self, genre_name: str, song_id: int) -> bool:
        """Delete a genre from a song by its name.

        Args:
            genre_name (str): Name of the genre to delete the song from.
            song_id (int): ID of the song to delete.

        Returns:
            bool: True if successful, False if not.
        """
        logging.info(f"Deleting genre from song by name: {genre_name}")
        cursor = self.conn.cursor()
        cursor.execute(
            """DELETE FROM songs_genres WHERE genre_id = (SELECT genre_id FROM genres WHERE genre_name = ?) AND song_id = ?;""",
            (genre_name, song_id)
        )
        self.conn.commit()
        logging.info(f"Deleted genre from song by name: {genre_name}")
        return True
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                                    RETRIEVE DATA INDIVIDUAL
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    def get_song_by_id(self, song_id: int) -> List[dict]:
        """
        get_song_by_id Searches the song table for a song with the given ID.

        Args:
            song_id (int): ID of the song to search for.

        Returns:
            List[dict]: List of dictionaries containing the song data.
        """

        logging.info(f"Getting song by ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM songs WHERE song_id = ?;""",
            (song_id,)
        )
        song = cursor.fetchone()

        song_table_data = {
            "filepath": None,  # string
            "main_artist": None,  # string
            "filesize": None,  # int in bytes
            "padding": None,  # int in bytes
            "album_artwork_bit_depth": None,  # int in bits
            "album_artwork_colors": None,  # int
            "album_artwork_height": None,  # int in pixels
            "album_artwork_width": None,  # int in pixels
            "bit_depth": None,  # int in bits
            "bitrate": None,  # int in bits, divide by 1000 to get Kbps
            "channels": None,  # int
            "duration": None,  # int in seconds
            "sample_rate": None,  # int in KHz
            "album": None,  # string
            "barcode": None,  # string
            "date_created": None,  # string in YYYY-MM-DD
            "disc_number": None,  # int
            "disc_total": None,  # int
            "genre": None,  # string
            "isrc": None,  # string
            "itunesadvisory": None,  # string
            "length": None,  # int
            "publisher": None,  # string
            "rating": None,  # int
            "title": None,  # string
            "track_number": None,  # int
            "track_total": None,  # int
            "source": None,  # string 
        }
        if song is None:
            return None

        song_table_data["filepath"] = song[1]
        song_table_data["filesize"] = song[2]
        song_table_data["padding"] = song[3]
        song_table_data["album_artwork_bit_depth"] = song[4]
        song_table_data["album_artwork_colors"] = song[5]
        song_table_data["album_artwork_height"] = song[6]
        song_table_data["album_artwork_width"] = song[7]
        song_table_data["bit_depth"] = song[8]
        song_table_data["bitrate"] = song[9]
        song_table_data["channels"] = song[10]
        song_table_data["duration"] = song[11]
        song_table_data["sample_rate"] = song[12]
        song_table_data["album"] = song[13]
        song_table_data["barcode"] = song[14]
        song_table_data["date_created"] = song[15]
        song_table_data["disc_number"] = song[16]
        song_table_data["disc_total"] = song[17]
        song_table_data["isrc"] = song[18]
        song_table_data["itunesadvisory"] = song[19]
        song_table_data["length"] = song[20]
        song_table_data["publisher"] = song[21]
        song_table_data["rating"] = song[22]
        song_table_data["title"] = song[23]
        song_table_data["track_number"] = song[24]
        song_table_data["track_total"] = song[25]
        song_table_data["source"] = song[26]
        song_table_data["main_artist"] = song[27]

        return song_table_data

    def get_song_id_by_title_filesize(self, title: str, filesize: int) -> int:
        """
        get_song_id_by_title_filesize Searches the database to find the song ID by title and filesize. 
        You want to use filesize because they're basically gurenteed to be unique.

        Args:
            title (str): Title of Song
            filesize (int): Filesize of song (get these from the song object)

        Returns:
            int: song_id of the song
        """

        logging.info(
            f"Getting song by title and filesize: {title}, {filesize}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM songs WHERE title = ? AND filesize = ?;""",
            (title, filesize)
        )
        # return the id of the song
        song = cursor.fetchone()
        if song is None:
            return None
        logging.info(f"Got song by title and filesize: {title}, {filesize}")
        return song[0]

    def get_songs_in_playlist(self, playlist_name: str) -> List[dict]:
        """
        get_songs_in_playlist Returns a list of all the songs in a given playlist

        Args:
            playlist_name (str): Name of the playlist to get songs from

        Returns:
            List[dict]: List of dictionaries containing the song data.
        """

        logging.info(f"Getting songs in playlist: {playlist_name}")

        playlist_id = self.get_playlist_id_by_name(playlist_name)

        # GET SONG IDS from playlists_songs table then look up songs in songs table
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM playlists_songs WHERE playlist_id = ?;""",
            (playlist_id,)
        )
        playlist_songs = cursor.fetchall()
        songs = []
        for playlist_song in playlist_songs:
            song_id = playlist_song[1]
            song = self.get_song_by_id(song_id)
            songs.append(song)
        logging.info(f"Got songs in playlist: {playlist_name}")

        return songs

    def get_playlist_id_by_name(self, playlist_name: str) -> int:
        """
        get_playlist_id_by_name Get ID of playlist by name.

        Args:
            playlist_name (str): Name of playlist

        Returns:
            int: ID of playlist
        """

        logging.info(f"Getting playlist by name: {playlist_name}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM playlists WHERE playlist_name = ?;""",
            (playlist_name,)
        )
        playlist = cursor.fetchone()
        if playlist is None:
            return None
        logging.info(f"Got playlist by name: {playlist_name}")
        return playlist[0]

    def get_playlist_by_id(self, playlist_id: int) -> tuple:
        """
        get_playlist_by_id Get playlist by ID.

        Args:
            playlist_id (int): ID of playlist

        Returns:
            tuple: playlist object
        """

        logging.info(f"Getting playlist by ID: {playlist_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM playlists WHERE playlist_id = ?;""",
            (playlist_id,)
        )
        playlist = cursor.fetchone()
        logging.info(f"Got playlist by ID: {playlist_id}")
        return playlist

    def get_song_album_artists(self, song_id: int) -> List[str]:
        """
        get_song_album_artists Get all the album artists of a song, returns a list of names.

        Args:
            song_id (int): ID of song

        Returns:
            List[str]: list of names of album artists
        """

        logging.info(f"Getting song album artists by song ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM album_artists WHERE song_id = ?;""",
            (song_id,)
        )
        album_artists = cursor.fetchall()
        logging.info(f"Got song album artists by song ID: {song_id}")
        return album_artists

    def get_song_composers(self, song_id: int) -> List[str]:
        """
        get_song_composers Get all the composers of a song, returns a list of names.

        Args:
            song_id (int): ID of song

        Returns:
            List[str]: list of names of composers
        """

        logging.info(f"Getting song composers by song ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM composers WHERE song_id = ?;""",
            (song_id,)
        )
        composers = cursor.fetchall()
        logging.info(f"Got song composers by song ID: {song_id}")
        return composers

    def get_song_artists(self, song_id: int) -> List[str]:
        """
        get_song_artists Get all the artists of a song, returns a list of names of Artists.

        Args:
            song_id (int): ID of song

        Returns:
            List[str]: list of names of artists
        """

        logging.info(f"Getting song artists by song ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM artists WHERE song_id = ?;""",
            (song_id,)
        )
        artists = cursor.fetchall()
        logging.info(f"Got song artists by song ID: {song_id}")
        return artists

    def get_song_genres(self, song_id: int) -> List[str]:
        """
        get_song_genres Get all the genres of a song, returns a list of names of genres.

        Args:
            song_id (int): ID of song

        Returns:
            List[str]: list of names of genres
        """

        logging.info(f"Getting song genres by song ID: {song_id}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM genres WHERE song_id = ?;""",
            (song_id,)
        )
        genres = cursor.fetchall()
        logging.info(f"Got song genres by song ID: {song_id}")
        return genres

    def get_play_information_from_song_id(self, song_id: int) -> Dict[str, int]:
        """
        get_play_information_from_song_id Get play information from song ID. This is the song_title, song_primary_artist, and filesize

        Args:
            song_id (int): ID of song

        Returns:
            Dict[str, int]: Dictionary of song_title, song_primary_artist, and filesize
        """        

        logging.info(f"Getting play information for song ID: {song_id}")

        song_raw = self.get_song_by_id(song_id)
        song_values = {
            "song_title": song_raw["title"],
            "song_primary_artist": song_raw["main_artist"],
            "filesize": song_raw["filesize"]
        }

        logging.info(f"Got play information for song ID: {song_id}")
        return song_values

    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                                    RETRIEVE DATA MULTIPLE
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    def get_all_tables(self) -> List[str]:
        """
        get_all_tables Get all the tables in the database, returns a list of table names.

        Returns:
            List[str]: list of table names
        """

        logging.info("Getting all tables")
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logging.info("Got all tables")
        return tables

    def get_all_songs(self) -> List[dict]:
        """
        get_all_songs Get all the songs in the database, returns a list of Song objects

        Returns:
            List[dict]: list of dictionaries
        """

        logging.info("Getting all songs")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM songs;")
        songs = cursor.fetchall()
        logging.info("Got all songs")
        return songs

    def get_all_plays(self) -> List[dict]:
        """
        get_all_plays Get all the plays in the database, returns a list of the plays

        Returns:
            List[dict]: list of dictionaries
        """

        logging.info("Getting all plays")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM plays;")
        plays = cursor.fetchall()
        logging.info("Got all plays")
        return plays

    def get_all_song_artists(self) -> List[str]:
        """
        get_all_song_artists Get all the song artists in the database, returns a list of strings

        Returns:
            List[str]: list of strings
        """

        # artists can be duplicated, so we need to remove duplicates from song_artists
        logging.info("Getting all song artists")
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT artist_name FROM song_artists;")
        song_artists = cursor.fetchall()
        logging.info("Got all song artists")
        song_artists = [artist[0] for artist in song_artists]
        return song_artists

    def get_all_album_artists(self) -> List[str]:
        """
        get_all_album_artists Get all the album artists in the database, returns a list of strings

        Returns:
            List[str]: list of strings
        """

        # artists can be duplicated, so we need to remove duplicates from album_artists
        logging.info("Getting all album artists")
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT artist_name FROM album_artists;")
        album_artists = cursor.fetchall()
        logging.info("Got all album artists")
        album_artists = [artist[0] for artist in album_artists]
        return album_artists

    def get_all_composers(self) -> List[str]:
        """
        get_all_composers Get all the composers in the database, returns a list of strings

        Returns:
            List[str]: list of strings
        """

        # composers can be duplicated, so we need to remove duplicates from composers
        logging.info("Getting all composers")
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT composer_name FROM composers;")
        composers = cursor.fetchall()
        logging.info("Got all composers")
        composers = [composer[0] for composer in composers]
        return composers

    def get_all_genres(self) -> List[str]:
        """
        get_all_genres Get all the genres in the database, returns a list of strings

        Returns:
            List[str]: list of strings
        """

        # genres can be duplicated, so we need to remove duplicates from genres
        logging.info("Getting all genres")
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT genre_name FROM genres;")
        genres = cursor.fetchall()
        logging.info("Got all genres")
        genres = [genre[0] for genre in genres]
        return genres

    def get_all_playlist_names(self) -> List[str]:
        """
        get_all_playlist_names Get all the playlist names in the database, returns a list of strings

        Returns:
            List[str]: list of strings
        """

        logging.info("Getting all playlist names")
        cursor = self.conn.cursor()
        cursor.execute("SELECT playlist_name FROM playlists;")
        playlist_names = cursor.fetchall()

        # remove the tuple from each playlist name
        playlist_names = [playlist_name[0] for playlist_name in playlist_names]
        logging.info("Got all playlist names")
        return playlist_names

    def get_all_playlist_songs(self) -> List[dict]:
        """
        get_all_playlist_songs Get all the playlist songs in the database, returns a list of dictionaries

        Returns:
            List[dict]: list of dictionaries [song_name, file_size, id]
        """

        playlist_names = self.get_all_playlist_names()
        playlist_songs = {}
        for playlist_name in playlist_names:
            # we only want the song_name, file_size, and id
            songs = self.get_songs_in_playlist(playlist_name)
            playlist_values = []
            for song_data in songs:
                print(song_data)
                song_values = {
                    "song_name": song_data["title"],
                    "file_size": song_data["filesize"],
                }

                song_id = self.get_song_id_by_title_filesize(
                    song_values["song_name"], song_values["file_size"])
                song_values["id"] = song_id
                playlist_values.append(song_values)

            playlist_songs[playlist_name] = playlist_values
        return playlist_songs

    def get_all_songs_in_genre(self, genre_name: str) -> List[dict]:
        """
        get_all_songs_in_genre Get all the songs in a genre, returns a list of dictionaries

        Args:
            genre_name (str): Name of the genre

        Returns:
            List[dict]: list of dictionaries
        """
            
        logging.info("Getting all songs in genre {}".format(genre_name))
        cursor = self.conn.cursor()

        # get all song_id that matches the given genre_name in the genres table
        
        cursor.execute(
            "SELECT song_id FROM genres WHERE genre_name = ?;", (genre_name,))
        song_ids = cursor.fetchall()
        song_ids = [song_id[0] for song_id in song_ids]

        # get all the songs that match the song_ids
        songs = []
        for song_id in song_ids:
            song_data = self.get_song_by_id(song_id)
            songs.append(song_data)

        logging.info("Got all songs in genre {}".format(genre_name))
        return songs

    def get_all_columns_from_table(self, table_name: str) -> List[str]:
        """
        get_all_columns_from_table Get all the columns from a table, returns a list of strings

        Args:
            table_name (str): Name of the table

        Returns:
            List[str]: list of strings
        """

        logging.info("Getting all columns from table {}".format(table_name))
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info({});".format(table_name))
        columns = cursor.fetchall()
        columns = [column[1] for column in columns]
        logging.info("Got all columns from table {}".format(table_name))
        return columns
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                                    INSERT DATA
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    # play table: song_title, song_primary_artist, filesize, start_dt, end_dt
    def insert_play(self, song_title: str, song_primary_artist: str, filesize: int, start_dt: str, end_dt: str) -> bool:
        """
        insert_play Insert a play into the plays table

        Args:
            song_title (str): Title of the song
            song_primary_artist (str): Primary artist of the song
            filesize (int): Filesize of the song
            start_dt (str): Date the song started playing
            end_dt (str): Date the song ended playing

        Returns:
            bool: True if successful, False if not
        """


        # plays table has auto incrementing id, so we don't need to insert the id
        logging.info("Inserting play into plays table")
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO plays (song_title, song_primary_artist, filesize, start_dt, end_dt) VALUES (?, ?, ?, ?, ?);",
            (song_title, song_primary_artist, filesize, start_dt, end_dt))
        self.conn.commit()
        logging.info("Inserted play into plays table")
        return True

    def insert_playlist(self, playlist_name: str, playlist_desc: str, created_dt: str) -> bool:
        """
        insert_playlist Insert a playlist into the playlists table. Only inserts if the playlist does not already exist

        Args:
            playlist_name (str): Name of the playlist
            playlist_desc (str): Description of the playlist
            created_dt (str): Date the playlist was created

        Returns:
            bool: True if successful, False if not
        """
        
        # check if the playlist already exists
        if self.get_playlist_id_by_name(playlist_name) is not None:
            logging.info("Playlist {} already exists".format(playlist_name))
            return False

        logging.info("Inserting playlist {} into playlists table".format(playlist_name))
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO playlists (playlist_name, playlist_desc, created_dt) VALUES (?, ?, ?);", (playlist_name, playlist_desc, created_dt))
        self.conn.commit()
        return True

    def insert_playlist_song(self, playlist_name: str, song_id: int) -> bool:
        """
        insert_playlist_song Inserts a song into a playlist. Adds a record to the playlists_songs table

        Args:
            playlist_name (str): Name of the playlist
            song_id (int): ID of the song

        Returns:
            bool: True if successful, False if not
        """
        logging.info(
            "Inserting playlist_song {} into playlists_songs table".format(playlist_name))

        playlist_id = self.get_playlist_id_by_name(playlist_name)
        added_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.conn.cursor()
        # duplicates are ok

        cursor.execute(
            """INSERT INTO playlists_songs (playlist_id, song_id, added_dt)
            VALUES (?, ?, ?);""",
            (playlist_id, song_id, added_dt)
        )
        self.conn.commit()
        logging.info(
            "Inserted playlist_song {} into playlists_songs table".format(playlist_name))
        return True

    def insert_song(self, **kwargs) -> int:
        """
        insert_song Insert a song into the songs table, returns song_id of inserted song.
        Only insert if the song does not already exist. Use the title and filesize.

        Args:
            **kwargs: song_table_data (dict)

        Returns:
            int: song_id of inserted song
        """
        logging.info(
            "Inserting song {} into songs table".format(kwargs["title"]))
        cursor = self.conn.cursor()
        # self.song_table_data = {
        #     "filepath": "N/A", # string
        #     "main_artist": "N/A", # string
        #     "filesize": -1, # in bytes
        #     "padding": -1, # in bytes
        #     "album_artwork_bit_depth": -1, # in bits
        #     "album_artwork_colors": -1, # int
        #     "album_artwork_height": -1, # in pixels
        #     "album_artwork_width": -1, # in pixels
        #     "bit_depth": -1, # in bits
        #     "bitrate": -1, # in bits, divide by 1000 to get Kbps
        #     "channels": -1, # int
        #     "duration": -1, # in seconds
        #     "sample_rate": -1, # in KHz
        #     "album": "N/A", # string
        #     "barcode": "N/A", # string
        #     "date_created": "N/A", # in YYYY-MM-DD
        #     "disc_number": -1, # int
        #     "disc_total": -1, # int
        #     "isrc": "N/A", # string
        #     "itunesadvisory": "N/A", # string
        #     "length": -1, # int
        #     "publisher": "N/A", # string
        #     "rating": -1, # int
        #     "title": "N/A", # string
        #     "track_number": -1, # int
        #     "track_total": -1, # int
        #     "source": "N/A", # string
        # }

        # check if song already exists
        song_id = self.get_song_id_by_title_filesize(
            kwargs["title"], kwargs["filesize"])
        if song_id:
            logging.warning("Song {} already exists in songs table".format(
                kwargs["title"]))
            return song_id
        cursor.execute(
            """INSERT INTO songs (
                filepath,
                main_artist,
                filesize,
                padding,
                album_artwork_bit_depth,
                album_artwork_colors,
                album_artwork_height,
                album_artwork_width,
                bit_depth,
                bitrate,
                channels,
                duration,
                sample_rate,
                album,
                barcode,
                date_created,
                disc_number,
                disc_total,
                isrc,
                itunesadvisory,
                length,
                publisher,
                rating,
                title,
                track_number,
                track_total,
                source
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );""",
            (
                kwargs["filepath"],
                kwargs["main_artist"],
                kwargs["filesize"],
                kwargs["padding"],
                kwargs["album_artwork_bit_depth"],
                kwargs["album_artwork_colors"],
                kwargs["album_artwork_height"],
                kwargs["album_artwork_width"],
                kwargs["bit_depth"],
                kwargs["bitrate"],
                kwargs["channels"],
                kwargs["duration"],
                kwargs["sample_rate"],
                kwargs["album"],
                kwargs["barcode"],
                kwargs["date_created"],
                kwargs["disc_number"],
                kwargs["disc_total"],
                kwargs["isrc"],
                kwargs["itunesadvisory"],
                kwargs["length"],
                kwargs["publisher"],
                kwargs["rating"],
                kwargs["title"],
                kwargs["track_number"],
                kwargs["track_total"],
                kwargs["source"],
            )
        )

        self.conn.commit()
        # get the song_id of the inserted song
        cursor.execute(
            """SELECT song_id FROM songs WHERE filepath = ?;""",
            (kwargs["filepath"],)
        )

        song_id = cursor.fetchone()[0]
        song_name = kwargs["title"]
        logging.info(f"Inserted {song_name} with song_id: {song_id}")
        return song_id

    def insert_album_artist(self, artist_name, song_id) -> bool:
        """
        insert_album_artist Insert an album_artist into the database, returns True if successful, False if not. Only insert if the album_artist does not already exist

        Args:
            artist_name (_type_): name of the album artist
            song_id (_type_): song_id of the song

        Returns:
            bool: True if successful, False if not
        """
        logging.info("Attempting to insert album artist {} iwith song_id {} into album_artists table".format(
            artist_name, song_id))
        cursor = self.conn.cursor()
        # check if album_artist already exists
        cursor.execute(
            """SELECT 1 FROM album_artists WHERE artist_name = ? AND song_id = ?;""",
            (artist_name, song_id)
        )

        if cursor.fetchone():
            logging.warning("Album artist {} with song_id {} already exists in album_artists table".format(
                artist_name, song_id))
            return False

        cursor.execute(
            """INSERT INTO album_artists (artist_name, song_id, dt_added)
            VALUES (?, ?, ?);""",
            (artist_name, song_id, datetime.datetime.now())
        )

        self.conn.commit()
        logging.info("Inserted album artist {} with song_id {} into album_artists table".format(
            artist_name, song_id))

        return True

    def insert_song_artist(self, artist_name, song_id) -> bool:
        """
        insert_song_artist Insert a song_artist into the database, returns True if successful, False if not. Only insert if the song_artist does not already exist

        Args:
            artist_name (_type_): name of the song artist
            song_id (_type_): song_id of the song

        Returns:
            bool: True if successful, False if not
        """

        logging.info("Attempting to insert song artist {} with song_id {} into song_artists table".format(
            artist_name, song_id))
        cursor = self.conn.cursor()
        # cursor.execute(
        #     """INSERT INTO song_artists (artist_name, song_id, dt_added)
        #     SELECT ?, ?, ? WHERE NOT EXISTS (
        #         SELECT 1 FROM song_artists WHERE artist_name = ? AND song_id = ?
        #     );""",
        #     (artist_name, song_id, datetime.datetime.now(), artist_name, song_id)
        # )

        # check if song_artist already exists
        cursor.execute(
            """SELECT 1 FROM song_artists WHERE artist_name = ? AND song_id = ?;""",
            (artist_name, song_id)
        )

        if cursor.fetchone():
            logging.warning("Song artist {} with song_id {} already exists in song_artists table".format(
                artist_name, song_id))
            return False

        cursor.execute(
            """INSERT INTO song_artists (artist_name, song_id, dt_added)
            VALUES (?, ?, ?);""",
            (artist_name, song_id, datetime.datetime.now())
        )

        self.conn.commit()
        logging.info("Inserted song artist {} with song_id {} into song_artists table".format(
            artist_name, song_id))
        return True

    def insert_composer(self, composer_name, song_id) -> bool:
        """
        insert_composer Insert a composer into the database, returns True if successful, False if not. 
        Only insert if the composer does not already exist

        Args:
            composer_name (_type_): name of the composer
            song_id (_type_): song_id of the song

        Returns:
            bool: True if successful, False if not
        """
        logging.info("Attempting to insert composer {} with song_id {} into composers table".format(
            composer_name, song_id))
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT 1 FROM composers WHERE composer_name = ? AND song_id = ?;""",
            (composer_name, song_id)
        )

        if cursor.fetchone():
            logging.warning("Composer {} with song_id {} already exists in composers table".format(
                composer_name, song_id))
            return False

        cursor.execute(
            """INSERT INTO composers (composer_name, song_id, dt_added)
            VALUES (?, ?, ?);""",
            (composer_name, song_id, datetime.datetime.now())
        )

        self.conn.commit()
        logging.info("Inserted composer {} with song_id {} into composers table".format(
            composer_name, song_id))
        return True

    def insert_genre(self, genre_name, song_id) -> bool:
        """Insert a genre into the database, returns True if successful, False if not. Only insert if the genre does not already exist."""
        logging.warning("Inserting genre {} with song_id {} into genres table".format(
            genre_name, song_id))
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT 1 FROM genres WHERE genre_name = ? AND song_id = ?;""",
            (genre_name, song_id)
        )

        if cursor.fetchone():
            logging.info("Genre {} with song_id {} already exists in genres table".format(
                genre_name, song_id))
            return False

        cursor.execute(
            """INSERT INTO genres (genre_name, song_id, dt_added)
            VALUES (?, ?, ?);""",
            (genre_name, song_id, datetime.datetime.now())
        )

        self.conn.commit()
        logging.info("Inserted genre {} with song_id {} into genres table".format(
            genre_name, song_id))
        return True

    # IMPORTANT: FUNCTION BELOW!

    def populate_database(self):
        """
        populate_database Populate the database using the data from the soundfiles in the SOUNDFILES_PATH directory
        """

        # fetch all the files from config.SOUNDFILES_PATH
        soundfiles = os.listdir(config.SOUNDFILES_PATH)

        for file in soundfiles:
            # get path of file
            file_path = os.path.join(config.SOUNDFILES_PATH, file)

            # get metadata from file
            parser = songparser.SongMetadata(filepath=file_path)

            # get the song data and insert it into the database
            song_data = parser.get_song_table_data()
            print(song_data, file)
            song_id = None
            if song_data is not None:
                print(song_data['barcode'])
                song_id = self.insert_song(**song_data)
            else:
                logging.error(f"Could not get song data for file: {file_path}")
                continue

            # get the artist data and insert it into the database
            album_artist_data = parser.get_album_artist_data()
            if album_artist_data is not None:
                for artist in album_artist_data:
                    self.insert_album_artist(artist, song_id)

            song_artist_data = parser.get_song_artist_data()
            if song_artist_data is not None:
                for artist in song_artist_data:
                    self.insert_song_artist(artist, song_id)

            composer_data = parser.get_composer_data()
            if composer_data is not None:
                for composer in composer_data:
                    self.insert_composer(composer, song_id)

            genre_data = parser.get_genre_data()
            if genre_data is not None:
                for genre in genre_data:
                    self.insert_genre(genre, song_id)

    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    #                                  Backup and Restore
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------

    def backup_database(self) -> bool:
        """
        backup_database Backup the database to the path specified in config.DATABASE_BACKUP_PATH

        Returns:
            bool: True if successful, False if not
        """
        logging.info("Backing up database")

        # Zip the database file and name it with the current date
        # then move it to config.DATABASE_BACKUP_PATH
        # database is at config.DATABASE_PATH

        with zipfile.ZipFile(f"{config.DATABASE_BACKUP_PATH}/{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.zip", 'w') as zip:
            zip.write(config.DATABASE_PATH, arcname="analytics.db")

        logging.info("Backed up database")
        return True


def init_db():
    # create an instance of the database handler
    db_handler = AnalyticsDBHandler()
    db_handler.create_all_tables()


if __name__ == "__main__":

    db_handler = AnalyticsDBHandler()
    db_handler.create_all_tables()
    db_handler.populate_database()
    # db_handler.populate_database()