"""
    URL shortener url application views for url model.
"""
from io import BytesIO

from flask import Blueprint, Response, request, redirect, url_for
import pydantic
import pyqrcode


from app.serializers.url import serialize_url
from app.services.api.errors import ApiErrorCode
from app.services.api.response import api_error, api_success
from app.database import crud, db
from app.services.url import validate_short_url, validate_url

bp_urls = Blueprint("urls", __name__)


@bp_urls.route("/", methods=["POST", "GET", "PATCH"])
def urls_index():
    """
    URLs index,
    Methods:
        POST - Creates short url and returns created url object.
        GET - List all urls.
    """

    if request.method == "POST":
        # Create new URL.
        long_url = request.form.get("url", "")
        validate_url(long_url)

        stats_is_public = request.form.get(
            "stats_is_public", False, type=lambda i: pydantic.parse_obj_as(bool, i)
        )

        url = crud.url.create_url(
            db=db, redirect_url=long_url, stats_is_public=stats_is_public
        )

        return api_success(serialize_url(url))

    if request.method == "PATCH":
        return api_error(
            ApiErrorCode.API_NOT_IMPLEMENTED, "Patching urls is not implemented yet!"
        )

    return api_error(
        ApiErrorCode.API_NOT_IMPLEMENTED, "Listing urls is not implemented yet!"
    )


@bp_urls.route("/<hash>/", methods=["GET", "DELETE"])
def short_url_index(hash: str):
    """
    Short url index resource.
    Methods:
        GET: Returns info about short url
        DELETE: Deletes url
    """
    short_url = crud.url.get_by_hash(hash=hash)
    validate_short_url(short_url)

    if request.method == "DELETE":
        crud.url.delete(db=db, url=short_url)

    response_status = 200 if request.method == "GET" else 204
    return api_success(
        serialize_url(short_url, include_stats=True), http_status=response_status
    )


@bp_urls.route("/<hash>/qr", methods=["GET"])
def generate_qr_code_for_url(hash: str):
    """
    Generates QR code image for hash url.

    TODO: Fix caching to not generate new QR code every time.
    TODO: Custom logo for QR.
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
    qr_code = pyqrcode.create(
        request.host_url[:-1] + url_for("urls.open_short_url", hash=short_url.hash)
    )

    # Export QR to the stream or pass directly.
    scale = request.args.get("scale", "3")
    if not scale.isdigit() or scale == "0" or int(scale) > 8:
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "`scale` argument must be an integer number in range from 1 to 8!",
        )
    scale = int(scale)

    quiet_zone = request.args.get("quiet_zone", "4")
    if not quiet_zone.isdigit() or int(quiet_zone) > 25:
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "`quiet_zone` argument must be an integer number in range from 0 to 25!",
        )
    quiet_zone = int(quiet_zone)

    qr_code_stream = BytesIO() if response_as != "txt" else None
    if response_as == "svg":
        qr_code.svg(qr_code_stream, scale=scale, quiet_zone=quiet_zone)
    elif response_as == "png":
        qr_code.png(qr_code_stream, scale=scale, quiet_zone=quiet_zone)

    if qr_code_stream is not None:
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


@bp_urls.route("/<hash>/open", methods=["GET"])
def open_short_url(hash: str):
    """
    Redirects user to long redirect url.
    """
    short_url = crud.url.get_by_hash(hash=hash, only_active=True)
    validate_short_url(short_url)

    crud.url.add_view(db=db, url=short_url)

    return redirect(short_url.redirect)
