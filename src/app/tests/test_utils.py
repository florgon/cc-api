"""
    Tests for utils views.
"""
import pytest
from flask import Flask, url_for

from app.app import _create_app

@pytest.fixture()
def app():
    app: Flask = _create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app): # pylint: disable=redefined-outer-name
    return app.test_client()


@pytest.fixture() 
def runner(app): # pylint: disable=redefined-outer-name
    return app.test_cli_runner()


def test_read_utils_get_server_time(client): # pylint: disable=redefined-outer-name
    response = client.get(url_for("get_server_time"))

    assert response.status == 200
    assert "v" in response.json()
    assert "success" in response.json()
    assert "server_time" in response.json()["success"]
