"""
    Service module for url.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re

from app.services.api.errors import ApiErrorException, ApiErrorCode


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
