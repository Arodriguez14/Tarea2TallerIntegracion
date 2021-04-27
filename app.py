from flask import Flask, request, g, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#import artist_controller
from base64 import b64encode
import json

#API_URL = 'http://localhost:5000'
API_URL = 'https://tarea2-arodriguez14.herokuapp.com'

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/tarea2'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://hwxdmseprrvfru:0e35e56ac4b45322e1afc4172e94f476a8947d4c6417eecdf7094c4ec2b5ab58@ec2-54-152-185-191.compute-1.amazonaws.com:5432/dadkecbviif2h3'
#####app.config['SQLALCHEMY_DATABASE_URI']='postgresql://bqdysojcqwhkyn:8fd9468ae25e1a10f5fa49787ef633abb28f01c4cb3facaa6a9de0fb47028830@ec2-54-224-120-186.compute-1.amazonaws.com:5432/davh5fis0le6tg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app)
ma = Marshmallow(app)

#MODELOS
class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.String(22), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(150), nullable=False)
    albums = db.Column(db.String(150))
    tracks = db.Column(db.String(150))

    def __init__(self, name, age):
        self.id = self.get_id(name) 
        self.name = name
        self.age = int(age)
        self.albums = API_URL + "/artists/" + self.id + "/albums"
        self.tracks = API_URL + "/artists/"+ self.id + "/tracks" 
        self.url = API_URL + "/artists/"+ self.id

    def get_id(self, name):
        name = b64encode(name.encode()).decode('utf-8')
        return name[:22]

class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.String(22), primary_key=True)
    artist_id = db.Column(db.String(22), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(150))
    tracks = db.Column(db.String(150))

    def __init__(self, name, genre, artist_id):
        self.id = self.get_id(name, artist_id)
        self.name = name
        self.genre = genre
        self.artist_id = artist_id
        self.artist = API_URL + "/artists/" + artist_id 
        self.tracks = API_URL + "/albums/"+ self.id + "/tracks" 
        self.url = API_URL + "/albums/" + self.id
    
    def get_id(self, name, artist_id):
        string = str(name + ":" + artist_id)
        album_id = b64encode(string.encode()).decode('utf-8')
        return album_id[:22]

class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column(db.String(22), primary_key=True)
    album_id = db.Column(db.String(22), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    times_played = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(100), nullable=False) 
    artist = db.Column(db.String(150))
    album = db.Column(db.String(150))

    def __init__(self, name, duration, album_id):
        self.id = self.get_id(name, album_id)
        self.name = name
        self.album_id = album_id
        self.duration = float(duration)
        self.times_played = 0
        self.artist = Album.query.get(album_id).artist
        self.album = API_URL + "/albums/" + album_id 
        self.url = API_URL + "/tracks/" + self.id  
    
    def get_id(self, name, album_id):
        string = str(name + ":" + album_id)
        track_id = b64encode(string.encode()).decode('utf-8')
        return track_id[:22]

db.create_all()

#CONTROLLER

def get_artists_controller():
    artists = Artist.query.all()
    total = []
    for elem in artists:
        dicto_artist = {}
        dicto_artist["name"] = elem.name
        dicto_artist["age"] = elem.age
        dicto_artist["albums"] = elem.albums
        dicto_artist["tracks"] = elem.tracks
        dicto_artist["self"] = elem.url
        total.append(dicto_artist)
    return json.dumps(total), 200

def insert_artists_controller(request):
    try:
        artist_details = request.get_json()
        name = artist_details["name"]
        age = artist_details["age"]
        new_artist = Artist(name, age)
    except:
        return '', 400
    possible_artist = Artist.query.get(new_artist.id)
    if possible_artist is None:
        db.session.add(new_artist)
        db.session.commit()
        lista = {"id": new_artist.id, "name":new_artist.name, "age":new_artist.age, "albums":new_artist.albums, "tracks":new_artist.tracks, "self":new_artist.url}
        return json.dumps(lista), 201
    else:
        lista = {"id": possible_artist.id, "name":possible_artist.name, "age":possible_artist.age, "albums":possible_artist.albums, "tracks":possible_artist.tracks, "self":possible_artist.url}
        return json.dumps(lista), 409

def get_albums_controller():
    albums = Album.query.all()
    total = []
    for elem in albums:
        dicto_album = {}
        dicto_album["name"] = elem.name
        dicto_album["genre"] = elem.genre
        dicto_album["artist"] = elem.artist
        dicto_album["tracks"] = elem.tracks
        dicto_album["self"] = elem.url
        total.append(dicto_album)
    return json.dumps(total), 200

