"""
    Module for testing services/url.py
"""
import pytest
from datetime import datetime, timedelta

from app.services.api.errors import ApiErrorException
from app.services.url import validate_url, validate_short_url
from app.database.models.url import Url

class TestValidateUrl:
    """
    Tests for validate_url function
    """
    def test_with_none_url(self):
        with pytest.raises(ApiErrorException):
            validate_url(url=None)

    def test_with_empty_url(self):
        with pytest.raises(ApiErrorException):
            validate_url(url="   ")

    @pytest.mark.parametrize("url", [
        "ftp:///some/path/to/file",
        "http://localhost/v1/api/",
        "/florgon.space/",
        "florgon.toooooolong",
        "too.much.subdomains.in.this.url",
        "wrong_symbols%in.url",
    ])
    def test_wrong_urls(self, url):
        with pytest.raises(ApiErrorException):
            validate_url(url=url)

    
    @pytest.mark.parametrize("url", [
        "florgon.space",
        "https://vk.com/florgon",
    ])
    def test_normal_url(self, url):
        assert validate_url(url=url) == None


class TestValidateShortUrl:
    """
    Tests for validate_short_url function
    """
    def test_with_none_url(self):
        with pytest.raises(ApiErrorException):
            validate_short_url(url=None)

    def test_expired_url(self):
        url = Url(
            redirect="https://florgon.space",
            expiration_date=datetime.utcnow() - timedelta(days=1)
        )
        with pytest.raises(ApiErrorException):
            validate_short_url(url)


    def test_normal_url(self):
        url = Url(
            redirect="https://florgon.space",
            expiration_date=datetime.utcnow() + timedelta(days=1),
        )
        assert validate_short_url(url=url) == None 




