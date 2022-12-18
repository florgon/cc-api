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

    @property
    def short_url(self):
        """
        Returns short url with hash based on model id.
        """
        hashids = Hashids(salt=current_app.config["HASHIDS_SALT"])
        return f"{request.host_url}c/{hashids.encode(self.id)}"
