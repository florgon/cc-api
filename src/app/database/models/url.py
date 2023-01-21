#!usr/bin/python
"""
    URL Database model.
    Provides URL class that contains where to redirect and other stuff.
"""
from datetime import datetime, timedelta

from flask import current_app
from hashids import Hashids

from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin


class Url(db.Model, CommonMixin, TimestampMixin):
    """
    Shortened URL model.
    """

    redirect = db.Column(db.String, nullable=False)
    expiration_date = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14)
    )
    stats_is_public = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)

    views = db.relationship("UrlView", backref="url", lazy="dynamic", uselist=True)

    @property
    def hash(self) -> str:  # pylint: disable=redefined-builtin
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
