from sqlalchemy.orm import Session

import models, schemas
import sys,os

def get_plays_by_id(db: Session, id: int):
    return db.query(models.Plays).filter(models.Plays.id == id).first()

def get_plays_by_song_id(db: Session, song_id: str):
    return db.query(models.Plays).filter(models.Plays.song_id == song_id).first()

def get_plays(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plays).offset(skip).limit(limit).all()

def create_play(db: Session, play: schemas.PlaysCreate,song_id):
    db_play = models.Plays(**play.dict(),song_id=song_id)
    db.add(db_play)
    db.commit()
    db.refresh(db_play)
    return db_play

def get_song_by_id(db: Session, id: int):
    return db.query(models.Songs).filter(models.Songs.id == id).first()

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Songs).offset(skip).limit(limit).all()

def create_song(db: Session, song: schemas.SongsCreate):
    db_song = models.Songs(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def get_playlist_by_id(db: Session, id: int):
    return db.query(models.Playlists).filter(models.Playlists.id == id).first()

def get_playlists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Playlists).offset(skip).limit(limit).all()

def create_playlist(db: Session, playlist: schemas.PlaylistsCreate):
    db_playlist = models.Songs(**playlist.dict())
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

def create_playlist_song(db: Session, playlistsong: schemas.PlaylistsCreate,playlist_id,song_id):
    db_playlistsong = models.Songs(**playlistsong.dict(),playlist_id = playlist_id, song_id = song_id)
    db.add(db_playlistsong)
    db.commit()
    db.refresh(db_playlistsong)
    return db_playlistsong
