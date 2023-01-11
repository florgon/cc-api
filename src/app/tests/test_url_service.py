"""
    Module for testing services/url.py
"""
from datetime import datetime, timedelta

import pytest

from app.services.api.errors import ApiErrorException
from app.services.url import validate_url, validate_short_url, validate_url_owner
from app.database.models.url import Url


class TestValidateUrl:
    """
    Tests for validate_url function
    """

    @staticmethod
    def test_with_none_url():
        """
        Tests that raises error when there is invalid url.
        """
        with pytest.raises(ApiErrorException):
            validate_url(url=None)

    @staticmethod
    def test_with_empty_url():
        """
        Tests that raises error when there is empty url.
        """
        with pytest.raises(ApiErrorException):
            validate_url(url="   ")

    @staticmethod
    @pytest.mark.parametrize(
        "url",
        [
            "ftp:///some/path/to/file",
            "http://localhost/v1/api/",
            "/florgon.space/",
            "florgon.toooooolong",
            "too.much.subdomains.in.this.url",
            "wrong_symbols%in.url",
        ],
    )
    def test_wrong_urls(url):
        """
        Tests that raises error when there is invalid url.
        """
        with pytest.raises(ApiErrorException):
            validate_url(url=url)

    @staticmethod
    @pytest.mark.parametrize(
        "url",
        [
            "florgon.space",
            "https://vk.com/florgon",
        ],
    )
    def test_normal_url(url):
        """
        Tests that there is no error when there is valid one url.
        """
        assert validate_url(url=url) is None


class TestValidateShortUrl:
    """
    Tests for validate_short_url function
    """

    @staticmethod
    def test_with_none_url():
        """
        Tests that raises error when there is invalid url.
        """
        with pytest.raises(ApiErrorException):
            validate_short_url(url=None)

    @staticmethod
    def test_expired_url():
        """
        Tests that raises error when there is expired url.
        """
        url = Url(
            redirect="https://florgon.space",
            expiration_date=datetime.utcnow() - timedelta(days=1),
        )
        with pytest.raises(ApiErrorException):
            validate_short_url(url)

    @staticmethod
    def test_normal_url():
        """
        Tests that not raises error when there is valid url.
        """
        url = Url(
            redirect="https://florgon.space",
            expiration_date=datetime.utcnow() + timedelta(days=1),
        )
        assert validate_short_url(url=url) is not None


class TestValidateUrlOwner:
    """
    Tests for validate_url_owner function.
    """

    @staticmethod
    @pytest.mark.parametrize("owner_id", [None, 33])
    def test_with_wrong_owner_id(owner_id: int | None):
        """
        Tests that function raises error when owner_id is not the same with url owner id.
        """
        url = Url(
            redirect="https://florgon.space",
            owner_id=1,
        )
        with pytest.raises(ApiErrorException):
            validate_url_owner(url=url, owner_id=owner_id)

    @staticmethod
    def test_with_normal_owner_id():
        """
        Tests that function doesn't raises error when owner_ids are same
        """
        url = Url(
            redirect="https://florgon.space",
            owner_id=1,
        )
        assert validate_url_owner(url=url, owner_id=url.owner_id) is None
