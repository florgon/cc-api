"""
    Url CRUD utils for the database.
"""
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids

from app.database.models.url import Url


def create_url(
    db: SQLAlchemy,
    redirect_url: str,
    stats_is_public: bool = False,
    owner_id: int | None = None,
) -> Url:
    """
    Creates new shortened url in database.
    :param SQLAlchemy db: database object
    :param str redirect_url: long url for redirecting
    :param int | None owner_id: id of local user
    :return: created url object
    :rtype: Url
    """
    if not redirect_url.startswith("http://") and not redirect_url.startswith(
        "https://"
    ):
        # Add protocol for valid redirecting to an external domain
        redirect_url = "https://" + redirect_url

    url = Url(
        redirect=redirect_url,
        stats_is_public=stats_is_public,
        owner_id=owner_id,
    )

    db.session.add(url)
    db.session.commit()
    db.session.refresh(url)

    return url


def get_all() -> list[Url]:
    """
    Returns all URLs from the database.
    :return: List with URLs.
    :rtype: List of the urls.
    """
    return Url.query.all()


def get_by_owner_id(owner_id: int) -> list[Url]:
    """
    Returns all URLs with owner ID from the database.
    :return: List with URLs.
    :rtype: List of the urls.
    """
    return Url.query.filter_by(owner_id=owner_id)


def get_by_hash(url_hash: str, only_active: bool = True) -> Url | None:
    """
    Get shortened url from database by hash generated by hashids.
    Decodes hash and get url from database by decoded id.
    :param SQLAlchemy db: database object
    :param str url_hash: hashids hash
    :param bool only_active: search url from active (with is_deleted = False) urls
    :return: url object
    :rtype: Url or None if hash is invalid
    """
    hashids = Hashids(salt=current_app.config["HASHIDS_SALT"], min_length=6)
    url_ids: tuple[int] = hashids.decode(url_hash)
    if len(url_ids) != 1:
        return None
    url_id = url_ids[0]
    url = Url.query.filter_by(id=url_id)
    if only_active:
        url = url.filter_by(is_deleted=False)
    return url.first()


def delete(db: SQLAlchemy, url: Url) -> None:
    """
    Deletes url and views.
    :param SQLAlchemy db: database object
    :param Url url: url object
    """
    url.is_deleted = True
    db.session.commit()
