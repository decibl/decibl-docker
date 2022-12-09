# Make a class to parse the metadata of song Files
#import audio_metadata
import config
import os
from abc import ABC, abstractmethod
import logging
import audio_metadata
from typing import List, Dict
# make decorator to log a certain method is being ran with a file
# this is the first time I've used decorators LOL


def log_data(func):
    def wrapper(*args, **kwargs):
        logging.info("Running " + func.__name__ + " on " + args[0].filename)
        return func(*args, **kwargs)
    return wrapper


class SongFile(ABC):

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        logging.info("Parsing metadata for " + self.filename)

    def __init__(self):
        self.filepath = None
        self.filename = None


    @log_data
    @abstractmethod
    def get_song_table_data(self) -> Dict[str, str]:
        """
        get_song_table_data Abstract method to get all the data required for the song table

        Returns:
            Dict: a dictionary with all the data required for the song table
        """        
        pass

    @log_data
    @abstractmethod
    def get_album_artist_data(self):
        pass

    @log_data
    @abstractmethod
    def get_song_artist_data(self):
        pass

    @log_data
    @abstractmethod
    def get_composer_data(self):
        pass

    @log_data
    @abstractmethod
    def get_genre_data(self):
        pass


class SongFileFLAC(SongFile):

    def __init__(self, filepath: str):
        """
        __init__ constructor for SongFileFLAC

        Args:
            filepath (str): the filepath of the FLAC song file (absolute path, use os.join)
        """        
        super().__init__(filepath)
        self.metadata = None
        self.song_table_data = None

        self.loadMetadata(filepath)
        self.make_song_table_data()

    def __init__(self):
        """
        __init__ Default constructor for SongFileFLAC. Does nothing.
        """        
        super().__init__()
        self.metadata = None
        self.song_table_data = None


    def make_song_table_data(self):
        """
        make_song_table_data Instantiates the song_table_data dictionary with all the keys and values set to None.
        """        
        # there's so much data bruh, here's a big ass list that details everything
        # this method isn't really necessary, but I thinik it makes things cleaner
        self.song_table_data = {
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
            "favorited": False,  # bool
        }

    def loadMetadata(self, filepath:str) -> None:
        """
        loadMetadata Loads the metadata of the FLAC file into the metadata variable.

        Args:
            filepath (str): the filepath of the FLAC song file (absolute path, use os.join)

        Returns:
            _type_: None
        """        
        
        return audio_metadata.load(filepath)

    def loadMetadataParams(self, params: dict) -> None:
        """
        loadMetadataParams Loads the metadata of the FLAC file into the metadata variable. Necessary if not using filepaths.

        Args:
            params (dict): the metadata of the FLAC song file
        """        
        self.song_table_data = params

    def get_song_table_data(self) -> dict:
        """
        get_song_table_data Looks at self.metadata and self.song_table_data and grabs all possible data from self.metadata and puts it into self.song_table_data.

        Returns:
            dict: dictionary of keys and values of the song table data
        """        
        super().get_song_table_data()
        # do the above but with if statements to check if the key exists
        if "filepath" in self.metadata:
            self.song_table_data["filepath"] = self.metadata["filepath"]
        if "filesize" in self.metadata:
            self.song_table_data["filesize"] = self.metadata["filesize"]
        if "padding" in self.metadata:
            self.song_table_data["padding"] = self.metadata["padding"].size
        if "pictures" in self.metadata:
            if "bit_depth" in self.metadata["pictures"][0]:
                self.song_table_data["album_artwork_bit_depth"] = self.metadata["pictures"][0]["bit_depth"]
            if "colors" in self.metadata["pictures"][0]:
                self.song_table_data["album_artwork_colors"] = self.metadata["pictures"][0]["colors"]
            if "height" in self.metadata["pictures"][0]:
                self.song_table_data["album_artwork_height"] = self.metadata["pictures"][0]["height"]
            if "width" in self.metadata["pictures"][0]:
                self.song_table_data["album_artwork_width"] = self.metadata["pictures"][0]["width"]
        if "streaminfo" in self.metadata:
            if "bit_depth" in self.metadata["streaminfo"]:
                self.song_table_data["bit_depth"] = self.metadata["streaminfo"]["bit_depth"]
            if "bitrate" in self.metadata["streaminfo"]:
                self.song_table_data["bitrate"] = self.metadata["streaminfo"]["bitrate"]
            if "channels" in self.metadata["streaminfo"]:
                self.song_table_data["channels"] = self.metadata["streaminfo"]["channels"]
            if "duration" in self.metadata["streaminfo"]:
                self.song_table_data["duration"] = self.metadata["streaminfo"]["duration"]
            if "sample_rate" in self.metadata["streaminfo"]:
                self.song_table_data["sample_rate"] = self.metadata["streaminfo"]["sample_rate"]
        if "tags" in self.metadata:
            if "album" in self.metadata["tags"]:
                self.song_table_data["album"] = self.metadata["tags"]["album"][0]
            if "barcode" in self.metadata["tags"]:
                self.song_table_data["barcode"] = self.metadata["tags"]["barcode"][0]
            if "date" in self.metadata["tags"]:
                self.song_table_data["date_created"] = self.metadata["tags"]["date"][0]
            if "discnumber" in self.metadata["tags"]:
                self.song_table_data["disc_number"] = self.metadata["tags"]["discnumber"][0]
            if "disctotal" in self.metadata["tags"]:
                self.song_table_data["disc_total"] = self.metadata["tags"]["disctotal"][0]
            if "isrc" in self.metadata["tags"]:
                self.song_table_data["isrc"] = self.metadata["tags"]["isrc"][0]
            if "itunesadvisory" in self.metadata["tags"]:
                self.song_table_data["itunesadvisory"] = self.metadata["tags"]["itunesadvisory"][0]
            if "length" in self.metadata["tags"]:
                self.song_table_data["length"] = self.metadata["tags"]["length"][0]
            if "publisher" in self.metadata["tags"]:
                self.song_table_data["publisher"] = self.metadata["tags"]["publisher"][0]
            if "rating" in self.metadata["tags"]:
                self.song_table_data["rating"] = self.metadata["tags"]["rating"][0]
            if "title" in self.metadata["tags"]:
                self.song_table_data["title"] = self.metadata["tags"]["title"][0]
            if "tracknumber" in self.metadata["tags"]:
                self.song_table_data["track_number"] = self.metadata["tags"]["tracknumber"][0]
            if "tracktotal" in self.metadata["tags"]:
                self.song_table_data["track_total"] = self.metadata["tags"]["tracktotal"][0]
            if "source" in self.metadata["tags"]:
                self.song_table_data["source"] = self.metadata["tags"]["source"][0]
        if "artist" in self.metadata["tags"]:
            self.song_table_data["main_artist"] = self.metadata["tags"]["artist"][0]

        return self.song_table_data

    def get_album_artist_data(self) -> List[str]:
        """
        get_album_artist_data gets the album artist data from the metadata

        Returns:
            List[str]: list of album artists for FLAC files
        """        
        super().get_album_artist_data()
        if "albumartist" in self.metadata["tags"]:
            return self.metadata["tags"]["albumartist"]
        else:
            return None

    def get_song_artist_data(self) -> List[str]:
        """
        get_song_artist_data gets the song artist data from the metadata

        Returns:
            List[str]: list of song artists for FLAC files
        """        
        
        super().get_song_artist_data()
        if "artist" in self.metadata["tags"]:
            return self.metadata["tags"]["artist"]
        else:
            return None

    def get_composer_data(self) -> List[str]:
        """
        get_composer_data gets the composer data from the metadata

        Returns:
            List[str]: list of composers for FLAC files
        """        
        super().get_composer_data()
        if "composer" in self.metadata["tags"]:
            return self.metadata["tags"]["composer"]
        else:
            return None

    def get_genre_data(self) -> List[str]:
        """
        get_genre_data gets the genre data from the metadata

        Returns:
            List[str]: list of genres for FLAC files
        """        
        super().get_genre_data()
        if "genre" in self.metadata["tags"]:
            return self.metadata["tags"]["genre"]
        else:
            return None


