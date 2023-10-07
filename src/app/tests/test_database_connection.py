"""
    Checks database connection.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from sqlalchemy import text

from app.database.core import db


def test_connection(app):
    """
    Tests connection to the database via SELECT query.
    """
    expected = 64
    with app.app_context():
        actual = db.session.execute(text(f"SELECT {expected}")).fetchall()[0][0]

    assert actual == expected
