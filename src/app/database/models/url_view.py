"""
    URL views database model.
    Provides UrlView class with data of url view after opening url.
"""
from datetime import datetime

from app.database import db


class UrlView(db.Model):
    """
    UrlView model class.
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    url_id = db.Column(db.Integer, db.ForeignKey("url.id"), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    user_agent_id = db.Column(
        db.Integer, db.ForeignKey("user_agent.id"), nullable=False
    )
    referer_id = db.Column(db.Integer, db.ForeignKey("referer.id"), nullable=True)
    view_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
