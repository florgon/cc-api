# Florgon CC API.

### Description.

API server for Florgon CC API (Links shortener API).

### Features.

- Shortify URLs
- Open short URLs
- Track URLs statistics
- Get QR codes for URLs

### See in action.

API deployed and used in production [here](https://api-cc.florgon.space/v1) (API endpoint).

### Technologies.

- Python (Flask, SQLAlchemy)
- PostgreSQL (with pgBouncer)
- Docker (with Docker-Compose)
- Gunicorn
- PyTest

### Documentation.
TBD: Document.

#### How to run.
```
cd src && docker-compose up
```

#### How to apply migrations.
When you do first start you should apply migrations to the DBMS.
```
cd src
docker-compose up -d
docker exec -it florgon-api-cc-server-1 /bin/sh
EXPORT FLASK_APP=app/app.py:app
flask db upgrade
```

#### How to configure.
Please edit `src/.server.env`, all configuration are fetched on startup to `src/app/config.py`

#### Development.
To run tests (`pytest`) against running instance.
```
docker exec -it florgon-api-cc-server-1 /bin/sh
pytest .
```
To do formatting before push.
```
black .
```
There is CI that is using `mypy` with `pylint`

# Tested on...

Docker engine: v20.* \
Docker compose: v2.*
