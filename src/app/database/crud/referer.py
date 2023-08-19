"""
    CRUD for Referer database model.
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
from flask_sqlalchemy import SQLAlchemy

from app.database.models.referer import Referer


def get_or_create(db: SQLAlchemy, referer: str) -> Referer:
    """
    Returns Referer object if there is one in DB, else create it.
    :param SQLAlchemy db: database object
    :param str referer: referer from `Referer` header
    :return: Referer object
    :rtype: Referer
    """
    referer_object = Referer.query.filter_by(referer_value=referer).first()
    if referer_object is None:
        referer_object = Referer(referer_value=referer)
        db.session.add(referer_object)
        db.session.commit()
        db.session.refresh(referer_object)

    return referer_object
