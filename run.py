from app import app 
from app import get_db
from flask import Flask

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

app.run(
    debug = True
)