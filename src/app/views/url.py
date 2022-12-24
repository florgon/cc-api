"""
    URL shortener url application views for url model.
"""
from urllib import response
import pydantic
from datetime import datetime
from io import BytesIO

from flask import Blueprint, Response, request, redirect, abort
import pyqrcode


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
    stats_is_public = request.form.get(
        "stats_is_public", False, type=lambda i: pydantic.parse_obj_as(bool, i)
    )

    url = crud.url.create_url(
        db=db, redirect_url=long_url, stats_is_public=stats_is_public
    )

    return api_success(serialize_url(url))


@bp_url.route("/<hash>/qr", methods=["GET"])
def generate_qr_code_for_url(hash: str):
    """
    Generates QR code image for hash url.

    TODO: Redirect to open handler, not directly to the target url.
    TODO: Fix caching to not generate new QR code every time.
    TODO: Custom logo for QR.
    TODO: Allow to pass scale.
    """
    response_as = request.args.get("as", "svg")
    short_url = crud.url.get_by_hash(hash=hash)
    validate_short_url(short_url)
    if response_as not in ("svg", "txt", "png"):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "Expected `as` to be `svg`, `png` or `txt`!",
        )

    # Create QR Code from redirect to.
    qr_code = pyqrcode.create(short_url.redirect)

    # Export QR to the stream or pass directly.
    qr_code_stream = BytesIO() if response_as != "txt" else None
    if response_as == "svg":
        qr_code.svg(qr_code_stream, scale=3)
    elif response_as == "png":
        qr_code.png(qr_code_stream, scale=3)

    if response_as in ("svg", "png"):
        # Headers to not cache image.
        headers_no_cache = {
            "Content-Type": "image/svg+xml" if response_as == "svg" else "image/png",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Content-Length": str(qr_code_stream.getbuffer().nbytes),
        }
        return qr_code_stream.getvalue(), 200, headers_no_cache
    else:
        # Plain text.
        return qr_code.text()


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

    return api_error(
        ApiErrorCode.API_METHOD_NOT_FOUND, f"{request.method} is not allowed for url!"
    )
