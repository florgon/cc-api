"""
    Standardized API error codes container.
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

from enum import Enum


class ApiErrorCode(Enum):
    """API Standardized error codes."""

    API_UNKNOWN_ERROR = 0, 400
    API_INTERNAL_SERVER_ERROR = 1, 500
    API_EXTERNAL_SERVER_ERROR = 2, 500
    API_INVALID_REQUEST = 3, 400
    API_NOT_IMPLEMENTED = 4, 400
    API_METHOD_NOT_FOUND = 5, 404
    API_TOO_MANY_REQUESTS = 6, 429
    API_FORBIDDEN = 7, 403
    API_ITEM_NOT_FOUND = 8, 404
    API_METHOD_NOT_ALLOWED = 9, 405
    AUTH_REQUIRED = 100, 401
    AUTH_INVALID_TOKEN = 101, 400
    AUTH_EXPIRED_TOKEN = 102, 400
    AUTH_INSUFFICIENT_PERMISSIONS = 103, 403
    USER_DEACTIVATED = 200, 403
    USER_EMAIL_NOT_CONFIRMED = 201, 403
    USER_NOT_FOUND = 202, 404


class ApiErrorException(Exception):
    """
    Exception, that will be return to the user as API error response (FastAPI) handler.
    """

    def __init__(
        self, api_code: ApiErrorCode, message: str = "", data: dict | None = None
    ):
        super().__init__()
        self.api_code = api_code
        self.message = message
        self.data = data
