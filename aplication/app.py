from flask import Flask, request, g, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import artist_controller
from base64 import b64encode
import json

API_URL = 'http://localhost:5000'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app)
ma = Marshmallow(app)

class ArtistSchema(ma.Schema):
  class Meta:
    fields = ('name', 'age', 'albums', 'tracks', 'url')

class AlbumSchema(ma.Schema):
  class Meta:
    fields = ('name', 'genre', 'artist', 'tracks', 'url')

class TrackSchema(ma.Schema):
  class Meta:
    fields = ('name', 'duration', 'times_played', 'artist', 'album', 'url')


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




@app.route('/artists', methods=["GET"])
def get_artists():
    return artist_controller.get_artists(),200

@app.route("/artists", methods=["POST"])
def insert_artist():
    result = artist_controller.insert_artist(request)
    return json.dumps(result), 201

# @app.route("/artists/<id>", methods=["DELETE"])
# def delete_artist(id):
#     result = artist_controller.delete_artist(id)
#     return jsonify(result)

# @app.route("/artists/<artist_id>", methods=["GET"])
# def get_artist_by_id(artist_id):
#     artist = artist_controller.get_by_id(artist_id)
#     total = []
#     dicto_artist = {}
#     dicto_artist["id"] = artist[0]
#     dicto_artist["age"] = artist[2]
#     dicto_artist["name"] = artist[1]
#     dicto_artist["albums"] = artist[3]
#     dicto_artist["tracks"] = artist[4]
#     dicto_artist["self"] = artist[5]
#     total.append(dicto_artist)
#     return jsonify(total)

# @app.route("/artists/<artist_id>/albums", methods=["POST"])
# def insert_albums(artist_id):
#     album_details = request.get_json()
#     name = album_details["name"]
#     string = str(name + ":" + artist_id)
#     album_id = b64encode(string.encode()).decode('utf-8')
#     if len(album_id) > 22:
#         album_id = album_id[:22]
#     genre = album_details["genre"]
#     artist = "http://localhost:5000/artists/"+str(artist_id)
#     tracks = "http://localhost:5000/albums/"+str(album_id)+"/tracks"
#     selff = "http://localhost:5000/albums/"+str(album_id)
#     result = artist_controller.insert_album(album_id, artist_id, name, genre, artist, tracks, selff)
#     return jsonify(result)

# @app.route('/albums', methods=["GET"])
# def get_albums():
#     albums = artist_controller.get_albums()
#     total = []
#     for elem in albums:
#         dicto_album = {}
#         dicto_album["id"] = elem[0]
#         dicto_album["artist_id"] = elem[1]
#         dicto_album["name"] = elem[2]
#         dicto_album["genre"] = elem[3]
#         dicto_album["artist"] = elem[4]
#         dicto_album["tracks"] = elem[5]
#         dicto_album["self"] = elem[6]
#         total.append(dicto_album)
#     return jsonify(total)

# @app.route("/albums/<album_id>", methods=["GET"])
# def get_album_by_id(album_id):
#     album = artist_controller.get_album_by_id(album_id)
#     total = []
#     dicto = {}
#     dicto["id"] = album[0]
#     dicto["artist_id"] = album[1]
#     dicto["age"] = album[2]
#     dicto["genre"] = album[3]
#     dicto["artist"] = album[4]
#     dicto["tracks"] = album[5]
#     dicto["self"] = album[6]
#     total.append(dicto)
#     return jsonify(total)

# @app.route("/artists/<artist_id>/albums", methods=["GET"])
# def get_albums_of_artists(artist_id):
#     albums = artist_controller.get_albums_of_artists(artist_id)
#     total = []
#     for elem in albums:
#         dicto = {}
#         dicto["id"] = elem[0]
#         dicto["artist_id"] = elem[1]
#         dicto["name"] = elem[2]
#         dicto["genre"] = elem[3]
#         dicto["artist"] = elem[4]
#         dicto["tracks"] = elem[5]
#         dicto["self"] = elem[6]
#         total.append(dicto)
#     return jsonify(total)

