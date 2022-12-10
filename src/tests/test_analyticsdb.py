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

import songparser
import analyticsdb
import config

# unzip the test database in config.ZIPPED_DATABASE_TEST_PATH

dbHelper = analyticsdb.AnalyticsDBHandler(debug_path=config.DATABASE_TEST_PATH)


def setup_prezipped_db():
    with zipfile.ZipFile(config.ZIPPED_DATABASE_TEST_PATH, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(config.DATABASE_TEST_PATH))


song_table_dict = {
    "filepath": "N/A",  # string
    "main_artist": "N/A",  # string
    "filesize": -1,  # in bytes
    "padding": -1,  # in bytes
    "album_artwork_bit_depth": -1,  # in bits
    "album_artwork_colors": -1,  # int
    "album_artwork_height": -1,  # in pixels
    "album_artwork_width": -1,  # in pixels
    "bit_depth": -1,  # in bits
    "bitrate": -1,  # in bits, divide by 1000 to get Kbps
    "channels": -1,  # int
    "duration": -1,  # in seconds
    "sample_rate": -1,  # in KHz
    "album": "N/A",  # string
    "barcode": "N/A",  # string
    "date_created": "N/A",  # in YYYY-MM-DD
    "disc_number": -1,  # int
    "disc_total": -1,  # int
    "genre": "N/A",  # string
    "isrc": "N/A",  # string
    "itunesadvisory": "N/A",  # string
    "length": -1,  # int
    "publisher": "N/A",  # string
    "rating": -1,  # int
    "title": "N/A",  # string
    "track_number": -1,  # int
    "track_total": -1,  # int
    "source": "N/A",  # string
}


def setup_test_db():
    # create a test database
    # dbHelper.clear_all_tables()
    dbHelper.create_all_tables()
    dbHelper.populate_database()

    # lets make some example playlists
    # def insert_playlist(self, playlist_name: str, playlist_desc: str, created_dt: str) -> bool:
    dbHelper.insert_playlist(
        "test_playlist_1", "test playlist 1 description", "2020-01-01")
    dbHelper.insert_playlist(
        "favorites", "test playlist 2 description", "2020-01-02")

    # lets make some example songs
    # def insert_playlist_song(self, playlist_name: str, song_id: int) -> bool:

    # THESE NEED TO BE COMMENTED OTHERWISE THEY WILL RE-INSERT THE SAME SONGS. UNCOMMENT TO RE-CREATE DATABASE

    dbHelper.insert_playlist_song("test_playlist_1", 1)
    dbHelper.insert_playlist_song("test_playlist_1", 2)
    dbHelper.insert_playlist_song("test_playlist_1", 3)
    dbHelper.insert_playlist_song("favorites", 1)
    dbHelper.insert_playlist_song("favorites", 2)
    dbHelper.insert_playlist_song("favorites", 3)
    dbHelper.insert_playlist_song("favorites", 19)

    # lets add some example plays

    # lets get the song table to look at the song_title, song_primary_artist, filesize

    # def get_play_information_from_song_id(self, song_id: int) -> Dict[str, int]:

    songs_info = []
    for i in range(1, 18):
        songs_info.append(dbHelper.get_play_information_from_song_id(i))

    # add some plays using this info
    # def insert_play(self, song_title: str, song_primary_artist: str, filesize: int, start_dt: str, end_dt: str) -> bool:
    for i in range(0, 50):
        # randomly pick a song
        song = random.choice(songs_info)
        # randomly pick a start time
        start_time = random.randint(0, 1000000000)
        # randomly pick an endtime up to 10 minutes after the start time
        end_time = random.randint(start_time, start_time + 600)
        # insert the play
        dbHelper.insert_play(
            song["song_title"], song["song_primary_artist"], song["filesize"], start_time, end_time)


def test_vital_paths():
    # check if ../analyticsdb ../backups ../logs exist
    assert os.path.exists(os.path.dirname(config.DATABASE_PATH))
    assert os.path.exists(config.BACKUPS_PATH)
    assert os.path.exists(os.path.dirname(config.LOGGING_FILENAME))
    assert os.path.exists(os.path.dirname(config.ZIPPED_DATABASE_TEST_PATH))

# --------------------------------------------------------------------------------
#                          TESTING CREATE TABLES
# --------------------------------------------------------------------------------

