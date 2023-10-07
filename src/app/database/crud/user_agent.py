"""
    CRUD for UserAgent database model.
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


from flask_sqlalchemy import SQLAlchemy

from app.database.models.user_agent import UserAgent


def get_or_create(db: SQLAlchemy, user_agent: str) -> UserAgent:
    """
    Return UserAgent object if there is one in DB, else create it.
    :param SQLAlchemy db: database object
    :param str user_agent: user agent from `User-Agent` header
    :return: UserAgent object
    :rtype: UserAgent
    """
    user_agent_object = UserAgent.query.filter_by(user_agent_value=user_agent).first()
    if user_agent_object is None:
        user_agent_object = UserAgent(user_agent_value=user_agent)
        db.session.add(user_agent_object)
        db.session.commit()
        db.session.refresh(user_agent_object)

    return user_agent_object
