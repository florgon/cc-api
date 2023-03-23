# pylint: disable=import-outside-toplevel
#!usr/bin/python
"""
    URL shortener API Flask application.
    Used to be run with Gunicorn or externally with Docker.
"""

import logging

from gatey_sdk.integrations.flask import GateyFlaskMiddleware
from gatey_sdk import Client
from flask_cors import CORS
from flask import Flask


def _create_app(for_testing: bool = False) -> Flask:
    """
    Creates initialized Flask Application.
    :param bool for_testing: if true, app uses testing config with testing database.
    """
    _app = Flask(import_name=__name__)
    _app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)
    _app.logger.setLevel(logging.DEBUG)
    _app.logger.debug("Flask logging was hooked up.")

    CORS(_app, resources={r"/*": {"origins": "*"}})

    from app.config import ConfigTesting, Config

    if for_testing:
        _app.config.from_object(ConfigTesting)
    else:
        _app.config.from_object(Config)

    _app.json.sort_keys = False

    from app.database.core import init_with_app

    init_with_app(_app)

    from app.views.utils import bp_utils
    from app.views.urls import bp_urls
    from app.views.pastes import bp_pastes
    from app.exception_handlers import bp_handlers

    PROXY_PREFIX = _app.config["PROXY_PREFIX"]
    _app.register_blueprint(bp_utils, url_prefix=f"{PROXY_PREFIX}/utils")
    _app.register_blueprint(bp_urls, url_prefix=f"{PROXY_PREFIX}/urls")
    _app.register_blueprint(bp_pastes, url_prefix=f"{PROXY_PREFIX}/pastes")
    _app.register_blueprint(bp_handlers)

    return _app


app: Flask = _create_app()
