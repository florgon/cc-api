"""
    Provides local User class.
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
from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin


class User(db.Model, CommonMixin, TimestampMixin):
    """
    Local User with requested from SSO server `user_id`
    """

    user_id = db.Column(db.Integer, nullable=False, unique=True)

    urls = db.relationship("RedirectUrl", backref="user", lazy="dynamic", uselist=True)
    pastes = db.relationship("PasteUrl", backref="user", lazy="dynamic", uselist=True)