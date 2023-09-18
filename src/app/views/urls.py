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

from flask import Blueprint, Response, request, redirect, url_for

from app.serializers.url import serialize_url, serialize_urls
from app.services.api.errors import ApiErrorCode, ApiErrorException
from app.services.api.response import api_error, api_success
from app.services.request.params import get_post_param
from app.services.request.headers import get_ip
from app.services.qr import (
    validate_qr_result_type,
    validate_qr_code_scale,
    validate_qr_code_quiet_zone,
    generate_qr_code,
)
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
from app.services.stats import collect_stats_and_add_view

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
    validate_url_owner(url=short_url, owner_id=auth_data.user_id)
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
    GET params:
     - str `result_type` - Type of result. May be `svg`, `png` or `txt`. Defaults to `svg`.
     - int `scale` - Image scaling. May be integer from 1 to 8. Defaults to 3.
     - int `quiet_zone` - White border around qr-code. May be from 0 to 25. Defaults to 4.

    TODO: Fix caching to not generate new QR code every time.
    TODO: Custom logo for QR.
    """
    short_url = validate_short_url(crud.redirect_url.get_by_hash(url_hash=url_hash))

    result_type = request.args.get("result_type", "svg")
    validate_qr_result_type(result_type)

    scale = request.args.get("scale", "3")
    validate_qr_code_scale(scale)
    scale = int(scale)

    quiet_zone = request.args.get("quiet_zone", "4")
    validate_qr_code_quiet_zone(quiet_zone)
    quiet_zone = int(quiet_zone)

    return generate_qr_code(
        text=url_for(
            "urls.open_short_url",
            url_hash=short_url.hash,
            _external=True,
            _scheme="https",
        ),
        result_type=result_type,
        scale=scale,
        quiet_zone=quiet_zone,
    )


@bp_urls.route("/<url_hash>/open", methods=["GET"])
def open_short_url(url_hash: str):
    """
    Redirects user to long redirect url.
    Collects IP address, referer and user agents for statistics.
    """
    short_url = validate_short_url(crud.redirect_url.get_by_hash(url_hash=url_hash))
    collect_stats_and_add_view(db=db, short_url=short_url)
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
