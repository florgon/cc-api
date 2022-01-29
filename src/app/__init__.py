#!env/bin/python
"""
    URL shortener application.
    Provides full application via 'create()' that returns ready to be runned application.
"""

from flask import Flask


__author__ = "Kirill Zhosul"
__copyright = "(c) 2022 Kirill Zhosul"
__license__ = "MIT"


def create(name=None) -> Flask:
    """
    Returns ready to be runned application.
    :param: name Flask import_name, preferred to be omitted.
    :return: Flask application.
    """
    app = Flask(name if name else __name__)

    from . import config
    app.config.from_object(config.ConfigDevelopment)

    return app
