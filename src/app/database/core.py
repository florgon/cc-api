"""
    Database core sessions / sessionmakers and migrations.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask


def init_with_app(app: Flask) -> None:
    """
    Initializes database requirements with Flask app by connecting ORM and running migrations if required.
    """
    db.init_app(app)
    migrate.init_app(app, db)


db = SQLAlchemy()
migrate = Migrate()
