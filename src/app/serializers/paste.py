"""
    Serializers for PasteUrl model.
"""
from typing import Any

from flask import url_for

from app.database.models.url import PasteUrl


def serialize_paste(url: PasteUrl, *, in_list: bool = False) -> dict[str, Any]:
    """
    Serializes PasteUrl object to dict for the response.
    """
    serialized_url = {
        "id": url.id,
        "hash": url.hash,
        "text": url.content,
        "expires_at": url.expiration_date.timestamp(),
        "is_deleted": url.is_deleted,
    }

    if in_list:
        return serialized_url

    return {"paste": serialized_url}


def serialize_pastes(
    urls: list[PasteUrl],
) -> dict[str, Any]:
    """
    Serializes list of PasteUrl objects to dict for the response.
    """
    return {
        "pastes": [
            serialize_paste(
                url,
                in_list=True,
            )
            for url in urls
        ]
    }
