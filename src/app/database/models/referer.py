"""
    Referer database model.
    Provides data about Referers after url opening.
"""
from app.database import db
from app.database.mixins import CommonMixin


class Referer(db.Model, CommonMixin):
    """
    Referer model class.
    """

    referer_value = db.Column(db.String(4096), nullable=False)
    url_views = db.relationship(
        "UrlView", backref="referer", lazy="dynamic", uselist=True
    )
