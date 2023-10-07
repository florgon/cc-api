"""
    Service module for url.
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
import re

from app.services.api.errors import ApiErrorException, ApiErrorCode
from app.database.mixins import UrlMixin


def validate_url(url: str | None) -> None:
    """
    Validates long url and raises ApiErrorException if it is invalid.
    :param str|None url: long url to validate
    :raises ApiErrorException: when url is invalid
    """
    if not url:
        raise ApiErrorException(ApiErrorCode.API_INVALID_REQUEST, "url is required!")

    pattern = re.compile(
        r"^((https:\/\/|http:\/\/|)([\w_-]+\.){1,3}\w{1,10}(\/.*)?|mailto:.*@.*|tel:.*)$",
        flags=re.U,
    )
    if pattern.match(url) is None:
        raise ApiErrorException(ApiErrorCode.API_INVALID_REQUEST, "url is invalid!")


def validate_short_url(url: UrlMixin | None, allow_expired: bool = False) -> UrlMixin:
    """
    Validates short url object and raises ApiErrorException if it is expired/invalid.
    :param UrlMixin|None url: short url to validate
    :raises ApiErrorException: when url is invalid
    """
    if url is None:
        raise ApiErrorException(
            ApiErrorCode.API_ITEM_NOT_FOUND, "url hash is invalid/not specified"
        )

    if not allow_expired and url.is_expired():
        raise ApiErrorException(ApiErrorCode.API_FORBIDDEN, "url is expired!")

    return url


def validate_url_owner(url: UrlMixin, owner_id: int | None) -> None:
    """
    Checks that url is owned by user with owner_id
    :param UrlMixin url: short url object
    :param int owner_id: id of owner
    :raises ApiErrorException: when url is not owned by user
    """
    if owner_id != url.owner_id or owner_id is None:
        raise ApiErrorException(
            ApiErrorCode.API_FORBIDDEN, "you are not owner of this url!"
        )


def is_accessed_to_stats(url: UrlMixin, owner_id: int | None):
    """
    Checks that user with owner_id has access to url stats.
    :param UrlMixin url: url object
    :param int owner_id: user id
    :return: True if has access, else False
    """
    if url.stats_is_public:
        return True

    try:
        validate_url_owner(url=url, owner_id=owner_id)
    except ApiErrorException:
        return False

    return True
