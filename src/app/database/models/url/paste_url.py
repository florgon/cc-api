"""
    URL Database model.
    Provides PasteUrl database model.
"""
from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin, UrlMixin


class PasteUrl(db.Model, CommonMixin, TimestampMixin, UrlMixin):
    """
    Shortened URL model with some text content.
    """

    content = db.Column(db.String(4096), nullable=False)
    burn_after_read = db.Column(db.Boolean, nullable=False, default=False)

    views = db.relationship("UrlView", backref="paste", lazy="dynamic", uselist=True)
