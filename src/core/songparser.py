# Make a class to parse the metadata of song Files
import audio_metadata
import config
import os

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
        # if filepath ends with .flac then set filetype to flac
        self.filetype = filepath.split(".")[-1]
        if self.filetype == "flac":
            self.metadata = audio_metadata.load(filepath)
        self.make_song_table_data()

    def make_song_table_data(self):
        self.song_table_data = {
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
            "favorited": False, # bool
        }
            

    def get_song_table_data(self):
        if self.filetype == "flac":
            return self.get_song_table_data_flac()

    def get_song_table_data_flac(self):

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

    def get_album_artist_data_flac(self):
        if "albumartist" in self.metadata["tags"]:
            return self.metadata["tags"]["albumartist"]
        else:
            return "N/A"

    def get_song_artist_data_flac(self):
        if "artist" in self.metadata["tags"]:
            return self.metadata["tags"]["artist"]
        else:
            return "N/A"

    def get_composer_data_flac(self):
        if "composer" in self.metadata["tags"]:
            return self.metadata["tags"]["composer"]
        else:
            return "N/A"

    def get_genre_data_flac(self):
        if "genre" in self.metadata["tags"]:
            return self.metadata["tags"]["genre"]
        else:
            return "N/A"

    def get_album_artist_data(self):
        if self.filetype == "flac":
            return self.get_album_artist_data_flac()

    def get_song_artist_data(self):
        if self.filetype == "flac":
            return self.get_song_artist_data_flac()

    def get_composer_data(self):
        if self.filetype == "flac":
            return self.get_composer_data_flac()
        
    def get_genre_data(self):
        if self.filetype == "flac":
            return self.get_genre_data_flac()

    # when printed, print the metadata
    def __str__(self):
        return str(self.metadata)

    # when printed, print the metadata
    def __repr__(self):
        return str(self.metadata)


# md = SongMetadata(os.path.join(config.SOUNDFILES_PATH, "enemy.flac"))
# print(md.get_song_table_data())
# print(md.get_album_artist_data())
# print(md.get_song_artist_data())

md2 = SongMetadata(os.path.join(config.SOUNDFILES_PATH, "gemstone.flac"))
print(md2)
# print(md2.get_song_table_data())
# # metadata2 = audio_metadata.load(os.path.join(config.SOUNDFILES_PATH, "example.mp3"))
# # print(metadata2)