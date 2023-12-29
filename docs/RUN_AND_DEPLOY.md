# Run and Deploy

**Docker** and **docker compose** are needed to run this API.

Clone this repository, then:
```bash
cd cc-api/src
touch .env
docker-compose up --build
```
When you do first start, you should apply migrations to the DBMS.
```bash
docker-compose exec server sh
export FLASK_APP=app/app.py
flask db upgrade
exit
```

## Tests

Run tests with:
```bash
docker-compose exec server pytest .
```

## Technical details

### Docker

To run this application with docker, files `Dockerfile`, `docker-compose.yml` are used.

`Dockerfile` uses `gunicorn` to run API application. Dockerfile uses Alpine Linux with python.

`docker-compose.yml` contains services needed for API (database, database-poller and main API server service)

database service uses **Postgres** as a main DBMS.

#### Configuration

Config for docker stored in `src/.env` file. There are some settings you should set:

**COMPOSE_PROJECT_NAME** - project name. I recommend set it to "florgon-cc-api".

**COMPOSE_EXPOSED_PORT** - API port. This docs assumes that port is 80 (default http port)

### Nginx

This API doesn't come with nginx configuration.
