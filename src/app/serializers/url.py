"""
    Serializers for url model.
"""
from typing import Any

from flask import url_for

from app.database.models.url import Url


def serialize_url(
    url: Url, *, include_stats=False, in_list: bool = False
) -> dict[str, Any]:
    """
    Serializes url object to dict for the response.
    """
    serialized_url = {
        "id": url.id,
        "sso_user_id": None,
        "redirect_url": url.redirect,
        "hash": url.hash,
        "expires_at": url.expiration_date.timestamp(),
        "stats_is_public": url.stats_is_public,
        "is_deleted": url.is_deleted,
        "_links": {
            "qr": {
                "href": url_for(
                    "urls.generate_qr_code_for_url",
                    url_hash=url.hash,
                    _external=True,
                    _scheme="https",
                )
            },
        },
    }

    if url.owner_id:
        serialized_url["sso_user_id"] = url.owner_id
    else:
        serialized_url.pop("sso_user_id")

    if include_stats:
        serialized_url["_links"]["stats"] = {
            "href": url_for(
                "urls.short_url_stats",
                url_hash=url.hash,
                _external=True,
                _scheme="https",
            )
        }

    if in_list:
        return serialized_url

    return {"url": serialized_url}


def serialize_urls(
    urls: list[Url],
    *,
    include_stats: bool = False,
) -> dict[str, Any]:
    """
    Serializes list of urls objects to dict for the response.
    """
    return {
        "urls": [
            serialize_url(
                url,
                include_stats=include_stats,
                in_list=True,
            )
            for url in urls
        ]
    }
