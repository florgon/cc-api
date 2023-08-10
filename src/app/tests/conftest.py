"""
    Pytest custom fixtures.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
