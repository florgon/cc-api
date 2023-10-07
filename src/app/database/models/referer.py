"""
    Referer database model.
    Provides data about Referers after url opening.
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
from app.database.mixins import CommonMixin


class Referer(db.Model, CommonMixin):
    """
    Referer model class.
    """

    referer_value = db.Column(db.String(4096), nullable=False)
    url_views = db.relationship(
        "UrlView", backref="referer", lazy="dynamic", uselist=True
    )
