"""
    URL shortener url application views for url model.
"""
import pydantic
from datetime import datetime

from flask import Blueprint, Response, request, redirect, abort

from app.serializers.url import serialize_url
from app.services.api.errors import ApiErrorCode
from app.services.api.response import api_error, api_success
from app.database import crud, db
from app.services.url import validate_short_url, validate_url

bp_url = Blueprint("url", __name__)


@bp_url.route("/create", methods=["POST"])
def create_short_url():
    """
    Creates short url and returns created url object.
    """

    long_url = request.form.get("url", "")
    validate_url(long_url)
    stats_is_public = request.form.get("stats_is_public", False,
                                        type=lambda i: pydantic.parse_obj_as(bool, i))

    url = crud.url.create_url(db=db, redirect_url=long_url, stats_is_public=stats_is_public)

    return api_success(serialize_url(url))

@bp_url.route("/<hash>/open", methods=["GET"])
def open_short_url(hash: str):
    """
    Redirects user to long redirect url.
    """
    short_url = crud.url.get_by_hash(hash=hash)
    validate_short_url(short_url)
    
    crud.url.add_view(db=db, url=short_url)

    return redirect(short_url.redirect)


@bp_url.route("/<hash>/", methods=["GET", "DELETE"])
def short_url_index(hash: str):
    """
    Short url index resource.
    Methods:
        GET: Returns info about short url
        DELETE: Deletes url
    """
    short_url = crud.url.get_by_hash(hash=hash)
    validate_short_url(short_url) 
    if request.method == "GET":
        return api_success(serialize_url(short_url, include_stats=True))
    elif request.method == "DELETE":
        crud.url.delete(db=db, url=short_url)
        return Response(status=204)

    return api_error(ApiErrorCode.API_METHOD_NOT_FOUND, f"{request.method} is not allowed for url!")
