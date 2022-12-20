#!usr/bin/python
"""
    URL shortener API Flask application.
    Used to be run with Gunicorn or externally with Docker.
"""

from flask import Flask
from flask_cors import CORS


def _create_app() -> Flask:
    """
    Creates initialized Flask Application.
    """
    app = Flask(import_name=__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    from app.config import ConfigDevelopment

    app.config.from_object(ConfigDevelopment)

    from app.database.core import init_with_app

    init_with_app(app)

    from app.views.utils import bp_utils
    from app.views.url import bp_url
    from app.exception_handlers import bp_handlers
    
    PROXY_PREFIX = app.config["PROXY_PREFIX"]
    app.register_blueprint(bp_utils, url_prefix=f"{PROXY_PREFIX}/utils")
    app.register_blueprint(bp_url, url_prefix=f"{PROXY_PREFIX}/url")
    app.register_blueprint(bp_handlers)

    return app


app: Flask = _create_app()
