import pytest
import sys, os
import sqlite3
# add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "databases")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "soundfiles")))

import config
import analyticsdb
import songparser

dbHelper = analyticsdb.AnalyticsDBHandler(debug_path=config.DATABASE_TEST_PATH)

song_table_dict = {
    "filepath": "N/A", # string
    "main_artist": "N/A", # string
    "filesize": -1, # in bytes
    "padding": -1, # in bytes
    "album_artwork_bit_depth": -1, # in bits
    "album_artwork_colors": -1, # int
    "album_artwork_height": -1, # in pixels
    "album_artwork_width": -1, # in pixels
    "bit_depth": -1, # in bits
    "bitrate": -1, # in bits, divide by 1000 to get Kbps
    "channels": -1, # int
    "duration": -1, # in seconds
    "sample_rate": -1, # in KHz
    "album": "N/A", # string
    "barcode": "N/A", # string
    "date_created": "N/A", # in YYYY-MM-DD
    "disc_number": -1, # int
    "disc_total": -1, # int
    "genre": "N/A", # string
    "isrc": "N/A", # string
    "itunesadvisory": "N/A", # string
    "length": -1, # int
    "publisher": "N/A", # string
    "rating": -1, # int
    "title": "N/A", # string
    "track_number": -1, # int
    "track_total": -1, # int
    "source": "N/A", # string
}

def setup_test():
    # create a test database
    dbHelper.create_all_tables()

    # lets make some example playlists
        
def test_vital_folders():
    # check if ../analyticsdb ../backups ../logs exist
    assert os.path.exists(os.path.dirname(config.DATABASE_PATH))
    assert os.path.exists(config.BACKUPS_PATH)
    assert os.path.exists(os.path.dirname(config.LOGGING_FILENAME))

if __name__ == "__main__":
    dbHelper = analyticsdb.AnalyticsDBHandler(debug_path=config.DATABASE_TEST_PATH)
    print(dbHelper.get_all_songs())