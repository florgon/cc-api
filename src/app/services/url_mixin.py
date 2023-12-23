"""
    Service module for models based on UrlMixin (PasteUrl, RedirectUrl).
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

from app.database.mixins import UrlMixin
from app.services.api.errors import ApiErrorException, ApiErrorCode


def validate_short_url(url: UrlMixin | None, allow_expired: bool = False) -> UrlMixin:
    """
    Validates short url object and raises ApiErrorException if
    it is expired/invalid.
    :param UrlMixin|None url: short url to validate
    :raises ApiErrorException: when url is invalid
    """
    if url is None:
        raise ApiErrorException(
            ApiErrorCode.API_ITEM_NOT_FOUND, "Url hash is invalid/not specified"
        )

    if not allow_expired and url.is_expired():
        raise ApiErrorException(ApiErrorCode.API_FORBIDDEN, "Url is expired!")

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
            ApiErrorCode.API_FORBIDDEN, "You are not owner of this url!"
        )
