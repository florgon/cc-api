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
from app.services.url import validate_short_url, validate_url

bp_url = Blueprint("url", __name__)


@bp_url.route("/create", methods=["POST"])
def create_short_url():
    """
    Creates short url and returns created url object.
    """

    long_url = request.form.get("url", "")
    validate_url(long_url) 

    url = crud.url.create_url(db=db, redirect_url=long_url)

    return api_success(serialize_url(url))

@bp_url.route("/<hash>/open", methods=["GET"])
def open_short_url(hash: str):
    """
    Redirects user to long redirect url.
    """
    short_url = crud.url.get_by_hash(db=db, hash=hash)
    validate_short_url(short_url)
    
    crud.url.add_view(db=db, url=short_url)

    return redirect(short_url.redirect)


@bp_url.route("/<hash>/", methods=["GET"])
def short_url_index(hash: str):
    """
    Short url index resource.
    Methods:
        GET: Returns info about short url
    """
    short_url = crud.url.get_by_hash(db=db, hash=hash)
    validate_short_url(short_url) 
    return api_success(serialize_url(short_url, include_stats=True))
