#!usr/bin/python
"""
    URL shortener application runner.
    Runs the Flask application.
"""
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    from app.config import ConfigDevelopment
    app.config.from_object(ConfigDevelopment)

    from app.models.db import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from app.views.utils import bp_utils
    app.register_blueprint(bp_utils)

    return app


app = create_app()

