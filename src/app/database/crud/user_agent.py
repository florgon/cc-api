"""
    CRUD for UserAgent database model.
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
    user_agent_object = UserAgent.query.filter_by(value=user_agent).first()
    if user_agent_object is None:
        user_agent_object = UserAgent(value=UserAgent)
        db.session.add(user_agent_object)
        db.session.commit()
        db.session.refresh(user_agent_object)

    return user_agent_object
