"""
    Pytest custom fixtures.
"""
import pytest
from flask import Flask

from app.app import _create_app


@pytest.fixture()
def app():
    app: Flask = _create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):  # pylint: disable=redefined-outer-name
    return app.test_client()


@pytest.fixture()
def runner(app):  # pylint: disable=redefined-outer-name
    return app.test_cli_runner()
