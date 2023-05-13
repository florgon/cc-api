"""
    Serializers for PasteUrl model.
"""
from typing import Any

from flask import url_for

from app.database.models.url import PasteUrl


def serialize_paste(
    url: PasteUrl, *, include_stats: bool = False, in_list: bool = False
) -> dict[str, Any]:
    """
    Serializes PasteUrl object to dict for the response.
    """
    serialized_url = {
        "id": url.id,
        "hash": url.hash,
        "text": url.content,
        "expires_at": url.expiration_date.timestamp(),
        "is_expired": url.is_expired(),
        "stats_is_public": url.stats_is_public,
        "burn_after_read": url.burn_after_read,
        "is_deleted": url.is_deleted,
        "_links": {},
    }

    if include_stats:
        serialized_url["_links"]["stats"] = {
            "href": url_for(
                "pastes.paste_stats",
                url_hash=url.hash,
                _external=True,
                _scheme="https",
            )
        }
    else:
        serialized_url.pop("_links")

    if in_list:
        return serialized_url

    return {"paste": serialized_url}


def serialize_pastes(
    urls: list[PasteUrl],
    include_stats: bool = False,
) -> dict[str, Any]:
    """
    Serializes list of PasteUrl objects to dict for the response.
    """
    return {
        "pastes": [
            serialize_paste(
                url,
                in_list=True,
                include_stats=include_stats,
            )
            for url in urls
        ]
    }
