#!env/bin/python
"""
    URL shortener application.
    Provides full application via 'create()' that returns ready to be runned application.
"""

from flask import Flask

__author__ = "Kirill Zhosul"
__copyright = "(c) 2022 Kirill Zhosul"
__license__ = "MIT"


def create() -> Flask:
    app = Flask(__name__)

    return app
