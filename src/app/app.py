#!usr/bin/python
"""
    URL shortener API Flask application.
    Used to be run with Gunicorn or externally with Docker.
"""

from flask import Flask
from flask_cors import CORS

from gatey_sdk.integrations.flask import GateyFlaskMiddleware
from gatey_sdk import Client, PrintTransport


def _create_app() -> Flask:
    """
    Creates initialized Flask Application.
    """
    app = Flask(import_name=__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    from app.config import ConfigDevelopment

    app.config.from_object(ConfigDevelopment)
    app.json.sort_keys = False

    from app.database.core import init_with_app

    init_with_app(app)

    from app.views.utils import bp_utils
    from app.views.urls import bp_urls
    from app.exception_handlers import bp_handlers

    PROXY_PREFIX = app.config["PROXY_PREFIX"]
    app.register_blueprint(bp_utils, url_prefix=f"{PROXY_PREFIX}/utils")
    app.register_blueprint(bp_urls, url_prefix=f"{PROXY_PREFIX}/urls")
    app.register_blueprint(bp_handlers)

    client = Client(
        include_platform_info=True,
        include_runtime_info=True,
        include_sdk_info=True,
        handle_global_exceptions=True,
        exceptions_capture_code_context=True,
        client_secret=app.config["GATEY_CLIENT_SECRET"],
        server_secret=app.config["GATEY_SERVER_SECRET"],
        project_id=app.config["GATEY_PROJECT_ID"],
    )
    app.wsgi_app = GateyFlaskMiddleware(
        app.wsgi_app,
        client=client,
        capture_requests_info=False,
        client_getter=None,
        capture_exception_options=None,
    )

    return app


app: Flask = _create_app()
