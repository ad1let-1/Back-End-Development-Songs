# Back-End-Development-Songs

This is the public README for my **Back-End-Development-Songs** repository:
https://github.com/ad1let-1/Back-End-Development-Songs/blob/main/README.md

Flask and MongoDB song catalogue service for Djirection. Based on the IBM Skills Network course template, licensed under Apache 2.0. It implements the REST endpoints and seeds the catalogue from `backend/data/songs.json` when the collection is empty.

## Run locally

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m flask --app app run --port 8081
```

On Windows, use `.venv\\Scripts\\python.exe`. When `MONGODB_SERVICE` is unset, a MongoDB-compatible in-memory collection is used for a local demonstration. For MongoDB, set `MONGODB_SERVICE` to the host and port and, if required, set `MONGODB_USERNAME` and `MONGODB_PASSWORD`.

## API

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/health` | Returns `{"status":"OK"}` |
| GET | `/song` | Lists songs under `songs` |
| GET | `/song/<id>` | Returns one song |
| POST | `/song` | Creates a song |
| PUT | `/song/<id>` | Updates a song |
| DELETE | `/song/<id>` | Removes a song |

Example:

```sh
curl -i http://127.0.0.1:8081/health
curl -i http://127.0.0.1:8081/song
```
