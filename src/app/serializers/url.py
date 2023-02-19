"""
    Serializers for PasteUrl model.
"""
from typing import Any

from flask import url_for

from app.database.models.url import PasteUrl


def serialize_paste(
    url: PasteUrl, *, include_stats=False, in_list: bool = False
) -> dict[str, Any]:
    """
    Serializes PasteUrl object to dict for the response.
    """
    serialized_paste = {
        "id": url.id,
        "hash": url.hash,
        "redirect_url": url.redirect,
        "expires_at": url.expiration_date.timestamp(),
        "stats_is_public": url.stats_is_public,
        "is_deleted": url.is_deleted,
        "_links": {},
    }

    if include_stats:
        # TODO: url for pastes.short_url_stats 
        serialized_paste["_links"]["stats"] = {
            "href": url_for(
                "urls.short_url_stats",
                url_hash=url.hash,
                _external=True,
                _scheme="https",
            )
        }

    if in_list:
        return serialized_paste

    return {"paste": serialized_paste}


def serialize_pastes(
    urls: list[PasteUrl],
    *,
    include_stats: bool = False,
) -> dict[str, Any]:
    """
    Serializes list of PasteUrl objects to dict for the response.
    """
    return {
        "pastes": [
            serialize_paste(
                url,
                include_stats=include_stats,
                in_list=True,
            )
            for url in urls
        ]
    }


