"""
    URL views database model.
    Provides UrlView class with data of url view after opening url.
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

from app.database import db
from app.database.mixins import CommonMixin, TimestampMixin


class UrlView(db.Model, CommonMixin, TimestampMixin):
    """
    UrlView model class.
    """

    url_id = db.Column(db.Integer, db.ForeignKey("redirect_urls.id"), nullable=True)
    paste_id = db.Column(db.Integer, db.ForeignKey("paste_urls.id"), nullable=True)
    ip = db.Column(db.String(15), nullable=False)
    user_agent_id = db.Column(
        db.Integer, db.ForeignKey("user_agents.id"), nullable=False
    )
    referer_id = db.Column(db.Integer, db.ForeignKey("referers.id"), nullable=True)

    @property
    def view_date(self):
        """
        Date when user viewed url.
        """
        return self.created_at
