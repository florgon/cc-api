"""
    Serializers for url model.
"""
from typing import Any

from flask import request, url_for

from app.database.models.url import Url


def serialize_url(url: Url, include_stats=False) -> dict[str, Any]:
    serialized_url = {
        "id": url.id,
        "redirect_url": url.redirect,
        "hash": url.hash,
        "expires_at": url.expiration_date.timestamp(),
        "stats_is_public": url.stats_is_public,
        "is_deleted": url.is_deleted,
        "_links": {
            "qr": {
                "href": request.host_url[:-1]
                + url_for("urls.generate_qr_code_for_url", hash=url.hash)
            },
        },
    }

    if include_stats:
        serialized_url["views"] = url.views

    return {"url": serialized_url}
