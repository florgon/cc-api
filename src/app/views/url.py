"""
    URL shortener url application views for url model.
"""
from time import time

from flask import Blueprint, request
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
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST, "url is required!"
        )

    url = crud.url.create_url(db=db, redirect_url=long_url) 

    return api_success(serialize_url(url))
