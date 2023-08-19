"""
    Config files.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os


class Config:
    """
    Base config for app.
    """

    DEBUG = bool(int(os.getenv("DEBUG", "1")))

    SECRET_KEY = os.getenv(
        "FLASK_SECRET_KEY",
        "hfd;g784r8hfigrjeunvior;e9trt964u8c73459w3;09byn904yboi4evuc;t",
    )
    FLASK_SECRET_KEY = SECRET_KEY

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DSN")

    HASHIDS_SALT = os.getenv(
        "HASHIDS_SALT",
        "gij5uy58yurhgirhigujewiohgihgdjh48ty684yu93tui3hithivhfk3kfm4khni3h4ijiojfuhug3n4ggflorgonojfikdjsigsbhduig",
    )
    PROXY_PREFIX = os.getenv("PROXY_PREFIX", "/v1")

    GATEY_IS_ENABLED = bool(int(os.getenv("GATEY_IS_ENABLED", "0")))
    GATEY_CLIENT_SECRET = os.getenv("GATEY_CLIENT_SECRET", "")
    GATEY_SERVER_SECRET = os.getenv("GATEY_SERVER_SECRET", "")
    GATEY_PROJECT_ID = int(os.getenv("GATEY_PROJECT_ID", "0"))

    SSO_API_URL = "https://api.florgon.com/v1"
    SSO_API_METHOD = "tokens/check"

    # If you are deploying API on other domain, you should change it
    API_HOSTNAME = os.getenv("API_HOSTNAME", "api-cc.florgon.com")
    # May be http, https
    API_SCHEME = os.getenv("API_SCHEME", "https")


class ConfigTesting(Config):
    """
    Config that should uses in tests.
    """

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_DSN")  # noqa
