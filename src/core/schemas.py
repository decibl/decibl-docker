from pydantic import BaseModel
from typing import Union

class PlaylistSongsBase(BaseModel):
    added_date: str

class PlaylistSongsCreate(PlaylistSongsBase):
    pass

class PlaylistSongs(PlaylistSongsBase):
    id: str
    playlist_id: str
    song_id: str

class PlaysBase(BaseModel):
    start_dt: str
    end_dt: str

class PlaysCreate(PlaysBase):
    pass

class Plays(PlaysBase):
    id: str
    song_id: str

    class Config:
        orm_mode: True

class SongsBase(BaseModel):
    filepath: str
    title: str
    artist: str
    albumn: str

class SongsCreate(SongsBase):
    pass

class Songs(SongsBase):
    id: str
    playlists: list[PlaylistSongs] = []

    class Config:
        orm_mode: True

class PlaylistsBase(BaseModel):
    name: str
    created_date: str

class PlaylistsCreate(PlaylistsBase):
    pass

class Playlists(PlaylistsBase):
    id: str
    songs: list[PlaylistSongs] = []