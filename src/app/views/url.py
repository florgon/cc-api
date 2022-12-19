"""
    URL shortener url application views for url model.
"""
import re
from datetime import datetime

from flask import Blueprint, request, redirect
from app.serializers.url import serialize_url
from app.services.api.errors import ApiErrorCode
from app.services.api.response import api_error, api_success
from app.database import crud, db

bp_url = Blueprint("url", __name__)


@bp_url.route("/create", methods=["POST"])
def create_short_url():
    """
    Creates short url and returns created url object.
    """

    long_url = request.form.get("url")
    if long_url is None or long_url == "":
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "url is required!")

    pattern = re.compile(r"^(https:\/\/|http:\/\/|)(\w+\.){1,3}\w{1,10}(\/.*)?$")
    if pattern.match(long_url) is None:
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST, "url is invalid!"
        )

    url = crud.url.create_url(db=db, redirect_url=long_url)

    return api_success(serialize_url(url))

@bp_url.route("/<hash>/open", methods=["GET"])
def open_short_url(hash: str):
    """
    Redirects user to long redirect url.
    """
    short_url = crud.url.get_by_hash(db=db, hash=hash)
    if short_url is None:
        return api_error(
            ApiErrorCode.API_ITEM_NOT_FOUND, "hash is invalid!"
        )

    if short_url.expiration_date <= datetime.now():
        return api_error(
            ApiErrorCode.API_TOKEN_EXPIRED, "hash is expired!"
        )

    return redirect(short_url.redirect)
