import sqlite3
import json
DATABASE = './database.db'
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def insert_artist(artist_id, name, age, albums, tracks, self):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO artists(artist_id, name, age, albums, tracks, self) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(statement, [artist_id, name, age, albums, tracks, self])
    db.commit()
    lista = [{"id": artist_id, "name":name, "age":age, "albums":albums, "tracks":tracks, "self":self}]
    return lista

# def update_artist(artist_id, name, age, albums, tracks, selff):
#     db = get_db()
#     cursor = db.cursor()
#     statement = "UPDATE artists SET name = ?, age = ?, albums = ?,  tracks = ?,  self = ?, WHERE artist_id = ?"
#     cursor.execute(statement, [artist_id, name, age, albums, tracks, selff])
#     db.commit()
#     return True

def delete_artist(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM artists WHERE artist_id = ?"
    statement2 = "DELETE FROM albums WHERE artist_id = ?"
    statement3 = "DELETE FROM tracks WHERE artist_id = ?"
    cursor.execute(statement, [id])
    cursor.execute(statement2, [id])
    cursor.execute(statement3, [id])
    db.commit() 
    return True

def get_by_id(artist_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT artist_id, name, age, albums, tracks, self FROM artists WHERE artist_id = ?"
    cursor.execute(statement, [artist_id])
    return cursor.fetchone()
    
def get_artists():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT artist_id, name, age, albums, tracks, self FROM artists"
    cursor.execute(query)
    return cursor.fetchall()

def insert_album(album_id, artist_id, name, genre, artist, tracks, self):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO albums(album_id, artist_id, name, genre, artist, tracks, self) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(statement, [album_id, artist_id, name, genre, artist, tracks, self])
    db.commit()
    lista = [{"id":album_id, "artist_id": artist_id, "name":name, "genre":genre, "artist":artist, "tracks":tracks, "self":self}]
    return lista

def get_albums():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT album_id, artist_id, name, genre, artist, tracks, self FROM albums"
    cursor.execute(query)
    return cursor.fetchall()

def get_album_by_id(album_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT album_id, artist_id, name, genre, artist, tracks, self FROM albums WHERE album_id = ?"
    cursor.execute(statement, [album_id])
    return cursor.fetchone()

def get_albums_of_artists(artist_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT album_id, artist_id, name, genre, artist, tracks, self FROM albums WHERE artist_id = ?"
    cursor.execute(statement, [artist_id])
    return cursor.fetchall()

def get_artist_id_for_track(album_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT artist_id FROM albums WHERE album_id = ?"
    cursor.execute(statement, [album_id])
    return cursor.fetchone()

def insert_track(track_id, album_id, artist_id, name, duration, times_played, artist, album, self):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO tracks(track_id, album_id, artist_id, name, duration, times_played, artist, album, self) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(statement, [track_id, album_id, artist_id, name, duration, times_played, artist, album, self])
    db.commit()
    lista = [{"id":track_id, "album_id": album_id, "name":name, "duration":duration, "times_played": times_played, "artist":artist, "album":album, "self":self}]
    return lista

def get_tracks():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT track_id, album_id, name, duration, times_played, artist, album, self FROM tracks"
    cursor.execute(query)
    return cursor.fetchall()

def get_tracks_of_album(album_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT track_id, album_id, name, duration, times_played, artist, album, self FROM tracks WHERE album_id = ?"
    cursor.execute(statement, [album_id])
    return cursor.fetchall()

def get_track_by_id(track_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT track_id, album_id, name, duration, times_played, artist, album, self FROM tracks WHERE track_id = ?"
    cursor.execute(statement, [track_id])
    return cursor.fetchone()

def get_tracks_of_artist(artist_id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT track_id, album_id, name, duration, times_played, artist, album, self FROM tracks WHERE artist_id = ?"
    cursor.execute(statement, [artist_id])
    return cursor.fetchall()

def delete_albums(album_id):
    db = get_db()
    cursor = db.cursor()
    statement2 = "DELETE FROM albums WHERE album_id = ?"
    statement3 = "DELETE FROM tracks WHERE album_id = ?"
    cursor.execute(statement2, [album_id])
    cursor.execute(statement3, [album_id])
    db.commit() 
    return True

def delete_tracks(track_id):
    db = get_db()
    cursor = db.cursor()
    statement3 = "DELETE FROM tracks WHERE track_id = ?"
    cursor.execute(statement3, [track_id])
    db.commit() 
    return True

def update_tracks(track_id):
    db = get_db()
    cursor = db.cursor()
    statement2 = "UPDATE tracks SET times_played = times_played + 1 WHERE track_id = ?"
    cursor.execute(statement2, [track_id])
    db.commit()
    return True

def update_tracks_of_album(album_id):
    db = get_db()
    cursor = db.cursor()
    statement2 = "UPDATE tracks SET times_played = times_played + 1 WHERE album_id = ?"
    cursor.execute(statement2, [album_id])
    db.commit()
    return True

def update_tracks_of_artist(artist_id):
    db = get_db()
    cursor = db.cursor()
    statement2 = "UPDATE tracks SET times_played = times_played + 1 WHERE artist_id = ?"
    cursor.execute(statement2, [artist_id])
    db.commit()
    return True