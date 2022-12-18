#!usr/bin/python
"""
    URL shortener API Flask application.
    Used to be run with Gunicorn or externally with Docker.
"""

from flask import Flask


def _create_app() -> Flask:
    """
    Creates initialized Flask Application.
    """
    app = Flask(import_name=__name__)

    from app.config import ConfigDevelopment

    app.config.from_object(ConfigDevelopment)

    from app.database.core import init_with_app

    init_with_app(app)

    from app.views.utils import bp_utils
    from app.views.url import bp_url

    app.register_blueprint(bp_utils, url_prefix="/utils")
    app.register_blueprint(bp_url, url_prefix="/url")

    return app


app: Flask = _create_app()