"""
    User agent database model.
    Provides data about User-Agents after url opening.
"""
from app.database import db


class UserAgent(db.Model):
    """
    UserAgent model class.
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_agent_value = db.Column(db.String(4096), nullable=False)
    url_views = db.relationship(
        "UrlView", backref="user_agent", lazy="dynamic", uselist=True
    )
