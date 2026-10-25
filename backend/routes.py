"""REST endpoints for the band's songs catalogue."""

import json
import os
from pathlib import Path

from flask import jsonify, request
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import DuplicateKeyError

from . import app


def create_collection():
    service = os.environ.get("MONGODB_SERVICE")
    if service:
        username = os.environ.get("MONGODB_USERNAME")
        password = os.environ.get("MONGODB_PASSWORD")
        if username and password:
            from urllib.parse import quote_plus

            service = f"{quote_plus(username)}:{quote_plus(password)}@{service}"
        client = MongoClient(f"mongodb://{service}", serverSelectionTimeoutMS=5000)
    else:
        # Local runs use an in-memory MongoDB-compatible collection.
        import mongomock

        client = mongomock.MongoClient()

    collection = client.songs.songs
    collection.create_index("id", unique=True)
    if collection.count_documents({}) == 0:
        data_path = Path(__file__).parent / "data" / "songs.json"
        with data_path.open(encoding="utf-8") as source:
            collection.insert_many(json.load(source))
    return collection


songs = create_collection()


def public_song(document):
    if document is None:
        return None
    return {key: value for key, value in document.items() if key != "_id"}


@app.get("/health")
def health():
    return jsonify(status="OK"), 200


@app.get("/song")
def get_songs():
    return jsonify(songs=[public_song(song) for song in songs.find().sort("id", 1)]), 200


@app.get("/song/<int:song_id>")
def get_song(song_id):
    song = public_song(songs.find_one({"id": song_id}))
    if song is None:
        return jsonify(message="Song not found"), 404
    return jsonify(song), 200


@app.post("/song")
def create_song():
    song = request.get_json(silent=True)
    if not isinstance(song, dict) or not isinstance(song.get("id"), int):
        return jsonify(message="A JSON song with an integer id is required"), 400
    try:
        songs.insert_one(song.copy())
    except DuplicateKeyError:
        return jsonify(message="Song already exists"), 409
    return jsonify(public_song(song)), 201


@app.put("/song/<int:song_id>")
def update_song(song_id):
    changes = request.get_json(silent=True)
    if not isinstance(changes, dict):
        return jsonify(message="A JSON song is required"), 400
    changes.pop("_id", None)
    changes["id"] = song_id
    result = songs.find_one_and_update(
        {"id": song_id}, {"$set": changes}, return_document=ReturnDocument.AFTER
    )
    if result is None:
        return jsonify(message="Song not found"), 404
    return jsonify(public_song(result)), 201


@app.delete("/song/<int:song_id>")
def delete_song(song_id):
    result = songs.delete_one({"id": song_id})
    if result.deleted_count == 0:
        return jsonify(message="Song not found"), 404
    return "", 204
