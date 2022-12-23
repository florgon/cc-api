"""
    Checks database connection.
"""
from sqlalchemy import text

from app.database.core import db

def test_connection(client):
    expected = 64
    actual = db.session.execute(text(f"SELECT {expected}")).fetchall()[0][0]
    assert actual == expected

