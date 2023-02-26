"""
    CRUD for UrlView model.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

from app.database.models.url import RedirectUrl, PasteUrl
from app.database.models.url_view import UrlView
from app.database.models.referer import Referer
from app.database import crud


def create(
    db: SQLAlchemy,
    ip: str,
    user_agent: str,
    url: RedirectUrl | None = None,
    paste: PasteUrl | None = None,
    referer: str | None = None,
) -> UrlView:
    """
    Adds url view to `url` with passed params
    :param SQLAlchemy db: database object
    :param str ip: ipv4 user address
    :param str user_agent: user agent from `User-Agent` header
    :param RedirectUrl|None url: viewed url
    :param PasteUrl|None paste: viewed paste
    :param str|None referer: referer from `Referer` header
    :return: created url view
    :rtype: UrlView
    :raises TypeError: if passed both url 
    """
    if (url, paste).count(None) != 1:
        raise TypeError("Pass only url or only paste (not both)!")

    user_agent_object = crud.user_agent.get_or_create(db=db, user_agent=user_agent)
    referer_object_id = None
    if referer:
        referer_object = crud.referer.get_or_create(db=db, referer=referer)
        referer_object_id = referer_object.id

    url_view = UrlView(
        ip=ip,
        user_agent_id=user_agent_object.id,
        url=url,
        paste=paste,
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


def delete_by_paste_id(db: SQLAlchemy, paste_id: int) -> None:
    """
    Deletes paste url views with specified paste_id.
    :param SQLAlchemy db: database object
    :param int paste_id: id of paste url
    """
    UrlView.query.filter_by(paste_id=paste_id).delete()
    db.session.commit()


def get_dates(
    db: SQLAlchemy,
    url_id: int | None = None,
    paste_id: int | None = None,
    value_as: str = "percent",
) -> dict[str, int]:
    """
    Returns url views count or percentage by dates.
    :param SQLAlchemy db: database object
    :param int url_id: id of short url
    :param int paste_id: id of paste short url
    :param str value_as: controls how to present value of views. Can be:
        `percent` - (default) percentage of views. Return value can be from 1 to 100.
        `number` - number of views.
    :return: dict like {'23-09-2023': 23, '24-09-2023': 12, ...}
    :rtype: dict[str, int]
    """
    if (url_id, paste_id).count(None) != 1:
        raise TypeError("Pass only url_id or only paste_id (not both)!")

    dates = (
        db.session.query(func.date(UrlView.created_at), func.count())
        .filter_by(url_id=url_id, paste_id=paste_id)
        .group_by(func.date(UrlView.created_at))
        .all()
    )
    all_views_count = sum(x[1] for x in dates)
    if value_as == "percent":
        formatted_dates = {
            str(date): _get_percentage(all_views_count, count)
            for date, count in dates
        }
    else:
        formatted_dates = {str(date): count for date, count in dates}
    
    return formatted_dates


def get_referers(
    db: SQLAlchemy,
    url_id: int | None = None,
    paste_id: int | None = None,
    value_as: str = "percent",
) -> dict[str, int]:
    """
    Returns url views count or percentage by referers.
    :param SQLAlchemy db: database object
    :param int|None url_id: id of short_url
    :param int|None paste_id: id of paste url
    :param str value_as: type of result dict's value. Can be:
        `percent` - (default) percentage of clicks with referer.
        Returned value is int and it is limited from 1 to 100.
        `number` - number of clicks with referer. Returned value is int.
    :return: dict like {'https://away.vk.com/': 45, ...} with value as specified in `value_as` parameter
    :rtype: dict[str, int]
    """
    if (url_id, paste_id).count(None) != 1:
        raise TypeError("Pass only url_id or only paste_id (not both)!")

    # NOTE: Is there a better solution for this query?
    referers = (
        db.session.query(Referer.referer_value, func.count())
        .filter(UrlView.url_id == url_id, UrlView.paste_id == paste_id, UrlView.referer_id == Referer.id)
        .group_by(UrlView.referer_id, Referer.referer_value)
        .all()
    )
    all_views_count = UrlView.query.filter_by(url_id=url_id, paste_id=paste_id).count()
    not_null_referer_views_count = sum(x[1] for x in referers)
    null_referer_views_count = all_views_count - not_null_referer_views_count

    if value_as == "percent":
        formatted_referers = {
            referer: _get_percentage(all_views_count, count)
            for referer, count in referers
        }
    else:
        formatted_referers = dict(referers)

    if null_referer_views_count > 0:
        formatted_referers["untracked"] = (
            _get_percentage(all_views_count, null_referer_views_count)
            if value_as == "percent"
            else null_referer_views_count
        )

    return formatted_referers

def _get_percentage(whole: int, part: int) -> int:
    """
    Returns the percentage of a part of the whole.
    """
    return round(part / whole * 100)

