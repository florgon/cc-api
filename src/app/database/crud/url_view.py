"""
    CRUD for UrlView model.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

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


def delete_by_url_id(db: SQLAlchemy, url_id: int) -> None:
    """
    Deletes url views with specified url_id.
    :param SQLAlchemy db: database object
    :param int url_id: id of short url
    """
    UrlView.query.filter_by(url_id=url_id).delete()

    db.session.commit()


def get_by_dates(db: SQLAlchemy, url_id: int, value_as: str = "percent") -> dict[str, int]:
    """
    Return url views count or percentage by dates.
    :param SQLAlchemy db: database object
    :param int url_id: id of short url
    :param str value_as: controls how to present value of views. Can be:
        `percent` - (default) percentage of views. Return value can be from 1 to 100.
        `number` - number of views.
    :return: dict like {'23-09-2023': 23, '24-09-2023': 12, ...}
    :rtype: dict[str, int]
    """
    dates = (
        db.session.query(func.date(UrlView.created_at), func.count())
        .filter_by(url_id=url_id)
        .group_by(func.date(UrlView.created_at))
        .all()
    )
    all_views_count = sum(x[1] for x in dates)
    if value_as == "percent":
        formatted_dates = {str(x[0]): _get_percentage(all_views_count, x[1]) for x in dates}
    else:
        formatted_dates = dict(dates)
    
    return formatted_dates


def _get_percentage(whole: int, part: int) -> int:
    """
    Returns the percentage of a part of the whole.
    """
    return round(part / whole * 100)

