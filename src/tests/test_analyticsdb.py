import pytest
import sys, os
import sqlite3
# add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analyticsdb")))

import config
import analyticsdb

def delete_folder(path):
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
        os.rmdir(path)
    
def prepare_test():
    # delete ../analyticsdb ../backups ../logs with all files in them
    try:
        if os.path.exists(config.DATABASE_PATH):
            delete_folder(os.path.dirname(config.DATABASE_PATH))
        if os.path.exists(config.BACKUPS_PATH):
            delete_folder(config.BACKUPS_PATH)
        if os.path.exists(config.LOGGING_FILENAME):
            delete_folder(os.path.dirname(config.LOGGING_FILENAME))
    except Exception as e:
        print(e)
        return False
        
        
def test_vital_folders():
    # check if ../analyticsdb ../backups ../logs exist
    assert os.path.exists(os.path.dirname(config.DATABASE_PATH))
    assert os.path.exists(config.BACKUPS_PATH)
    assert os.path.exists(os.path.dirname(config.LOGGING_FILENAME))

def test_table_creation():
    dbHelper = analyticsdb.AnalyticsDBHandler()
    dbHelper.create_all_tables()

    # make sure all tables exist
    tables = dbHelper.get_all_tables()
    print(tables)

    # make sure there is a plays, playlists, songs, and playlist_songs table
    count = 0
    for table in tables:
        if table[0] == "plays":
            count += 1
        elif table[0] == "playlists":
            count += 1
        elif table[0] == "songs":
            count += 1
        elif table[0] == "playlists_songs":
            count += 1
    assert count == 4

def test_insertion_retrieval():
    dbHelper = analyticsdb.AnalyticsDBHandler()
    dbHelper.create_all_tables()
    dbHelper.clear_all_tables()

    # insert a song
        # def insert_song(self, filepath: str, title: str, artist: str, album: str) -> bool:

    song = ("C:\\Users\\jason\\Desktop\\test.mp3", "test", "test", "test")
    dbHelper.insert_song(*song)

    # insert a playlist
    #     def insert_playlist(self, playlist_name: str, created_dt: str) -> bool:

    playlist = ("test", "2020-01-01 00:00:00")
    dbHelper.insert_playlist(*playlist)

    # insert a play
    #     def insert_play(self, song_title: str, song_artist: str, start_dt: str, end_dt: str) -> bool:

    play = ("test", " test", "2020-01-01 00:00:00", "2020-01-01 00:00:00") 
    dbHelper.insert_play(*play)

    #     def insert_playlist_song(self, playlist_id: int, song_id: int, added_dt: str) -> bool:
    playlist_song = (1, 1, "2020-01-01 00:00:00")
    dbHelper.insert_playlist_song(*playlist_song)

    # get all songs
    songs = dbHelper.get_all_songs()
    print(songs)
    assert len(songs) == 1

    # get all playlists
    playlists = dbHelper.get_all_playlists()
    print(playlists)
    assert len(playlists) == 1

    # get all plays
    plays = dbHelper.get_all_plays()
    print(plays)
    assert len(plays) == 1

    # get all songs in a playlist
    songs = dbHelper.get_all_playlists()
    print(songs)
    assert len(songs) == 1

    # get all playlists a song is in
    playlists = dbHelper.get_all_playlists_songs()
    print(playlists)
    assert len(playlists) == 1