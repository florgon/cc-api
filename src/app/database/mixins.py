"""
    Mixins for database tables.
"""
import re
from datetime import datetime, timedelta

from hashids import Hashids
from flask import current_app
from sqlalchemy.orm import declared_attr

from app.database import db



class CommonMixin:
    """
    Mixin that provides basic id primary key and __tablename__ directive.
    """

    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        pattern = re.compile(r"[A-Z][a-z]*")
        return ("_".join(pattern.findall(cls.__name__)) + "s").lower()

    id = db.Column(db.Integer, primary_key=True, nullable=False)


class TimestampMixin:
    """
    Mixin that provides fields related to basic timestamps.
    """

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class UrlMixin:
    """
    Mixin that provides common url features like statisticts.
    """
    expiration_date = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14)
    )
    stats_is_public = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)

    @declared_attr
    def views(self):
        return db.relationship("UrlView", backref="url", lazy="dynamic", uselist=True)

    
    @property
    @declared_attr
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
