#!usr/bin/python
"""
    Config files for app configuration.
    Contains several classes for the
"""

# Used for database path generation.
import os


# Base config.
class Config(object):
    SECRET_KEY = "hfd;g784r8hfigrjeunvior;e9trt964u8c73459w3;09byn904yboi4evuc;t"
    FLASK_SECRET_KEY = SECRET_KEY
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DSN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Config, that should be used for development purposes.
class ConfigDevelopment(Config):
    DEBUG = True


# Config, that should be used for production.
class ConfigProduction(Config):
    DEBUG = False
