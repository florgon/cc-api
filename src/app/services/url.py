"""
    Service module for url.
"""
import re

from app.database.models.url import Url
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
        r"^((https:\/\/|http:\/\/|)([\w_-]+\.){1,3}\w{1,10}(\/.*)?|mailto:.*@.*|tel:.*)$", flags=re.U
    )
    if pattern.match(url) is None:
        raise ApiErrorException(ApiErrorCode.API_INVALID_REQUEST, "url is invalid!")


def validate_short_url(url: Url | None) -> None:
    """
    Validates short url object and raises ApiErrorException if it is expired/invalid.
    :param Url|None url: short url to validate
    :raises ApiErrorException: when url is invalid
    """
    if url is None:
        raise ApiErrorException(
            ApiErrorCode.API_ITEM_NOT_FOUND, "url hash is invalid/not specified"
        )

    if url.is_expired():
        raise ApiErrorException(ApiErrorCode.API_FORBIDDEN, "url is expired!")
