"""
    Serializers for PasteUrl model.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
        "language": url.language,
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
