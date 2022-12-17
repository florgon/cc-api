#!usr/bin/python
"""
    URL Database model.
    Provides URL class that contains where to redirect and other stuff.
"""
from datetime import datetime

from app.database import db


class Url(db.Model):
    """
    Shortened URL model.
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    views = db.Column(db.Integer, nullable=False, default=0)
    redirect = db.Column(db.String, nullable=False)
    expiration_date = db.Column(db.DateTime, default=datetime.utcnow())
