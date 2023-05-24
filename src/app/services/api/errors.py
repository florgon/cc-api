"""
    Standardized API error codes container.
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
            self, api_code: ApiErrorCode, message: str = "", data: dict | None = None, headers: dict | None = None,
    ):
        super().__init__()
        self.api_code = api_code
        self.message = message
        self.data = data
        self.headers = headers
