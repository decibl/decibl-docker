# Make a class to parse the metadata of song Files
import audio_metadata
import config
import os

class SongMetadata:
    pass


metadata = audio_metadata.load(os.path.join(config.SOUNDFILES_PATH, "enemy.flac"))
print(metadata)
metadata2 = audio_metadata.load(os.path.join(config.SOUNDFILES_PATH, "example.mp3"))
print(metadata2)