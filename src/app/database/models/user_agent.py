"""
    User agent database model.
    Provides data about User-Agents after url opening.
"""
from app.database import db
from app.database.mixins import CommonMixin

class UserAgent(db.Model, CommonMixin):
    """
    UserAgent model class.
    """

    user_agent_value = db.Column(db.String(4096), nullable=False)
    url_views = db.relationship(
        "UrlView", backref="user_agent", lazy="dynamic", uselist=True
    )