def test_create_songs_table():
    dbHelper.create_songs_table()
    # get all the columns from the songs table
    columns = dbHelper.get_all_columns_from_table("songs")
    assert columns == ['song_id', 'filepath', 'filesize', 'padding', 'album_artwork_bit_depth', 'album_artwork_colors', 'album_artwork_height', 'album_artwork_width', 'bit_depth', 'bitrate', 'channels', 'duration',
                       'sample_rate', 'album', 'barcode', 'date_created', 'disc_number', 'disc_total', 'isrc', 'itunesadvisory', 'length', 'publisher', 'rating', 'title', 'track_number', 'track_total', 'source', 'main_artist']

def test_create_plays_table():
    dbHelper.create_plays_table()
    # get all the columns from the plays table
    columns = dbHelper.get_all_columns_from_table("plays")
    assert columns == ['play_id', 'song_title', 'song_primary_artist', 'filesize', 'start_dt', 'end_dt']

def test_create_playlists_table():
    dbHelper.create_playlists_table()
    # get all the columns from the playlists table
    columns = dbHelper.get_all_columns_from_table("playlists")
    assert columns == ['playlist_id', 'playlist_name', 'playlist_desc', 'created_dt']

def test_create_playlist_songs_table():
    dbHelper.create_playlists_songs_table()
    # get all the columns from the playlist_songs table
    columns = dbHelper.get_all_columns_from_table("playlists_songs")
    print(columns)
    assert columns == ['playlist_id', 'song_id', 'added_dt']

def test_create_song_artists_table():
    dbHelper.create_song_artists_table()
    # get all the columns from the song_artists table
    columns = dbHelper.get_all_columns_from_table("song_artists")
    assert columns == ['artist_name', 'song_id', 'dt_added']

def test_create_album_artists_table():
    dbHelper.create_album_artists_table()
    # get all the columns from the album_artists table
    columns = dbHelper.get_all_columns_from_table("album_artists")
    assert columns == ['artist_name', 'song_id', 'dt_added']

def test_create_composers_table():
    dbHelper.create_composers_table()
    # get all the columns from the composers table
    columns = dbHelper.get_all_columns_from_table("composers")
    assert columns == ['composer_name', 'song_id', 'dt_added']

def test_create_genres_table():
    dbHelper.create_genres_table()
    # get all the columns from the genres table
    columns = dbHelper.get_all_columns_from_table("genres")
    assert columns == ['genre_name', 'song_id', 'dt_added']

# --------------------------------------------------------------------------------
#                          TESTING CLEAR TABLES
# --------------------------------------------------------------------------------

def test_clear_songs_table():
    dbHelper.clear_songs_table()
    # get all the columns from the songs table
    try:
        columns = dbHelper.get_all_columns_from_table("songs")
    except Exception as e:
        assert True

def test_clear_plays_table():
    dbHelper.clear_plays_table()
    # get all the columns from the plays table
    try:
        columns = dbHelper.get_all_columns_from_table("plays")
    except Exception as e:
        assert True

def test_clear_playlists_table():
    dbHelper.clear_playlists_table()
    # get all the columns from the playlists table
    try:
        columns = dbHelper.get_all_columns_from_table("playlists")
    except Exception as e:
        assert True

def test_clear_playlist_songs_table():
    dbHelper.clear_playlists_songs_table()
    # get all the columns from the playlist_songs table
    try:
        columns = dbHelper.get_all_columns_from_table("playlists_songs")
    except Exception as e:
        assert True

def test_clear_song_artists_table():
    dbHelper.clear_song_artists_table()
    # get all the columns from the song_artists table
    try:
        columns = dbHelper.get_all_columns_from_table("song_artists")
    except Exception as e:
        assert True

def test_clear_album_artists_table():
    dbHelper.clear_album_artists_table()
    # get all the columns from the album_artists table
    try:
        columns = dbHelper.get_all_columns_from_table("album_artists")
    except Exception as e:
        assert True

def test_clear_composers_table():
    dbHelper.clear_composers_table()
    # get all the columns from the composers table
    try:
        columns = dbHelper.get_all_columns_from_table("composers")
    except Exception as e:
        assert True

def test_clear_genres_table():
    dbHelper.clear_genres_table()
    # get all the columns from the genres table
    try:
        columns = dbHelper.get_all_columns_from_table("genres")
    except Exception as e:
        assert True
        
# --------------------------------------------------------------------------------
#                          TESTING INSERTS
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    test_clear_songs_table()
    # setup_test_db()
