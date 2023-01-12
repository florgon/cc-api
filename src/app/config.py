"""
    Config files.
"""

import os


class Config:
    """
    Base config for app.
    """

    SECRET_KEY = "hfd;g784r8hfigrjeunvior;e9trt964u8c73459w3;09byn904yboi4evuc;t"
    FLASK_SECRET_KEY = SECRET_KEY

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HASHIDS_SALT = os.getenv(
        "HASHIDS_SALT",
        "gij5uy58yurhgirhigujewiohgihgdjh48ty684yu93tui3hithivhfk3kfm4khni3h4ijiojfuhug3n4ggflorgonojfikdjsigsbhduig",
    )
    PROXY_PREFIX = os.getenv("PROXY_PREFIX", "/v1")

    GATEY_CLIENT_SECRET = os.getenv("GATEY_CLIENT_SECRET")
    GATEY_SERVER_SECRET = os.getenv("GATEY_SERVER_SECRET")
    GATEY_PROJECT_ID = int(os.getenv("GATEY_PROJECT_ID", "4"))

    SSO_API_URL = "https://api.florgon.space"
    SSO_API_METHOD = "secure.checkAccessToken"


class ConfigDevelopment(Config):
    """
    Config, that should be used for development purposes.
    """

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DSN")

class ConfigProduction(Config):
    """
    Config, that should be used for production.
    """

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DSN")

class ConfigTesting(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_DSN")
