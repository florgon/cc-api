#!usr/bin/python
"""
    URL shortener API Flask application.
    Used to be run with Gunicorn or externally with Docker.
"""

from flask import Flask
from flask_cors import CORS

from gatey_sdk.integrations.flask import GateyFlaskMiddleware
from gatey_sdk import Client


def _create_app() -> Flask:
    """
    Creates initialized Flask Application.
    """
    _app = Flask(import_name=__name__)
    CORS(_app, resources={r"/*": {"origins": "*"}})

    from app.config import ConfigDevelopment  # pylint: disable=import-outside-toplevel

    _app.config.from_object(ConfigDevelopment)
    _app.json.sort_keys = False

    from app.database.core import (
        init_with_app,
    )  # pylint: disable=import-outside-toplevel

    init_with_app(_app)

    from app.views.utils import bp_utils  # pylint: disable=import-outside-toplevel
    from app.views.urls import bp_urls  # pylint: disable=import-outside-toplevel
    from app.exception_handlers import (
        bp_handlers,
    )  # pylint: disable=import-outside-toplevel

    PROXY_PREFIX = _app.config["PROXY_PREFIX"]
    _app.register_blueprint(bp_utils, url_prefix=f"{PROXY_PREFIX}/utils")
    _app.register_blueprint(bp_urls, url_prefix=f"{PROXY_PREFIX}/urls")
    _app.register_blueprint(bp_handlers)

    client = Client(
        include_platform_info=True,
        include_runtime_info=True,
        include_sdk_info=True,
        handle_global_exceptions=True,
        exceptions_capture_code_context=True,
        client_secret=_app.config["GATEY_CLIENT_SECRET"],
        server_secret=_app.config["GATEY_SERVER_SECRET"],
        project_id=_app.config["GATEY_PROJECT_ID"],
    )
    _app.wsgi_app = GateyFlaskMiddleware(
        _app.wsgi_app,
        client=client,
        capture_requests_info=False,
        client_getter=None,
        capture_exception_options=None,
    )

    return _app


app: Flask = _create_app()
