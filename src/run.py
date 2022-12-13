#!usr/bin/python
"""
    URL shortener application runner.
    Runs the Flask application.
"""
from app.config import ConfigDevelopment
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(ConfigDevelopment)

    from app.views.utils import bp_utils
    app.register_blueprint(bp_utils)

    return app
