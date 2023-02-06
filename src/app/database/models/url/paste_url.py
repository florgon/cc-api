"""
    URL Database model.
    Provides PasteUrl database model.
"""
from datetime import datetime, timedelta

from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin, UrlMixin

class PasteUrl(db.Model, CommonMixin, TimestampMixin, UrlMixin):
    """
    Shortened URL model with some text content.
    """
    content = db.Column(db.Text, nullable=False)

