#!usr/bin/python
"""
    URL shortener views.
"""

from flask import Flask


def register(app: Flask) -> None:
    """
    Registers all views blueprints.
    :param: app Flask application.
    """
    from . import root

    app.register_blueprint(root.bp_root)
