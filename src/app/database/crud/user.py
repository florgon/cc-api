"""
    CRUD for User database model.
"""
from flask_sqlalchemy import SQLAlchemy
from app.database.models.user import User


def get_or_create(db: SQLAlchemy, user_id: int) -> User:
    user = get_by_user_id(user_id=user_id)
    if not user:
        user = create(db=db, user_id=user_id)

    return user


def create(db: SQLAlchemy, user_id: int) -> User:
    """
    Creates local User with SSO User's user_id and returns created object.
    :param SQLAlchemy db: database object
    :param int user_id: SSO User's id
    :rtype: User
    """
    user = User(user_id=user_id)

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return user


def get_by_user_id(user_id: int) -> User | None:
    """
    Returns local User with specified user_id.
    :param int user_id: SSO User's id
    :rtype: User or None
    """
    user = User.query.filter_by(user_id=user_id).first()
    return user
