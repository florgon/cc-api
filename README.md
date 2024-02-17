<h1 align="center">:monkey_face: Florgon CC API.</h1>

<p align="center">
  <img src="https://www.gnu.org/graphics/agplv3-88x31.png" />
  <img src="https://img.shields.io/badge/Florgon%20ecosystem-official-green?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABLFBMVEUAAAAAAAAAAAACAQEqDApfGhVlGxc2Dw0GAgJQUFB6enp2dnZSUlIFAwRjGxfZPTPzTULzUEXjQTaAIx0LAwMAAACIiIhWVlYtLS0fISE+Eg/iRTv1j4fyh3/wjIXzkYruU0lfGhUAAACGhoZLS0sgICAQEhKHIxz2d23yjITzbmXxgHjyeG/2i4OtLiYHAgKOjo6YmJh+fn5ERESZJyD3hn7ydGvzSDzyTkPyXlT2mJG+NCoNBAMAAACFhYUyMjIAAAByHhn0ZlzzoJnyVUryTkLylI32e3GZKCECAQEAAAB+fn4uLi4hCQjENi33dm31oJr0oZv2hHvZQDU7EA4AAAAdHR0LCwsvDQyiKyPYQTfbRDmzMCdFExABAAAIAgIhCQglCgkMBAP///8mzhs8AAAAAWJLR0RjXL4tqgAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAAd0SU1FB+cFEg8gM9Rtk3cAAACHSURBVBjTY2CgDDDCWUwMzCysbOwcEB4nFzcPLx+/gKCQsAiILyomLiEpJS0jKyevoAgSUFJWUVVT19DU0tbR1dMHiRgYGhmbmJqZW1haWdsA+bZ29gwOjk7OLq5u7h6eQAEvbx8GBl8//4DAoOAQkI7QsHAgGREZFR0TG4fkqPiExCQy/QMAIkUS9L41BccAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMDUtMThUMTI6MzI6NTErMDM6MDBjvVo7AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTA1LTE4VDEyOjMyOjUxKzAzOjAwEuDihwAAAABJRU5ErkJggg==" />
</p>

RESTful API for Florgon url shortener && paste manager (Florgon CC API). Integrated with Florgon SSO. ***100% free software***

**WARNING!** This version is experimental and may be not comfortable to user. This version contains basic auth procedure instead of Florgon SSO (independent auth). This version is temporary, because basic auth is not secure.

## I want to test it!

API deployed and used in production [here](https://api-cc.florgon.com/v1) (API endpoint).

You can install *Florgon CC CLI* (Command line interface) [here](https://github.com/stepanzubkov/florgon-cc-cli). It is in beta stage.

*Florgon CC web* interface is hosted [here](https://cc.florgon.com/). I **don't** recommend use it, because it is in alpha stage and it is nonfree service. Many features may not work.

## Features

**Url shortener**

Create unlimited short urls anonymously or logged in. Every short url will be expired after 2 weeks. 

If you are logged in via Florgon SSO, you can **delete** your url or check **statistics** about url views. You can also make stats public.

**Paste manager**

Create unlimited text pastes anonymously or logged in. Every paste also will be expired after 2 weeks. You can also specify programming language of paste and **syntax highlighting** will be work in all clients.

You can delete paste or check stats as well as short urls.

## Run && deploy

Clone this repository, then:
```bash
cd cc-api/src
docker-compose up --build
```
When you do first start you should apply migrations to the DBMS.
```bash
docker-compose exec server sh
export FLASK_APP=app/app.py
flask db upgrade
```

### Configuration

Please edit `src/.server.env`, all configuration are fetched on startup to `src/app/config.py`.

DB config are stored in `src/.database.env`.

Docker settings is `src/.env`.

### Deployment

You should configure nginx server to run this api in production. Gunicorn are already configured in Dockerfile.

## Documentation

Documentation will be soon...

## Technologies

Written mostly in Python 3.10+

Main framework: flask

DBMS: PostgreSQL

API also uses Redis as broker.

API, DB and Redis runs in docker containers, using docker compose.

Other dependencies are stored in `requirements.txt`.

## Tested on...

Docker engine: v20._ \
Docker compose: v2._ \
Python: 3.10, 3.11

## License

SPDX-License-Identifier: AGPLv3-or-later

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

## Contribution

Feel free to contribute to this program. You can send issue, submit a pull request. You can also email me (`stepanzubkov@florgon.com`).

## Support

If you are from Russia, you can support me by sending some money [using this link](https://www.tinkoff.ru/rm/zubkov.stepan27/FGvQQ98452).


