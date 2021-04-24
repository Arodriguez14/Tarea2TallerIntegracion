from flask import Flask, request, g, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import config	
import sqlite3
import artist_controller
from base64 import b64encode
import json


app = Flask(__name__)

DATABASE = './database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_artists_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS artists(
                artist_id STRING,
                name STRING,
				age INTEGER,
				albums TEXT,
                tracks TEXT,
                self TEXT
            )
            """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    print("Tabla creada")

def create_albums_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS albums (
                album_id STRING PRIMARY KEY,
                name STRING,
				genre STRING,
				artist TEXT,
                tracks TEXT,
                self TEXT,
                artist_id STRING,
                FOREIGN KEY (artist_id) 
                    REFERENCES artists (artist_id) 
                    ON DELETE CASCADE
                            )
            """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    print("Tabla creada")

def create_tracks_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS tracks (
                track_id STRING PRIMARY KEY,
                name STRING,
				duration FLOAT,
                times_played INTEGER,
				artist TEXT,
                album TEXT,
                self TEXT,
                artist_id STRING,
                album_id STRING,
                FOREIGN KEY (album_id) 
                    REFERENCES albums (album_id) 
                    ON DELETE CASCADE,
                FOREIGN KEY (artist_id) 
                    REFERENCES artists (artist_id) 
                    ON DELETE CASCADE 
            )
            """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    print("Tabla creada")

@app.route('/artists', methods=["GET"])
def get_artists():
    artists = artist_controller.get_artists()
    total = []
    for elem in artists:
        dicto_artist = {}
        dicto_artist["id"] = elem[0]
        dicto_artist["name"] = elem[1]
        dicto_artist["age"] = elem[2]
        dicto_artist["albums"] = elem[3]
        dicto_artist["tracks"] = elem[4]
        dicto_artist["self"] = elem[5]
        total.append(dicto_artist)

    return jsonify(total)

@app.route("/artists", methods=["POST"])
def insert_artist():
    artist_details = request.get_json()
    name = artist_details["name"]
    artist_id = b64encode(name.encode()).decode('utf-8')
    if len(artist_id) > 22:
        artist_id = artist_id[:22]
    age = artist_details["age"]
    albums = "http://localhost:5000/artists/"+str(artist_id)+"/albums"
    tracks = "http://localhost:5000/artists/"+str(artist_id)+"/tracks"
    selff = "http://localhost:5000/artists/"+str(artist_id)
    result = artist_controller.insert_artist(artist_id, name, age, albums, tracks, selff)

    return jsonify(result)

@app.route("/artists/<id>", methods=["DELETE"])
def delete_artist(id):
    result = artist_controller.delete_artist(id)
    return jsonify(result)

@app.route("/artists/<artist_id>", methods=["GET"])
def get_artist_by_id(artist_id):
    artist = artist_controller.get_by_id(artist_id)
    total = []
    dicto_artist = {}
    dicto_artist["id"] = artist[0]
    dicto_artist["age"] = artist[2]
    dicto_artist["name"] = artist[1]
    dicto_artist["albums"] = artist[3]
    dicto_artist["tracks"] = artist[4]
    dicto_artist["self"] = artist[5]
    total.append(dicto_artist)
    return jsonify(total)

@app.route("/artists/<artist_id>/albums", methods=["POST"])
def insert_albums(artist_id):
    album_details = request.get_json()
    name = album_details["name"]
    string = str(name + ":" + artist_id)
    album_id = b64encode(string.encode()).decode('utf-8')
    if len(album_id) > 22:
        album_id = album_id[:22]
    genre = album_details["genre"]
    artist = "http://localhost:5000/artists/"+str(artist_id)
    tracks = "http://localhost:5000/albums/"+str(album_id)+"/tracks"
    selff = "http://localhost:5000/albums/"+str(album_id)
    result = artist_controller.insert_album(album_id, artist_id, name, genre, artist, tracks, selff)
    return jsonify(result)

@app.route('/albums', methods=["GET"])
def get_albums():
    albums = artist_controller.get_albums()
    total = []
    for elem in albums:
        dicto_album = {}
        dicto_album["id"] = elem[0]
        dicto_album["artist_id"] = elem[1]
        dicto_album["name"] = elem[2]
        dicto_album["genre"] = elem[3]
        dicto_album["artist"] = elem[4]
        dicto_album["tracks"] = elem[5]
        dicto_album["self"] = elem[6]
        total.append(dicto_album)
    return jsonify(total)

@app.route("/albums/<album_id>", methods=["GET"])
def get_album_by_id(album_id):
    album = artist_controller.get_album_by_id(album_id)
    total = []
    dicto = {}
    dicto["id"] = album[0]
    dicto["artist_id"] = album[1]
    dicto["age"] = album[2]
    dicto["genre"] = album[3]
    dicto["artist"] = album[4]
    dicto["tracks"] = album[5]
    dicto["self"] = album[6]
    total.append(dicto)
    return jsonify(total)

@app.route("/artists/<artist_id>/albums", methods=["GET"])
def get_albums_of_artists(artist_id):
    albums = artist_controller.get_albums_of_artists(artist_id)
    total = []
    for elem in albums:
        dicto = {}
        dicto["id"] = elem[0]
        dicto["artist_id"] = elem[1]
        dicto["name"] = elem[2]
        dicto["genre"] = elem[3]
        dicto["artist"] = elem[4]
        dicto["tracks"] = elem[5]
        dicto["self"] = elem[6]
        total.append(dicto)
    return jsonify(total)

@app.route("/albums/<album_id>/tracks", methods=["POST"])
def insert_tracks(album_id):
    artist_id = artist_controller.get_artist_id_for_track(album_id)[0]
    print(artist_id)
    track_details = request.get_json()
    name = track_details["name"]
    string = str(name + ":" + album_id)
    track_id = b64encode(string.encode()).decode('utf-8')
    if len(track_id) > 22:
        track_id = track_id[:22]
    duration = track_details["duration"]
    times_played = 0
    artist = "http://localhost:5000/artists/"+str(artist_id)
    album = "http://localhost:5000/albums/"+str(album_id)
    selff = "http://localhost:5000/tracks/"+str(track_id)
    result = artist_controller.insert_track(track_id, album_id, artist_id, name, duration, times_played, artist, album, selff)
    return jsonify(result)

@app.route('/tracks', methods=["GET"])
def get_tracks():
    tracks = artist_controller.get_tracks()
    total = []
    for elem in tracks:
        dicto = {}
        dicto["id"] = elem[0]
        dicto["album_id"] = elem[1]
        dicto["name"] = elem[2]
        dicto["duration"] = elem[3]
        dicto["times_played"] = elem[4]
        dicto["artist"] = elem[5]
        dicto["album"] = elem[6]
        dicto["self"] = elem[7]
        total.append(dicto)
    return jsonify(total)

@app.route('/albums/<album_id>/tracks', methods=["GET"])
def get_tracks_of_album(album_id):
    tracks = artist_controller.get_tracks_of_album(album_id)
    total = []
    print(type(tracks))
    for elem in tracks:
        dicto = {}
        dicto["id"] = elem[0]
        dicto["album_id"] = album_id
        dicto["name"] = elem[2]
        dicto["duration"] = elem[3]
        dicto["times_played"] = elem[4]
        dicto["artist"] = elem[5]
        dicto["album"] = elem[6]
        dicto["self"] = elem[7]
        total.append(dicto)
    return jsonify(total)

@app.route("/tracks/<track_id>", methods=["GET"])
def get_track_by_id(track_id):
    track = artist_controller.get_track_by_id(track_id)
    total = []
    dicto = {}
    dicto["id"] = track[0]
    dicto["album_id"] = track[1]
    dicto["name"] = track[2]
    dicto["duration"] = track[3]
    dicto["times_played"] = track[4]
    dicto["artist"] = track[5]
    dicto["album"] = track[6]
    dicto["self"] = track[7]
    total.append(dicto)
    return jsonify(total)

@app.route('/artists/<artist_id>/tracks', methods=["GET"])
def get_tracks_of_artist(artist_id):
    tracks = artist_controller.get_tracks_of_artist(artist_id)
    total = []
    print(type(tracks))
    for elem in tracks:
        dicto = {}
        dicto["id"] = elem[0]
        dicto["album_id"] = elem[1]
        dicto["name"] = elem[2]
        dicto["duration"] = elem[3]
        dicto["times_played"] = elem[4]
        dicto["artist"] = elem[5]
        dicto["album"] = elem[6]
        dicto["self"] = elem[7]
        total.append(dicto)
    return jsonify(total)

@app.route("/albums/<album_id>", methods=["DELETE"])
def delete_album(album_id):
    result = artist_controller.delete_albums(album_id)
    return jsonify(result)

@app.route("/tracks/<track_id>", methods=["DELETE"])
def delete_track(track_id):
    result = artist_controller.delete_tracks(track_id)
    return jsonify(result)

@app.route("/tracks/<track_id>/play", methods=["PUT"])
def update_track(track_id):
    result = artist_controller.update_tracks(track_id)
    print(result)
    return jsonify(result)

@app.route("/albums/<album_id>/tracks/play", methods=["PUT"])
def update_track_of_album(album_id):
    result = artist_controller.update_tracks_of_album(album_id)
    return jsonify(result)

@app.route("/artists/<artist_id>/albums/play", methods=["PUT"])
def update_track_of_artist(artist_id):
    result = artist_controller.update_tracks_of_artist(artist_id)
    return jsonify(result)

if __name__ == "__main__":
    create_artists_tables()
    create_albums_tables()
    create_tracks_tables()
    app.run()




# @app.route("/artist", methods=["PUT"])
# def update_artist():
#     artist_details = request.get_json()
#     name = artist_details["name"]
#     artist_id = b64encode(name.encode()).decode('utf-8')
#     age = artist_details["age"]
#     albums = artist_details["albums"]
#     tracks = artist_details["tracks"]
#     selff = artist_details["self"]
#     result = artist_controller.update_artist(artist_id, name, age, albums, tracks, selff)
#     print(jsonify(result))
#     return jsonify(result)
