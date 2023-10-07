"""
    Mixins for database tables.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re
from datetime import datetime, timedelta

from hashids import Hashids
from flask import current_app
from sqlalchemy.orm import declared_attr

from app.database import db


class CommonMixin:
    """
    Mixin that provides basic id primary key and __tablename__ directive.
    """

    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        pattern = re.compile(r"[A-Z][a-z]*")
        return ("_".join(pattern.findall(cls.__name__)) + "s").lower()

    id = db.Column(db.Integer, primary_key=True, nullable=False)


class TimestampMixin:
    """
    Mixin that provides fields related to basic timestamps.
    """

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class UrlMixin:
    """
    Mixin that provides common url features like statisticts.
    """

    expiration_date = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14)
    )
    is_deleted = db.Column(db.Boolean, default=False)
    stats_is_public = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)

    @property
    def hash(self) -> str:  # pylint: disable=redefined-builtin
        """
        Returns hash based on model id.
        :rtype: str
        """
        hashids = Hashids(salt=current_app.config["HASHIDS_SALT"], min_length=6)
        return hashids.encode(self.id)

    def is_expired(self) -> bool:
        """
        Checks if url is expired.
        :rtype: bool
        """
        return self.expiration_date <= datetime.now()