# @app.route("/albums/<album_id>/tracks", methods=["POST"])
# def insert_tracks(album_id):
#     artist_id = artist_controller.get_artist_id_for_track(album_id)[0]
#     print(artist_id)
#     track_details = request.get_json()
#     name = track_details["name"]
#     string = str(name + ":" + album_id)
#     track_id = b64encode(string.encode()).decode('utf-8')
#     if len(track_id) > 22:
#         track_id = track_id[:22]
#     duration = track_details["duration"]
#     times_played = 0
#     artist = "http://localhost:5000/artists/"+str(artist_id)
#     album = "http://localhost:5000/albums/"+str(album_id)
#     selff = "http://localhost:5000/tracks/"+str(track_id)
#     result = artist_controller.insert_track(track_id, album_id, artist_id, name, duration, times_played, artist, album, selff)
#     return jsonify(result)

# @app.route('/tracks', methods=["GET"])
# def get_tracks():
#     tracks = artist_controller.get_tracks()
#     total = []
#     for elem in tracks:
#         dicto = {}
#         dicto["id"] = elem[0]
#         dicto["album_id"] = elem[1]
#         dicto["name"] = elem[2]
#         dicto["duration"] = elem[3]
#         dicto["times_played"] = elem[4]
#         dicto["artist"] = elem[5]
#         dicto["album"] = elem[6]
#         dicto["self"] = elem[7]
#         total.append(dicto)
#     return jsonify(total)

# @app.route('/albums/<album_id>/tracks', methods=["GET"])
# def get_tracks_of_album(album_id):
#     tracks = artist_controller.get_tracks_of_album(album_id)
#     total = []
#     print(type(tracks))
#     for elem in tracks:
#         dicto = {}
#         dicto["id"] = elem[0]
#         dicto["album_id"] = album_id
#         dicto["name"] = elem[2]
#         dicto["duration"] = elem[3]
#         dicto["times_played"] = elem[4]
#         dicto["artist"] = elem[5]
#         dicto["album"] = elem[6]
#         dicto["self"] = elem[7]
#         total.append(dicto)
#     return jsonify(total)

# @app.route("/tracks/<track_id>", methods=["GET"])
# def get_track_by_id(track_id):
#     track = artist_controller.get_track_by_id(track_id)
#     total = []
#     dicto = {}
#     dicto["id"] = track[0]
#     dicto["album_id"] = track[1]
#     dicto["name"] = track[2]
#     dicto["duration"] = track[3]
#     dicto["times_played"] = track[4]
#     dicto["artist"] = track[5]
#     dicto["album"] = track[6]
#     dicto["self"] = track[7]
#     total.append(dicto)
#     return jsonify(total)

# @app.route('/artists/<artist_id>/tracks', methods=["GET"])
# def get_tracks_of_artist(artist_id):
#     tracks = artist_controller.get_tracks_of_artist(artist_id)
#     total = []
#     print(type(tracks))
#     for elem in tracks:
#         dicto = {}
#         dicto["id"] = elem[0]
#         dicto["album_id"] = elem[1]
#         dicto["name"] = elem[2]
#         dicto["duration"] = elem[3]
#         dicto["times_played"] = elem[4]
#         dicto["artist"] = elem[5]
#         dicto["album"] = elem[6]
#         dicto["self"] = elem[7]
#         total.append(dicto)
#     return jsonify(total)

# @app.route("/albums/<album_id>", methods=["DELETE"])
# def delete_album(album_id):
#     result = artist_controller.delete_albums(album_id)
#     return jsonify(result)

# @app.route("/tracks/<track_id>", methods=["DELETE"])
# def delete_track(track_id):
#     result = artist_controller.delete_tracks(track_id)
#     return jsonify(result)

# @app.route("/tracks/<track_id>/play", methods=["PUT"])
# def update_track(track_id):
#     result = artist_controller.update_tracks(track_id)
#     print(result)
#     return jsonify(result)

# @app.route("/albums/<album_id>/tracks/play", methods=["PUT"])
# def update_track_of_album(album_id):
#     result = artist_controller.update_tracks_of_album(album_id)
#     return jsonify(result)

# @app.route("/artists/<artist_id>/albums/play", methods=["PUT"])
# def update_track_of_artist(artist_id):
#     result = artist_controller.update_tracks_of_artist(artist_id)
#     return jsonify(result)

if __name__ == "__main__":
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
