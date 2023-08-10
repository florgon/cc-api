"""
    URL Database model.
    Provides PasteUrl database model.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from app.database.mixins import UrlMixin, TimestampMixin, CommonMixin
from app.database import db


class PasteUrl(db.Model, CommonMixin, TimestampMixin, UrlMixin):
    """
    Shortened URL model with some text content.
    """

    content = db.Column(db.String(4096), nullable=False)
    burn_after_read = db.Column(db.Boolean, nullable=False, default=False)
    language = db.Column(db.String, nullable=False, server_default="plain")
    views = db.relationship("UrlView", backref="paste", lazy="dynamic", uselist=True)
