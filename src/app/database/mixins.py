"""
    Mixins for database tables.
"""
import re

from sqlalchemy.orm import declared_attr

from app.database import db


class CommonMixin():
    """
    Mixin that provides basic id primary key and __tablename__ directive.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        pattern = re.compile(r"[A-Z][a-z]*")
        return ("_".join(pattern.findall(cls.__name__)) + "s").lower()


    id = db.Column(db.Integer, primary_key=True, nullable=False)


