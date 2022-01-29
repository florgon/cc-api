#!usr/bin/python
"""
    URL Database model.
    Provides URL class that contains where to redirect and other stuff.
"""

from .. import db


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    views = db.Column(db.Integer, nullable=False, default=0)
    redirect = db.Column(db.String, nullable=False)

    def __init__(self, url):
        """
        URL Database model constructor.
        :param url:
        """
        self.views = 0
        self.redirect = url
