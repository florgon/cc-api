# syntax=docker/dockerfile:1
FROM python:3.10.7-alpine

# Disable python buffering and bytecode *.pyc compiling. 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Project directory on the container.
WORKDIR /srv

# Install requirements.
COPY requirements.txt /srv/
RUN pip install --upgrade pip && \
    pip install --upgrade --no-cache-dir -r requirements.txt

# Copy whole project to the container.
COPY . /srv/

# Run project after building.
CMD ["gunicorn", "-w", "4", "--reload", "-b", "0.0.0.0:80", "app.app:app"]
