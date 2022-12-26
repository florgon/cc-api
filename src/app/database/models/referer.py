"""
    Referer database model.
    Provides data about Referers after url opening.
"""
from app.database import db


class Referer(db.Model):
    """
    Referer model class.
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    referer_value = db.Column(db.String(4096), nullable=False)
    url_views = db.relationship(
        "UrlView", backref="referer", lazy="dynamic", uselist=True
    )
