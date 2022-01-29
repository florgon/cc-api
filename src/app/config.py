#!usr/bin/python
"""
    Config files for app configuration.
    Contains several classes for the
"""


# Base config.
class Config(object):
    SECRET_KEY = "very-strong-secret-key-for-hackers"
    FLASK_SECRET_KEY = SECRET_KEY
    DEBUG = False


# Config, that should be used for development purposes.
class ConfigDevelopment(Config):
    DEBUG = True


# Config, that should be used for production.
class ConfigProduction(Config):
    DEBUG = False
