import datetime
import os
import sys
import sqlite3
import zipfile
# add current file to system path

import logging
import config
import songparser

# log a message
logging.info("Loading database module")


# Make Database class to hold all the data analytics
# This will be used to create and manage the database of the users activity.
# (there's lots of data in the songs table so I'm not going to put it in the graphic)

class AnalyticsDBHandler:
    """Class to handle all the data analytics, especially stuff like creating tables, making backups, etc."""

    # CONSTRUCTOR

    def __init__(self) -> None:
        self.conn = sqlite3.connect(config.DATABASE_PATH)

    # --------------------------------------------------------------------------------------------
    #                                    CREATE AND DELETE TABLES
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
            favorited BOOLEAN,
            main_artist TEXT
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
                song_primary_artist TEXT NOT NULL,
                filesize BIGINT,
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

    def create_genres_table(self) -> bool:
        """Create the genres table, returns True if successful, False if not."""

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
        self.create_genres_table()
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
        cursor.execute("DELETE FROM genres;")
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
    #                                    RETRIEVE DATA INDIVIDUAL
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

    def get_song_by_title_filesize(self, title: str, filesize: int) -> int:
        """Get a song by its title and filesize, returns the id of the song."""

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

    def get_songs_in_playlist(self, playlist_name: str) -> list:
        """Get all the songs in a playlist, returns a list of Song objects."""

        logging.info(f"Getting songs in playlist: {playlist_name}")
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM songs
            INNER JOIN playlists_songs ON songs.song_id = playlists_songs.song_id
            INNER JOIN playlists ON playlists_songs.playlist_id = playlists.playlist_id
            WHERE playlists.playlist_name = ?;""",
            (playlist_name,)
        )
        songs = cursor.fetchall()
        logging.info(f"Got songs in playlist: {playlist_name}")
        return songs

    def get_playlist_id_by_name(self, playlist_name: str) -> int:
        """Get a playlist by its name, returns the id of the playlist."""

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
    # --------------------------------------------------------------------------------------------
    #                                    RETRIEVE DATA MULTIPLE
    # --------------------------------------------------------------------------------------------


    def get_all_tables(self) -> list:
        """Get all the tables in the database, returns a list of table names."""

        logging.info("Getting all tables")
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logging.info("Got all tables")
        return tables

    def get_all_songs(self) -> list:
        """Get all the songs in the database, returns a list of Song objects."""

        logging.info("Getting all songs")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM songs;")
        songs = cursor.fetchall()
        logging.info("Got all songs")
        return songs

    def get_all_plays(self) -> list:
        """Get all the plays in the database, returns a list of Play objects."""

        logging.info("Getting all plays")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM plays;")
        plays = cursor.fetchall()
        logging.info("Got all plays")
        return plays

    

    # --------------------------------------------------------------------------------------------
    #                                    INSERT DATA
    # --------------------------------------------------------------------------------------------

    def insert_playlist(self, playlist_name: str, created_dt: str) -> bool:
        """Insert a playlist into the database, returns True if successful, False if not. Only insert if the playlist does not already exist."""
        logging.info("Inserting playlist {} into playlists table".format(playlist_name))

        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO playlists (playlist_name, created_dt)
            SELECT ?, ? WHERE NOT EXISTS (
                SELECT 1 FROM playlists WHERE playlist_name = ?
            );""",
            (playlist_name, created_dt, playlist_name)
        )
        self.conn.commit()
        logging.info("Inserted playlist {} into playlists table".format(playlist_name))
        return True

    def insert_playlist_song(self, playlist_name: str, song_id: int) -> bool:
        """Insert a playlist_song into the database, returns True if successful, False if not."""
        logging.info("Inserting playlist_song {} into playlists_songs table".format(playlist_name))

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
        logging.info("Inserted playlist_song {} into playlists_songs table".format(playlist_name))
        return True

    def insert_song(self, **kwargs) -> bool:
        """Insert a song into the database, returns song_id of inserted song. 
        Only insert if the song does not already exist. Use the title and filesize.
        Returns the song_id"""
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
        #     "genre": "N/A", # string
        #     "isrc": "N/A", # string
        #     "itunesadvisory": "N/A", # string
        #     "length": -1, # int
        #     "publisher": "N/A", # string
        #     "rating": -1, # int
        #     "title": "N/A", # string
        #     "track_number": -1, # int
        #     "track_total": -1, # int
        #     "source": "N/A", # string
        #     "favorited": False, # bool
        # }

        # check if song already exists
        song_id = self.get_song_by_title_filesize(
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
                source,
                favorited
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
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
                kwargs["favorited"]
            )
        )

        self.conn.commit()
        # get the song_id of the inserted song
        cursor.execute(
            """SELECT song_id FROM songs WHERE filepath = ?;""",
            (kwargs["filepath"],)
        )

        song_id = cursor.fetchone()[0]
        logging.info(f"Inserted song with song_id: {song_id}")
        return song_id

    def insert_album_artist(self, artist_name, song_id) -> bool:
        """Insert an album_artist into the database, returns True if successful, False if not. Only insert if the album_artist does not already exist."""
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
        """Insert a song_artist into the database, returns True if successful, False if not. Only insert if the song_artist does not already exist."""
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
        """Insert a composer into the database, returns True if successful, False if not. 
        Only insert if the composer does not already exist."""
        logging.info("Attempting to insert composer {} with song_id {} into composers table".format(
            composer_name, song_id))
        cursor = self.conn.cursor()
        # cursor.execute(
        #     """INSERT INTO composers (composer_name, song_id, dt_added)
        #     SELECT ?, ?, ? WHERE NOT EXISTS (
        #         SELECT 1 FROM composers WHERE composer_name = ? AND song_id = ?
        #     );""",
        #     (composer_name, song_id, datetime.datetime.now(), composer_name, song_id)
        # )

        # check if composer already exists
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
        # cursor.execute(
        #     """INSERT INTO genres (genre_name, song_id, dt_added)
        #     SELECT ?, ?, ? WHERE NOT EXISTS (
        #         SELECT 1 FROM genres WHERE genre_name = ? AND song_id = ?
        #     );""",
        #     (genre_name, song_id, datetime.datetime.now(), genre_name, song_id)
        # )

        # check if genre already exists
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
        """Populate the database with all the given data"""

        # fetch all the files from config.SOUNDFILES_PATH
        soundfiles = os.listdir(config.SOUNDFILES_PATH)

        for file in soundfiles:
            # get path of file
            file_path = os.path.join(config.SOUNDFILES_PATH, file)

            # get metadata from file
            parser = songparser.SongMetadata(file_path)

            # get the song data and insert it into the database
            song_data = parser.get_song_table_data()
            song_id = None
            if song_data is not None:
                print(song_data['barcode'])
                song_id = self.insert_song(**song_data)
            else:
                logging.error(f"Could not get song data for file: {file_path}")
                continue

            # get the
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
    # db_handler.create_all_tables()
    # db_handler.clear_all_tables()
    db_handler.populate_database()
    # print(db_handler.get_all_songs())

    db_handler.insert_playlist("Test Playlist", datetime.datetime.now())
    db_handler.insert_playlist_song("Test Playlist", 1)
    db_handler.insert_playlist_song("Test Playlist", 2)
    db_handler.insert_playlist_song("Test Playlist", 3)
    db_handler.insert_playlist_song("Test Playlist", 4)

    # print(db_handler.get_songs_in_playlist("Test Playlist"))
    # print(db_handler.get_song_by_title_filesize("Gemstone", 34815481))
    # # sp = songparser.SongMetadata(os.path.join(config.SOUNDFILES_PATH, "Gemstone.flac"))
    # # print(sp.get_song_table_data())
    # logging.error("Finished")
