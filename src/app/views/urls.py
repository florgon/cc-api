"""
    URL shortener url application views for url model.
"""
from io import BytesIO

from flask import Blueprint, Response, request, redirect, url_for
import pydantic
import pyqrcode

from app.database.models.url import Url
from app.serializers.url import serialize_url, serialize_urls
from app.services.api.errors import ApiErrorCode
from app.services.api.response import api_error, api_success
from app.database import crud, db
from app.services.url import validate_short_url, validate_url

bp_urls = Blueprint("urls", __name__)


@bp_urls.route("/", methods=["POST", "GET"])
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

    urls = crud.url.get_all()
    return api_success(serialize_urls(urls, include_stats=False))


@bp_urls.route("/<url_hash>/", methods=["GET", "DELETE", "PATCH"])
def short_url_index(url_hash: str):
    """
    Short url index resource.
    Methods:
        GET: Returns info about short url
        DELETE: Deletes url
        PATCH: Updates url
    """
    short_url = validate_short_url(crud.url.get_by_hash(url_hash=url_hash))

    if request.method == "DELETE":
        crud.url.delete(db=db, url=short_url)
        return Response(status=204)

    if request.method == "PATCH":
        return api_error(
            ApiErrorCode.API_NOT_IMPLEMENTED, "Patching urls is not implemented yet!"
        )

    return api_success(serialize_url(short_url, include_stats=True))


@bp_urls.route("/<url_hash>/qr", methods=["GET"])
def generate_qr_code_for_url(url_hash: str):
    """
    Generates QR code image for hash url.

    TODO: Fix caching to not generate new QR code every time.
    TODO: Custom logo for QR.
    """
    response_as = request.args.get("as", "svg")
    short_url = validate_short_url(crud.url.get_by_hash(url_hash=url_hash))
    if response_as not in ("svg", "txt", "png"):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "Expected `as` to be `svg`, `png` or `txt`!",
        )

    # Create QR Code from redirect to.
    qr_code = pyqrcode.create(
        url_for(
            "urls.open_short_url",
            url_hash=short_url.hash,
            _external=True,
            _scheme="https",
        )
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

    # Plain text.
    return qr_code.text()


@bp_urls.route("/<url_hash>/open", methods=["GET"])
def open_short_url(url_hash: str):
    """
    Redirects user to long redirect url.
    """
    short_url = validate_short_url(crud.url.get_by_hash(url_hash=url_hash))

    if "X-Forwarded-For" in request.headers:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(" ")[-1]
    else:
        remote_addr = request.remote_addr or "untrackable"
    user_agent = request.user_agent.string
    referer = request.headers.get("Referer")
    crud.url_view.create(
        db=db, url=short_url, ip=remote_addr, user_agent=user_agent, referer=referer
    )

    return redirect(short_url.redirect)


@bp_urls.route("/<url_hash>/stats", methods=["GET"])
def short_url_stats(url_hash: str):
    """
    Returns stats for short url.
    """
    short_url = validate_short_url(crud.url.get_by_hash(url_hash=url_hash))

    referer_views_value_as = request.args.get("referer_views_value_as", "percent")
    if referer_views_value_as not in ("percent", "number"):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "`referer_views_value_as` must be a `percent` or `number`!",
        )
    referers = crud.referer.get_url_views_count_by_referers(
        db=db, url=short_url, value_as=referer_views_value_as
    )
    return api_success(
        {"views": {"total": short_url.views.count(), "by_referers": referers}}
    )
