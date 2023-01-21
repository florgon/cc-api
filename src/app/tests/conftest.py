"""
    Pytest custom fixtures.
"""
import pytest
from flask import Flask

from app.app import _create_app
from app.database import db


@pytest.fixture()
def app():  # pylint: disable=redefined-outer-name
    """
    Flask core application.
    """
    _app: Flask = _create_app(for_testing=True)
    with _app.app_context():
        db.create_all()
        print("All tables in testing database was successfully created!")

        yield _app

        db.session.remove()
        db.drop_all()
        print("All tables in testing database was successfully dropped!")

@pytest.fixture()
def client(app):  # pylint: disable=redefined-outer-name
    """
    HTTP Client.
    """
    return app.test_client()


@pytest.fixture()
def runner(app):  # pylint: disable=redefined-outer-name
    """
    CLI runner.
    """
    return app.test_cli_runner()
