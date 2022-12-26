"""
    CRUD for UrlView model.
"""

from flask_sqlalchemy import SQLAlchemy

from app.database.models.url import Url
from app.database.models.url_view import UrlView
from app.database import crud


def create(
    db: SQLAlchemy, ip: str, user_agent: str, url: Url, referer: str | None
) -> UrlView:
    """
    Adds url view to `url` with passed params
    :param SQLAlchemy db: database object
    :param str ip: ipv4 user address
    :param str user_agent: user agent from `User-Agent` header
    :param Url url: viewed url
    :param str|None referer: referer from `Referer` header
    :return: created url view
    :rtype: UrlView
    """
    user_agent_object = crud.user_agent.get_or_create(db=db, user_agent=user_agent)
    referer_object_id = None
    if referer:
        referer_object = crud.referer.get_or_create(db=db, referer=referer)
        referer_object_id = referer_object.id

    url_view = UrlView(
        ip=ip,
        user_agent_id=user_agent_object.id,
        url_id=url.id,
        referer_id=referer_object_id,
    )

    db.session.add(url_view)
    db.session.commit()
    db.session.refresh(url_view)

    return url_view