def insert_albums_controller(request, artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        return '', 422
    try:
        album_details = request.get_json()
        name = album_details["name"]
        genre = album_details["genre"]
        new_album = Album(name, genre, artist_id)
    except:
        return '', 400
    possible_album = Album.query.get(new_album.id)
    if possible_album is None:
        db.session.add(new_album)
        db.session.commit()
        lista = {"id": new_album.id, "name":new_album.name, "genre":new_album.genre, "artist":new_album.artist, "tracks":new_album.tracks, "self":new_album.url}
        return json.dumps(lista), 201
    else:
        lista = {"id": possible_album.id, "name":possible_album.name, "genre":possible_album.genre, "artist":possible_album.artist, "tracks":possible_album.tracks, "self":possible_album.url}
        return json.dumps(lista), 409

def get_tracks_controller():
    tracks = Track.query.all()
    total = []
    for elem in tracks:
        dicto_track = {}
        dicto_track["name"] = elem.name
        dicto_track["duration"] = elem.duration
        dicto_track["times_played"] = elem.times_played
        dicto_track["artist"] = elem.artist
        dicto_track["album"] = elem.album
        dicto_track["self"] = elem.url
        total.append(dicto_track)
    return json.dumps(total), 200

def insert_tracks_controller(request, album_id):
    album = Album.query.get(album_id)
    if not album:
        return '', 422
    try:
        track_details = request.get_json()
        name = track_details["name"]
        duration = track_details["duration"]
        new_track = Track(name, duration, album_id)
    except:
        return '', 400
    possible_track = Track.query.get(new_track.id)
    if possible_track is None:
        db.session.add(new_track)
        db.session.commit()
        lista = {"id": new_track.id, "name":new_track.name, "duration":new_track.duration, "times_played":new_track.times_played, "artist":new_track.artist, "album":new_track.album, "self":new_track.url}
        return json.dumps(lista), 201
    else:
        lista = {"id": possible_track.id, "name":possible_track.name, "duration":possible_track.duration, "times_played":possible_track.times_played, "artist":possible_track.artist, "album":possible_track.album, "self":possible_track.url}
        return json.dumps(lista), 409

def get_albums_controller_by_artist(request, artist_id):
    possible_artist = Artist.query.get(artist_id)
    if possible_artist is None:
        return '', 404
    total = []
    all_albums = Album.query.all()
    for album in all_albums:
        if album.artist == API_URL + "/artists/" + artist_id:
            dicto_album = {}
            dicto_album["name"] = album.name
            dicto_album["genre"] = album.genre
            dicto_album["artist"] = album.artist
            dicto_album["tracks"] = album.tracks
            dicto_album["self"] = album.url
            total.append(dicto_album)
    return json.dumps(total), 200   

def get_tracks_controller_by_album(request, album_id):
    possible_album = Album.query.get(album_id)
    if not possible_album:
        return '', 404
    total = []
    all_tracks = Track.query.all()
    for track in all_tracks:
        if track.album == API_URL + "/albums/" + album_id:
            dicto_track = {}
            dicto_track["name"] = track.name
            dicto_track["duration"] = track.duration
            dicto_track["times_played"] = track.times_played
            dicto_track["artist"] = track.artist
            dicto_track["album"] = track.album
            dicto_track["self"] = track.url
            total.append(dicto_track)
    return json.dumps(total), 200

def get_tracks_controller_by_artist(request, artist_id):
    possible_artist = Artist.query.get(artist_id)
    if not possible_artist:
        return '', 404
    total = []
    all_tracks = Track.query.all()
    for track in all_tracks:
        if track.artist == API_URL + "/artists/" + artist_id:
            dicto_track = {}
            dicto_track["name"] = track.name
            dicto_track["duration"] = track.duration
            dicto_track["times_played"] = track.times_played
            dicto_track["artist"] = track.artist
            dicto_track["album"] = track.album
            dicto_track["self"] = track.url
            total.append(dicto_track)
    return json.dumps(total), 200

def get_artist_by_id_controller(artist_id):
    artist = Artist.query.get(artist_id)
    if artist is None:
        return '', 404
    #total = []
    dicto_artist = {}
    dicto_artist["name"] = artist.name
    dicto_artist["age"] = artist.age
    dicto_artist["albums"] = artist.albums
    dicto_artist["tracks"] = artist.tracks
    dicto_artist["self"] = artist.url
    #total.append(dicto_artist)
    return json.dumps(dicto_artist), 200

def get_album_by_id_controller(album_id):
    album = Album.query.get(album_id)
    if album is None:
        return '', 404
    dicto_album = {}
    #total = []
    dicto_album["name"] = album.name
    dicto_album["genre"] = album.genre
    dicto_album["artist"] = album.artist
    dicto_album["tracks"] = album.tracks
    dicto_album["self"] = album.url
    #total.append(dicto_album)
    return json.dumps(dicto_album), 200

def get_track_by_id_controller(track_id):
    track = Track.query.get(track_id)
    if track is None:
        return '', 404
    dicto_track = {}
    #total = []
    dicto_track["name"] = track.name
    dicto_track["duration"] = track.duration
    dicto_track["times_played"] = track.times_played
    dicto_track["artist"] = track.artist
    dicto_track["album"] = track.album
    dicto_track["self"] = track.url
    #total.append(dicto_track)
    return json.dumps(dicto_track), 200

def delete_track_controller(track_id):
    track = Track.query.get(track_id)
    if track is None:
        return '', 404
    db.session.delete(track)
    db.session.commit()
    return '', 204

def delete_album_controller(album_id):
    album = Album.query.get(album_id)
    if album is None:
        return '', 404
    db.session.delete(album)
    all_tracks = Track.query.all()
    for track in all_tracks:
        if track.album == API_URL + "/albums/" + album_id:
            db.session.delete(track)
    db.session.commit()
    return '', 204

def delete_artist_controller(artist_id):
    artist = Artist.query.get(artist_id)
    if artist is None:
        return '', 404
    db.session.delete(artist)
    all_tracks = Track.query.all()
    all_albums = Album.query.all()
    for track in all_tracks:
        if track.artist == API_URL + "/artists/" + artist_id:
            db.session.delete(track)
    for album in all_albums:
        if album.artist == API_URL + "/artists/" + artist_id:
            db.session.delete(album)
    db.session.commit()
    return '', 204

def play_track_controller(track_id):
    track = Track.query.get(track_id)
    if track is None:
        return '', 404
    track.times_played += 1
    db.session.commit()
    return '', 200

def play_tracks_of_album_controller(album_id):
    album = Album.query.get(album_id)
    if album is None:
        return '', 404
    all_tracks = Track.query.all()
    for track in all_tracks:
        if track.album == API_URL + "/albums/" + album_id:
            track.times_played += 1
    db.session.commit()
    return '', 200

def play_tracks_of_artist_controller(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        all_tracks = Track.query.all()
        for track in all_tracks:
            if track.artist == API_URL + "/artists/" + artist_id:
                track.times_played += 1
        db.session.commit()
        return '', 200
    else:
        return '', 404


#RUTAS

@app.route('/artists', methods=["GET", "POST"])
def artists_method():
    if request.method == "GET":
        return get_artists_controller()
    elif request.method == "POST":
        return insert_artists_controller(request)

@app.route('/artists/<artist_id>/albums', methods=["GET", "POST"])
def albums_method(artist_id):
    if request.method == "GET":
        return get_albums_controller_by_artist(request, artist_id)
    elif request.method == "POST":
        return insert_albums_controller(request, artist_id)

@app.route('/albums/<album_id>/tracks', methods=["GET", "POST"])
def tracks_method(album_id):
    if request.method == "GET":
        print("ALBUM_ID,",album_id)
        return get_tracks_controller_by_album(request, album_id)
    elif request.method == "POST":
        return insert_tracks_controller(request, album_id)

@app.route('/artists/<artist_id>/tracks', methods=["GET"])
def tracks_of_artist(artist_id):   
    return get_tracks_controller_by_artist(request, artist_id)

@app.route('/albums', methods=["GET"])
def get_albums():
    return get_albums_controller()

@app.route('/tracks', methods=["GET"])
def get_tracks():
    return get_tracks_controller()

@app.route('/artists/<artist_id>', methods=["GET", "DELETE"])
def get_artist_by_id(artist_id):
    if request.method == "GET":
        return get_artist_by_id_controller(artist_id)
    elif request.method == "DELETE":
        return delete_artist_controller(artist_id)

@app.route('/albums/<album_id>', methods=["GET", "DELETE"])
def get_aalbum_by_id(album_id):
    if request.method == "GET":
        return get_album_by_id_controller(album_id)
    elif request.method == "DELETE":
        return delete_album_controller(album_id)

@app.route('/tracks/<track_id>', methods=["GET", "DELETE"])
def get_track_by_id(track_id):
    if request.method == "GET":
        return get_track_by_id_controller(track_id)
    elif request.method == "DELETE":
        return delete_track_controller(track_id)

@app.route('/tracks/<track_id>/play', methods=["PUT"])
def play_track(track_id):
    return play_track_controller(track_id)

@app.route('/albums/<album_id>/tracks/play', methods=["PUT"])
def play_tracks_of_album(album_id):
    return play_tracks_of_album_controller(album_id)

@app.route('/artists/<artist_id>/tracks/play', methods=["PUT"])
def play_track_of_artist(artist_id):
    return play_tracks_of_artist_controller(artist_id)


if __name__ == "__main__":
    app.run()

