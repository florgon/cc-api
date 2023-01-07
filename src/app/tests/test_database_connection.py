"""
    Checks database connection.
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