class SongMetadata:
    # Songs have a lot of Metadata! We want to store as much as possible.
    # We will store the following:
    #   - filepath
    #   - filesize (in bytes)
    #   - padding (in bytes)
    #   - Album Artwork Bit Depth (in bits)
    #   - Album Artwork Colors (int)
    #   - Album Artwork Size (in bytes)
    #   - Album Artwork Height (in pixels)
    #   - Album Artwork Width (in pixels)
    #   - bit_depth (in bits)
    #   - bitrates (in Kbps)
    #   - channels (int)
    #   - duration (in seconds)
    #   - sample_rate (in KHz)
    #   - Album
    #   - Album Artists
    #   - Song Artists
    #   - Barcode
    #   - Composers
    #   - Date Created (in YYYY-MM-DD)
    #   - Disc Number
    #   - Disc Total
    #   - Genre
    #   - ISRC
    #   - itunesadvisory
    #   - length
    #   - publisher
    #   - rating
    #   - title
    #   - track number
    #   - track total
    #   - favorited (bool)

    def __init__(self, filepath):
        """Initialize the SongMetadata object.
            We want to see what file type it is, and load the correct file."""
        self.extension = os.path.splitext(filepath)[1]
        self.songfile = None
        if self.extension == ".flac":
            self.songfile = SongFileFLAC(filepath)
        else:
            logging.error("File type not supported: " + self.extension)


    def get_song_table_data(self) -> Dict[str, str]:
        """
        get_song_table_data Gets the required song data for inserting into the database depending on the file

        Returns:
            Dict[str, str]: Dictionary of song data
        """         
        if self.songfile is not None:
            return self.songfile.get_song_table_data()

    def get_album_artist_data(self) -> List[str]:
        """
        get_album_artist_data Gets the album artist data for inserting into the database depending on the file

        Returns:
            List[str]: List of album artists
        """        
        if self.songfile is not None:
            return self.songfile.get_album_artist_data()

    def get_song_artist_data(self) -> List[str]:
        """
        get_song_artist_data Gets the song artist data for inserting into the database depending on the file

        Returns:
            List[str]: List of song artists
        """        
        if self.songfile is not None:
            return self.songfile.get_song_artist_data()

    def get_composer_data(self) -> List[str]:
        """
        get_composer_data Gets the composer data for inserting into the database depending on the file

        Returns:
            List[str]: List of composers
        """        
        if self.songfile is not None:
            return self.songfile.get_composer_data()

    def get_genre_data(self) -> List[str]:
        """
        get_genre_data Gets the genre data for inserting into the database depending on the file

        Returns:
            List[str]: List of genres
        """        
        if self.songfile is not None:
            return self.songfile.get_genre_data()

    # when printed, print the metadata

    def __str__(self):
        return str(self.songfile.metadata)

    # when printed, print the metadata
    def __repr__(self):
        return str(self.songfile.metadata)


# md = SongMetadata(os.path.join(config.SOUNDFILES_PATH, "enemy.flac"))
# print(md.get_song_table_data())
# print(md.get_album_artist_data())
# print(md.get_song_artist_data())

# md2 = SongMetadata(os.path.join(config.SOUNDFILES_PATH, "gemstone.flac"))
# print(md2)
# print(md2.get_song_table_data())
# # metadata2 = audio_metadata.load(os.path.join(config.SOUNDFILES_PATH, "example.mp3"))
# # print(metadata2)
