"""
    Service module for url.
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


def validate_short_url(url: UrlMixin | None) -> UrlMixin:
    """
    Validates short url object and raises ApiErrorException if it is expired/invalid.
    :param UrlMixin|None url: short url to validate
    :raises ApiErrorException: when url is invalid
    """
    if url is None:
        raise ApiErrorException(
            ApiErrorCode.API_ITEM_NOT_FOUND, "url hash is invalid/not specified"
        )

    if url.is_expired():
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
