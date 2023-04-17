"""
    Provides local User class.
"""
from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin


class User(db.Model, CommonMixin, TimestampMixin):
    """
    Local User with requested from SSO server `user_id`
    """

    user_id = db.Column(db.Integer, nullable=False, unique=True)

    urls = db.relationship("RedirectUrl", backref="user", lazy="dynamic", uselist=True)
    pastes = db.relationship("PasteUrl", backref="user", lazy="dynamic", uselist=True)
