# Florgon CC API.

![](https://img.shields.io/badge/Florgon%20ecosystem-official-green?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABLFBMVEUAAAAAAAAAAAACAQEqDApfGhVlGxc2Dw0GAgJQUFB6enp2dnZSUlIFAwRjGxfZPTPzTULzUEXjQTaAIx0LAwMAAACIiIhWVlYtLS0fISE+Eg/iRTv1j4fyh3/wjIXzkYruU0lfGhUAAACGhoZLS0sgICAQEhKHIxz2d23yjITzbmXxgHjyeG/2i4OtLiYHAgKOjo6YmJh+fn5ERESZJyD3hn7ydGvzSDzyTkPyXlT2mJG+NCoNBAMAAACFhYUyMjIAAAByHhn0ZlzzoJnyVUryTkLylI32e3GZKCECAQEAAAB+fn4uLi4hCQjENi33dm31oJr0oZv2hHvZQDU7EA4AAAAdHR0LCwsvDQyiKyPYQTfbRDmzMCdFExABAAAIAgIhCQglCgkMBAP///8mzhs8AAAAAWJLR0RjXL4tqgAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAAd0SU1FB+cFEg8gM9Rtk3cAAACHSURBVBjTY2CgDDDCWUwMzCysbOwcEB4nFzcPLx+/gKCQsAiILyomLiEpJS0jKyevoAgSUFJWUVVT19DU0tbR1dMHiRgYGhmbmJqZW1haWdsA+bZ29gwOjk7OLq5u7h6eQAEvbx8GBl8//4DAoOAQkI7QsHAgGREZFR0TG4fkqPiExCQy/QMAIkUS9L41BccAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMDUtMThUMTI6MzI6NTErMDM6MDBjvVo7AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTA1LTE4VDEyOjMyOjUxKzAzOjAwEuDihwAAAABJRU5ErkJggg==)

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
export FLASK_APP=app/app.py:app
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

Docker engine: v20._ \
Docker compose: v2._
