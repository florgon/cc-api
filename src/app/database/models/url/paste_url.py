"""
    URL Database model.
    Provides PasteUrl database model.
"""
from app.database.mixins import UrlMixin, TimestampMixin, CommonMixin
from app.database import db


class PasteUrl(db.Model, CommonMixin, TimestampMixin, UrlMixin):
    """
    Shortened URL model with some text content.
    """

    content = db.Column(db.String(4096), nullable=False)
    burn_after_read = db.Column(db.Boolean, nullable=False, default=False)
    language = db.Column(db.String, nullable=False, server_default="plain")
    views = db.relationship("UrlView", backref="paste", lazy="dynamic", uselist=True)
