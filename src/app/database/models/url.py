#!usr/bin/python
"""
    URL Database model.
    Provides URL class that contains where to redirect and other stuff.
"""
from datetime import datetime, timedelta

from flask import request, current_app
from hashids import Hashids

from app.database import db


class Url(db.Model):
    """
    Shortened URL model.
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    views = db.Column(db.Integer, nullable=False, default=0)
    redirect = db.Column(db.String, nullable=False)
    expiration_date = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14)
    )
    stats_is_public = db.Column(db.Boolean, default=False)

    @property
    def hash(self) -> str:
        """
        Returns hash based on model id.
        :rtype: str
        """
        hashids = Hashids(salt=current_app.config["HASHIDS_SALT"], min_length=6)
        return hashids.encode(self.id)


    def is_expired(self) -> bool:
        """
        Checks if url is expired.
        :rtype: bool
        """
        return self.expiration_date <= datetime.now()
