#!usr/bin/python
"""
    URL Database model.
    Provides RedirectUrl class that contains where to redirect and other stuff.
"""
from datetime import datetime, timedelta

from flask import current_app
from hashids import Hashids

from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin, UrlMixin


class RedirectUrl(db.Model, CommonMixin, TimestampMixin, UrlMixin):
    """
    Shortened URL model with redirect to external url.
    """

    redirect = db.Column(db.String, nullable=False)
 
