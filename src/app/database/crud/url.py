"""
    Url CRUD utils for the database.
"""
from flask_sqlalchemy import SQLAlchemy

from app.database.models.url import Url


def create_url(db: SQLAlchemy, redirect_url: str) -> Url:
    """
    Creates new shortened url in database.
    :param SQLAlchemy db: database object
    :param str redirect_url: long url for redirecting
    :return: created url object
    :rtype: Url
    """
    url = Url(
        redirect=redirect_url,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url
