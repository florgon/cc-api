"""
    CRUD for Referer database model.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from app.database.models.referer import Referer
from app.database.models.url import Url
from app.database.models.url_view import UrlView


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


def get_url_views_count_by_referers(db: SQLAlchemy, url: Url, value_as: str = "percent") -> dict[str, int]:
    """
    Returns a dict where the key is referer and the value is the number
    or percentage of views of the url with referer. 
    :param SQLAlchemy db: database object
    :param Url url: Url object
    :param str value_as: type of result dict's value. Can be:
        `percent` - (default) percentage of clicks with referer.
        Returned value is int and it is limited from 1 to 100.
        `number` - number of clicks with referer. Returned value is int.
    :return: dict like {'https://away.vk.com/': 45, ...} with value as specified in `value_as` parameter
    :rtype: dict[str, int]
    """
    
    # NOTE: Is there a better solution for this query?
    referers = (db.session.query(Referer.referer_value, func.count())
                          .filter(UrlView.url_id == url.id, UrlView.referer_id == Referer.id)
                          .group_by(UrlView.referer_id, Referer.referer_value)
                          .all())
    all_views_count = UrlView.query.filter_by(url_id=url.id).count()
    not_null_referer_views_count = sum(x[1] for x in referers) 
    null_referer_views_count = all_views_count - not_null_referer_views_count

    referers.append(("untracked", null_referer_views_count))
    if value_as == "percent":
        formatted_referers = {x[0]: _get_percentage(all_views_count, x[1]) for x in referers}
    else:
        formatted_referers = dict(referers)

    return formatted_referers



def _get_percentage(whole: int, part: int) -> int:
    """
    Returns the percentage of a part of the whole.
    """
    return round(part/whole*100)
