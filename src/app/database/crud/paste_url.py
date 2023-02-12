"""
    PasteUrl CRUD urils for the database.
"""
from flask_sqlalchemy import SQLAlchemy

from app.database.models.url import PasteUrl

def create_url(
    db: SQLAlchemy,
    content: str,
    stats_is_public: bool = False,
    owner_id: int | None = None,
) -> PasteUrl:
    """
    Creates new shortened paste url in database.
    :param SQLAlchemy db: database object
    :param str content: paste text content
    :param int | None owner_id: id of local user
    :return: created url object
    :rtype: RedirectUrl
    """
    url = PasteUrl(
        content=content,
        stats_is_public=stats_is_public,
        owner_id=owner_id,
    )

    db.session.add(url)
    db.session.commit()
    db.session.refresh(url)

    return url
