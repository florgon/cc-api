#!usr/bin/python
"""
    Config files.
"""

import os


class Config:
    SECRET_KEY = "hfd;g784r8hfigrjeunvior;e9trt964u8c73459w3;09byn904yboi4evuc;t"
    FLASK_SECRET_KEY = SECRET_KEY
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DSN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HASHIDS_SALT = os.getenv(
        "HASHIDS_SALT",
        "gij5uy58yurhgirhigujewiohgihgdjh48ty684yu93tui3hithivhfk3kfm4khni3h4ijiojfuhug3n4ggflorgonojfikdjsigsbhduig",
    )
    PROXY_PREFIX = os.getenv("PROXY_PREFIX", "/v1")

    GATEY_CLIENT_SECRET = os.getenv("GATEY_CLIENT_SECRET")
    GATEY_SERVER_SECRET = os.getenv("GATEY_SERVER_SECRET")


# Config, that should be used for development purposes.
class ConfigDevelopment(Config):
    DEBUG = True


# Config, that should be used for production.
class ConfigProduction(Config):
    DEBUG = False
