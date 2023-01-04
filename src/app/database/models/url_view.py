"""
    URL views database model.
    Provides UrlView class with data of url view after opening url.
"""
from datetime import datetime

from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin


class UrlView(db.Model, CommonMixin, TimestampMixin):
    """
    UrlView model class.
    """

    url_id = db.Column(db.Integer, db.ForeignKey("urls.id"), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    user_agent_id = db.Column(
        db.Integer, db.ForeignKey("user_agents.id"), nullable=False
    )
    referer_id = db.Column(db.Integer, db.ForeignKey("referers.id"), nullable=True)


    @property
    def view_date(self):
        return self.created_at
