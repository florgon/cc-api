"""
    Database package for working with DBMS and ORM models.
"""

from app.database.core import db
from . import crud

__all__ = ["db", "crud"]
