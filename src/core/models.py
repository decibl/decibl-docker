from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config import DBbase

class Plays(DBbase):
    __tablename__ = "plays"

    id = Column(String, primary_key=True, index=True)
    song_id = Column(String, ForeignKey("songs.id"))
    start_dt = Column(String)
    end_dt = Column(String)
    
    song = relationship("Songs", back_populates="plays")

class Songs(DBbase):
    __tablename__ = "songs"

    id = Column(String, primary_key=True, index=True)
    filepath = Column(String,unique=True)
    title = Column(String)
    artist = Column(String)
    albumn = Column(String)

    plays = relationship("Plays", back_populates="song")
    playlists = relationship("PlaylistSongs", back_populates="song")

class Playlists(DBbase):
    __tablename__ = "playlists"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    created_date = Column(String)

    songs = relationship("PlaylistSongs", back_populates="playlist")

class PlaylistSongs(DBbase):
    __tablename__ = "playlist_songs"

    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(String, ForeignKey("playlists.id"))
    song_id = Column(String, ForeignKey("songs.id"))
    added_date = Column(String)

    playlist = relationship("Playlists", back_populates="songs")
    song = relationship("Songs", back_populates="playlists")