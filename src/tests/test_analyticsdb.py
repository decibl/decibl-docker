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

import config
import analyticsdb
import songparser

# unzip the test database in config.ZIPPED_DATABASE_TEST_PATH

dbHelper = analyticsdb.AnalyticsDBHandler(debug_path=config.DATABASE_TEST_PATH)


def setup_prezipped_db():
    with zipfile.ZipFile(config.ZIPPED_DATABASE_TEST_PATH, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(config.DATABASE_TEST_PATH))


song_table_data = {
    "song_id": "haeirofaiofnaiof",  # string
    "filepath": None,  # string
    "main_artist": None,  # string
    "filesize": 0,  # int in bytes
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
    "isrc": None,  # string
    "itunesadvisory": None,  # string
    "length": None,  # int
    "publisher": None,  # string
    "rating": None,  # int
    "title": "Missing",  # string
    "track_number": None,  # int
    "track_total": None,  # int
    "source": None,  # string
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
    # def insert_playlist_song(self, playlist_name: str, song_id: str) -> bool:

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

    # def get_play_information_from_song_id(self, song_id: str) -> Dict[str, int]:

    songs_info = []
    # get all song_ids
    songs = dbHelper.get_all_songs()
    for song in songs:
        song_id = song["song_id"]
        song_info = dbHelper.get_play_information_from_song_id(song_id)
        songs_info.append(song_info)

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
    try:
        dbHelper.clear_all_tables()
    except:
        pass
    dbHelper.create_songs_table()
    # get all the columns from the songs table
    columns = dbHelper.get_all_columns_from_table("songs")
    assert columns == ['song_id', 'filepath', 'filesize', 'padding', 'album_artwork_bit_depth', 'album_artwork_colors', 'album_artwork_height', 'album_artwork_width', 'bit_depth', 'bitrate', 'channels', 'duration',
                       'sample_rate', 'album', 'barcode', 'date_created', 'disc_number', 'disc_total', 'isrc', 'itunesadvisory', 'length', 'publisher', 'rating', 'title', 'track_number', 'track_total', 'source', 'main_artist']


def test_create_plays_table():
    dbHelper.create_plays_table()
    # get all the columns from the plays table
    columns = dbHelper.get_all_columns_from_table("plays")
    assert columns == ['play_id', 'song_title',
                       'song_primary_artist', 'filesize', 'start_dt', 'end_dt', 'song_id']


def test_create_playlists_table():
    dbHelper.create_playlists_table()
    # get all the columns from the playlists table
    columns = dbHelper.get_all_columns_from_table("playlists")
    assert columns == ['playlist_id', 'playlist_name',
                       'playlist_desc', 'created_dt']


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
#                          TESTING INSERTS AND RETRIEVALS
# --------------------------------------------------------------------------------

    # def insert_play(self, song_title: str, song_primary_artist: str, filesize: int, start_dt: str, end_dt: str) -> bool:
    # def insert_playlist(self, playlist_name: str, playlist_desc: str, created_dt: str) -> bool:
    # def insert_playlist_song(self, playlist_name: str, song_id: str) -> bool:
    # def insert_song(self, **kwargs) -> int:
    # def insert_album_artist(self, artist_name, song_id) -> bool:
    # def insert_song_artist(self, artist_name, song_id) -> bool:
    # def insert_composer(self, composer_name, song_id) -> bool:
    # def insert_genre(self, genre_name, song_id) -> bool:


def test_insert_song():
    dbHelper.create_all_tables()
    song_id = dbHelper.insert_song(**song_table_data)
    print(song_id)
    song_data = dbHelper.get_song_by_id(song_id)
    assert song_data == song_table_data


def test_insert_play():
    play_table_data = {
        "song_title": "test song",
        "song_primary_artist": "test artist",
        "filesize": 123456,
        "start_dt": "2020-01-01 00:00:00",
        "end_dt": "2020-01-01 00:00:00",
        "song_id": song_table_data["song_id"]
    }
    play_id = dbHelper.insert_play(play_table_data["song_title"], play_table_data["song_primary_artist"],
                                   play_table_data["filesize"], play_table_data["start_dt"], play_table_data["end_dt"], play_table_data["song_id"])
    
    play_data = dbHelper.get_play_by_id(play_id)
    play_table_data["play_id"] = play_id
    assert play_data == play_table_data

def test_insert_playlist():
    playlist_table_data = {
        "playlist_name": "test playlist",
        "playlist_desc": "test playlist description",
        "created_dt": "2020-01-01 00:00:00"
    }
    playlist_id = dbHelper.insert_playlist(playlist_table_data["playlist_name"], playlist_table_data["playlist_desc"],
                                           playlist_table_data["created_dt"])
    playlist_data = dbHelper.get_playlist_by_id(playlist_id)
    playlist_table_data["playlist_id"] = playlist_id
    assert playlist_data == playlist_table_data

def test_insert_playlist_song():
    # get all playlists
    playlists = dbHelper.get_all_playlist_names()
    # get all songs
    songs = dbHelper.get_all_songs()
    # insert a playlist song
    playlist_song_id = dbHelper.insert_playlist_song(playlists[0], songs[0]["song_id"])
    # get the playlist song
    playlist_songs = dbHelper.get_songs_in_playlist(playlists[0])
    playlist_songs[0]["song_id"] = songs[0]["song_id"]
    # print(playlist_songs[0])
    # print(songs[0])
    assert playlist_songs[0] == songs[0]

def test_insert_album_artist():
    # get all songs
    songs = dbHelper.get_all_songs()
    # insert an album artist
    dbHelper.insert_album_artist("test artist", songs[0]["song_id"])
    # get the album artist
    album_artists = dbHelper.get_all_album_artists()
    assert album_artists[0] == "test artist"

def test_insert_song_artist():
    # get all songs
    songs = dbHelper.get_all_songs()
    # insert a song artist
    dbHelper.insert_song_artist("test artist", songs[0]["song_id"])
    # get the song artist
    song_artists = dbHelper.get_all_song_artists()
    assert song_artists[0] == "test artist"

def test_insert_composer():
    # get all songs
    songs = dbHelper.get_all_songs()
    # insert a composer
    dbHelper.insert_composer("test composer", songs[0]["song_id"])
    # get the composer
    composers = dbHelper.get_all_composers()
    assert composers[0] == "test composer"

def test_insert_genre():
    # get all songs
    songs = dbHelper.get_all_songs()
    # insert a genre
    dbHelper.insert_genre("test genre", songs[0]["song_id"])
    # get the genre
    genres = dbHelper.get_all_genres()
    assert genres[0] == "test genre"


# --------------------------------------------------------------------------------
#                          COMPLICATED TESTING - RETRIEVALS
# --------------------------------------------------------------------------------

def test_get_all_songs():
    setup_prezipped_db()
    songs = dbHelper.get_all_songs()
    assert len(songs) == 18

def test_get_song_artists_of_song():
    songs = dbHelper.get_all_songs()

    check_dict = {
        0: ["MIYAVI", "Sky-Hi"],
        1: ["MIYAVI"],
        2: ["Martin Garrix", "Macklemore", "Fall Out Boy"],
        3: ["MIYAVI"],
        4: ["MIYAVI"],
        5: ["MIYAVI"],
        6: ["Rag'n'Bone Man"],
        7: ["MIYAVI"],
        8: ["MIYAVI"],
        9: ["MIYAVI"],
        10: [],
        11: ["Imagine Dragons", "Arcane", "League Of Legends"],
        12: [],
        13: ["Frank Ocean"],
        14: ["Hudson Mohawke"],
        15: ["Lil Uzi Vert"],
        16: ["Diggy-MO'"],
        17: ["Steve Lacy"]

    }
    for idx, song in enumerate(songs):
        song_artists = dbHelper.get_song_artists_of_song(song["song_id"])
        assert song_artists == check_dict[idx]

def test_get_album_artists_of_song():
    songs = dbHelper.get_all_songs()

    check_dict = {
        0: ["MIYAVI"],
        1: ["MIYAVI"],
        2: ["Martin Garrix", "Macklemore", "Fall Out Boy"],
        3: ["MIYAVI"],
        4: ["MIYAVI"],
        5: ["MIYAVI"],
        6: ["Rag'n'Bone Man"],
        7: ["MIYAVI"],
        8: ["MIYAVI"],
        9: ["MIYAVI"],
        10: [],
        11: ["Imagine Dragons", "Arcane", "League Of Legends"],
        12: [],
        13: ["Frank Ocean"],
        14: ["Hudson Mohawke"],
        15: ["Lil Uzi Vert"],
        16: [],
        17: ["Steve Lacy"]

    }

    for idx, song in enumerate(songs):
        album_artists = dbHelper.get_album_artists_of_song(song["song_id"])
        assert album_artists == check_dict[idx]

def test_get_composers_of_song():
    songs = dbHelper.get_all_songs()
    check_dict = {
        0: ['Sky-Hi', 'MIYAVI', 'Lenny Skolnik', 'Jonny Litten'],
        1: ['Miyavi'],
        2: ['Martijn Garritsen', 'Brian Lee', 'Jaramye Daniels', 'Giorgio Tuinfort', 'Benjamin Hammond Haggerty'],
        3: ['Andrew Ramsey', 'Shannon Sanders', 'MIYAVI'],
        4: ['MIYAVI', 'Andrew Ramsey', 'Shannon Sanders'],
        5: ['Lenny Skolnik', 'Ilan Kidron', 'MIYAVI'],
        6: [],
        7: ['MIYAVI', 'Lenny Skolnik', 'Seann Bowe'],
        8: ['MIYAVI', 'Lenny Skolnik', 'Ilan Kidron', 'Doc Brittain', 'RAS'],
        9: ['Lalo Schifrin'],
        10: [],
        11: ['Dan Reynolds', 'Wayne Sermon', 'Ben McKee', 'Daniel Platzman', 'Robin Fredriksson', 'Mattias Larsson', 'Justin Tranter', 'Destin Route'],
        12: [],
        13: ['Taylor Johnson', 'James Ho', 'Lonnie Breaux'],
        14: [],
        15: [],
        16: [],
        17: []
    }
    for idx, song in enumerate(songs):
        composers = dbHelper.get_composers_of_song(song["song_id"])
        assert composers == check_dict[idx]
    
def test_get_genres_of_song():
    songs = dbHelper.get_all_songs()
    check_dict = {
        0: ['Rock'],
        1: ['Rock'],
        2: ['Electro', 'Techno/House', 'Dance', 'Pop', 'International Pop', 'Rock'],
        3: ['Rock'],
        4: ['Rock'],
        5: ['Rock'],
        6: ['Alternative; Indie Pop; Indie Rock'],
        7: ['Rock'],
        8: ['Rock'],
        9: ['Rock'],
        10: [],
        11: ['Alternative'],
        12: [],
        13: ['Pop'],
        14: ['Alternative', 'Electro'],
        15: ['Rap/Hip Hop'],
        16: ['Anime'],
        17: ['R&B']
    }
    for idx, song in enumerate(songs):
        genres = dbHelper.get_genres_of_song(song["song_id"])
        assert genres == check_dict[idx]
        
if __name__ == "__main__":
    # test_clear_songs_table()
    # setup_test_db()
    pass
