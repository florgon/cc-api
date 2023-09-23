"""
    URL shortener views for text pastes urls.
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
from flask import Blueprint, request, Response

from app.services.api.errors import ApiErrorException, ApiErrorCode
from app.services.api.response import api_success
from app.serializers.paste import serialize_paste, serialize_pastes
from app.services.request.auth import (
    try_query_auth_data_from_request,
    query_auth_data_from_request,
)
from app.services.request.params import get_post_param
from app.services.request.headers import get_ip
from app.services.url import (
    validate_short_url,
    validate_url_owner,
)
from app.services.stats import is_accessed_to_stats
from app.database import db, crud


bp_pastes = Blueprint("pastes", __name__)


@bp_pastes.route("/", methods=["POST", "GET"])
def pastes_index():
    """
    Pastes index resource.
    Methods:
        POST - Creates paste url and return created url object
        GET - List all urls
    """

    if request.method == "POST":
        text = get_post_param("text")
        if len(text) < 10:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste text must be at least 10 characters length!",
            )
        if len(text) > 4096:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste text must be less than 4096 characters length!",
            )

        language = get_post_param("language", None)
        if language is None:
            pass
        elif not language:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste language must be at least 1 character length!"
            )
        elif len(language) > 20:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste language must be less then 20 character length!"
            )

        is_authorized, auth_data = try_query_auth_data_from_request(db=db)
        if is_authorized and auth_data:
            owner_id = auth_data.user_id
        else:
            owner_id = None

        stats_is_public = get_post_param("stats_is_public", "False", bool)
        burn_after_read = get_post_param("burn_after_read", "False", bool)

        url = crud.paste_url.create_url(
            db=db,
            content=text,
            stats_is_public=stats_is_public,
            burn_after_read=burn_after_read,
            owner_id=owner_id,
            language=language if language else "plain",
        )

        include_stats = is_accessed_to_stats(url=url, owner_id=owner_id)
        return api_success(serialize_paste(url, include_stats=include_stats))

    auth_data = query_auth_data_from_request(db=db)
    urls = crud.paste_url.get_by_owner_id(owner_id=auth_data.user_id)
    return api_success(serialize_pastes(urls, include_stats=False))


@bp_pastes.route("/<url_hash>/", methods=["GET", "DELETE", "PATCH"])
def paste_index(url_hash: str):
    """
    Paste url index resource.
    Methods:
        GET: Returns info about paste
        DELETE: Deletes paste
        PATCH: Updates paste
    """
    _, auth_data = try_query_auth_data_from_request(db=db)

    if request.method == "DELETE":
        short_url = validate_short_url(
            crud.paste_url.get_by_hash(url_hash=url_hash), allow_expired=True
        )
        validate_url_owner(
            url=short_url, owner_id=auth_data.user_id if auth_data else None
        )
        crud.paste_url.delete(db=db, url=short_url)
        return Response(status=204)

    if request.method == "PATCH":
        short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))
        text = get_post_param("text", None)
        if text is None:
            pass
        elif len(text) < 10:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste text must be at least 10 characters length!",
            )
        elif len(text) > 4096:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste text must be less than 4096 characters length!",
            )
        language = get_post_param("language", None)
        if language is None:
            pass
        elif len(language) == 0:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste language must be at least 1 character length!"
            )
        elif len(language) > 20:
            raise ApiErrorException(
                ApiErrorCode.API_INVALID_REQUEST,
                "Paste language must be less then 20 character length!"
            )

        validate_url_owner(
            url=short_url, owner_id=auth_data.user_id if auth_data else None
        )
        to_update = {k: v for k, v in {
            "text": text,
            "language": language,
        }.items() if v is not None}
        crud.paste_url.update(db=db, url=short_url, **to_update)
        return api_success(serialize_paste(short_url, include_stats=True))

    short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))
    include_stats = is_accessed_to_stats(
        url=short_url, owner_id=auth_data.user_id if auth_data else None
    )

    remote_addr = get_ip()
    user_agent = request.user_agent.string
    referer = request.headers.get("Referer")

    crud.url_view.create(
        db=db,
        paste=short_url,
        ip=remote_addr,
        referer=referer,
        user_agent=user_agent,
    )
    if short_url.burn_after_read:
        crud.paste_url.delete(db, short_url)

    return api_success(serialize_paste(short_url, include_stats=include_stats))


@bp_pastes.route("/<url_hash>/stats", methods=["GET", "DELETE"])
def paste_stats(url_hash: str):
    """
    Returns stats for paste url.
    Methods:
        GET: get url statistics
        DELETE: clear url statistics
    """
    short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))

    if request.method == "DELETE":
        auth_data = query_auth_data_from_request(db=db)
        validate_url_owner(short_url, owner_id=auth_data.user_id)
        crud.url_view.delete_by_paste_id(db=db, paste_id=short_url.id)
        return Response(status=204)

    if not short_url.stats_is_public:
        auth_data = query_auth_data_from_request(db=db)
        validate_url_owner(short_url, owner_id=auth_data.user_id)

    referer_views_value_as = request.args.get("referer_views_value_as", "percent")
    if referer_views_value_as not in ("percent", "number"):
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "`referer_views_value_as` must be a `percent` or `number`!",
        )
    referers = crud.url_view.get_referers(
        db=db,
        paste_id=short_url.id,
        value_as=referer_views_value_as,
    )

    dates_views_value_as = request.args.get("dates_views_value_as", "percent")
    if dates_views_value_as not in ("percent", "number"):
        return ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "`dates_views_value_as` must be a `percent` or `number`!",
        )
    dates = crud.url_view.get_dates(
        db=db,
        paste_id=short_url.id,
        value_as=dates_views_value_as,
    )

    response = {"views": {"total": short_url.views.count()}}
    if referers:
        response["views"]["by_referers"] = referers
    if dates:
        response["views"]["by_dates"] = dates

    return api_success(response)
