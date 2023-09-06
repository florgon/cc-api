"""
    URL shortener url application views for url model.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from io import BytesIO

from flask import Blueprint, Response, request, redirect, url_for
import pyqrcode

from app.serializers.url import serialize_url, serialize_urls
from app.services.api.errors import ApiErrorCode, ApiErrorException
from app.services.api.response import api_error, api_success
from app.services.request.params import get_post_param
from app.services.request.headers import get_ip
from app.database import crud, db
from app.services.url import (
    is_accessed_to_stats,
    validate_short_url,
    validate_url,
    validate_url_owner,
)
from app.services.request.auth import (
    query_auth_data_from_request,
    try_query_auth_data_from_request,
    auth_required,
)
from app.services.request.auth_data import AuthData

bp_urls = Blueprint("urls", __name__)

@bp_urls.route("/", methods=["POST"])
def create_url():
    """
    Method creates new short url.
    POST params:
     - str `url` -- long url.
     - bool `stats_is_public` (auth required) -- Make stats awailable for all.
    """
    long_url = get_post_param("url")
    validate_url(long_url)

    stats_is_public = get_post_param("stats_is_public", "False", bool)

    is_authorized, auth_data = try_query_auth_data_from_request(db=db)
    if is_authorized and auth_data:
        owner_id = auth_data.user_id
    else:
        owner_id = None

    url = crud.redirect_url.create_url(
        db=db,
        redirect_url=long_url,
        stats_is_public=stats_is_public,
        owner_id=owner_id,
    )

    include_stats = is_accessed_to_stats(url=url, owner_id=owner_id)
    return api_success(serialize_url(url, include_stats=include_stats))



@auth_required
@bp_urls.route("/", methods=["GET"])
def urls_list():
    """
    Method returns all user's urls. Auth required.
    """
    urls = crud.redirect_url.get_by_owner_id(owner_id=auth_data.user_id)
    return api_success(serialize_urls(urls, include_stats=False))


@bp_urls.route("/<url_hash>/", methods=["GET"])
def get_info_about_url(url_hash: str):
    """
    Method returns info about short url. Also it returns links to stats, if user is owner of this url.
    """
    short_url = validate_short_url(crud.redirect_url.get_by_hash(url_hash=url_hash))
    _, auth_data = try_query_auth_data_from_request(db=db)
    include_stats = is_accessed_to_stats(
        url=short_url, owner_id=auth_data.user_id if auth_data else None
    )
    return api_success(serialize_url(short_url, include_stats=include_stats))


@auth_required
@bp_urls.route("/<url_hash>/", methods=["DELETE"])
def delete_short_url(auth_data: AuthData, url_hash: str):
    """
    Method deletes short url. Auth and ownership required.
    """
    short_url = validate_short_url(crud.redirect_url.get_by_hash(url_hash=url_hash))
    validate_url_owner(
        url=short_url, owner_id=auth_data.user_id
    )
    crud.redirect_url.delete(db=db, url=short_url)
    return Response(status=204)


@bp_urls.route("/<url_hash>/", methods=["PATCH"])
def short_url_index(url_hash: str):
    raise ApiErrorException(
        ApiErrorCode.API_NOT_IMPLEMENTED, "Patching urls is not implemented yet!"
    )


@bp_urls.route("/<url_hash>/qr", methods=["GET"])
def generate_qr_code_for_url(url_hash: str):
    """
    Generates QR code image for hash url.

    TODO: Fix caching to not generate new QR code every time.
    TODO: Custom logo for QR.
    """
    response_as = request.args.get("as", "svg")
    short_url = validate_short_url(crud.redirect_url.get_by_hash(url_hash=url_hash))
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
    short_url = validate_short_url(crud.redirect_url.get_by_hash(url_hash=url_hash))

    remote_addr = get_ip()
    user_agent = request.user_agent.string
    referer = request.headers.get("Referer")
    crud.url_view.create(
        db=db, url=short_url, ip=remote_addr, user_agent=user_agent, referer=referer
    )

    return redirect(short_url.redirect)


@bp_urls.route("/<url_hash>/stats", methods=["GET", "DELETE"])
def short_url_stats(url_hash: str):
    """
    Returns stats for short url.
    Methods:
        GET: get url statistics
        DELETE: clear url statistics
    """
    short_url = validate_short_url(crud.redirect_url.get_by_hash(url_hash=url_hash))

    if request.method == "DELETE":
        auth_data = query_auth_data_from_request(db=db)
        validate_url_owner(short_url, owner_id=auth_data.user_id)
        crud.url_view.delete_by_url_id(db=db, url_id=short_url.id)
        return Response(status=204)

    if not short_url.stats_is_public:
        auth_data = query_auth_data_from_request(db=db)
        validate_url_owner(short_url, owner_id=auth_data.user_id)

    referer_views_value_as = request.args.get("referer_views_value_as", "percent")
    if referer_views_value_as not in ("percent", "number"):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "`referer_views_value_as` must be a `percent` or `number`!",
        )
    referers = crud.url_view.get_referers(
        db=db,
        url_id=short_url.id,
        value_as=referer_views_value_as,
    )

    dates_views_value_as = request.args.get("dates_views_value_as", "percent")
    if dates_views_value_as not in ("percent", "number"):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "`dates_views_value_as` must be a `percent` or `number`!",
        )
    dates = crud.url_view.get_dates(
        db=db,
        url_id=short_url.id,
        value_as=dates_views_value_as,
    )

    response = {"views": {"total": short_url.views.count()}}
    if referers:
        response["views"]["by_referers"] = referers
    if dates:
        response["views"]["by_dates"] = dates

    return api_success(response)
