"""
    URL shortener views for text pastes urls.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from flask import Blueprint, request, Response

from app.services.api.errors import ApiErrorException, ApiErrorCode
from app.services.api.response import api_success
from app.serializers.paste import serialize_paste, serialize_pastes
from app.serializers.paste_stats import serialize_paste_stats
from app.services.request.auth import (
    try_query_auth_data_from_request,
    query_auth_data_from_request,
    auth_required,
)
from app.services.request.auth_data import AuthData
from app.services.request.params import get_post_param
from app.services.url_mixin import (
    validate_short_url,
    validate_url_owner,
)
from app.services.stats import is_accessed_to_stats, get_stats, validate_dates_views_value_as, validate_referer_views_value_as
from app.services.paste.paste import validate_paste_text, validate_paste_language
from app.database import db, crud


bp_pastes = Blueprint("pastes", __name__)

@bp_pastes.route("/", methods=["GET"])
@auth_required
def get_pastes_list(auth_data: AuthData):
    """
    Returns list of pastes. Auth required.
    """
    urls = crud.paste_url.get_by_owner_id(owner_id=auth_data.user_id)
    return api_success(serialize_pastes(urls, include_stats=False))

@bp_pastes.route("/", methods=["POST"])
def create_paste():
    """
    Creates new paste.
    POST params:
     - str `text` - Text of paste.
     - str `language` - Programming language of paste.
     - bool `stats_is_public` - Make paste stats public. Defaults to False.
     - bool `burn_after_read` - Paste will be deleted after first reading. Defaults to False.
    """

    text = get_post_param("text")
    validate_paste_text(text)
    language = get_post_param("language", None)
    validate_paste_language(language)
    stats_is_public = get_post_param("stats_is_public", "False", bool)
    burn_after_read = get_post_param("burn_after_read", "False", bool)

    is_authorized, auth_data = try_query_auth_data_from_request(db=db)
    owner_id = auth_data.user_id if is_authorized else None

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

@bp_pastes.route("/<url_hash>/", methods=["GET"])
def get_paste_info(url_hash: str):
    """
    Returns info about paste and links to stats if user is accessed to stats.
    """
    _, auth_data = try_query_auth_data_from_request(db=db)
    short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))
    include_stats = is_accessed_to_stats(
        url=short_url, owner_id=auth_data.user_id if auth_data else None
    )

    crud.url_view.create(
        db=db,
        paste=short_url,
        stats=get_stats()
    )
    if short_url.burn_after_read:
        crud.paste_url.delete(db, short_url)

    return api_success(serialize_paste(short_url, include_stats=include_stats))

@bp_pastes.route("/<url_hash>/", methods=["DELETE"])
@auth_required
def delete_paste(auth_data: AuthData, url_hash: str):
    """
    Deletes paste. Ownership required.
    """
    short_url = validate_short_url(
        crud.paste_url.get_by_hash(url_hash=url_hash), allow_expired=True
    )
    validate_url_owner(
        url=short_url, owner_id=auth_data.user_id if auth_data else None
    )
    crud.paste_url.delete(db=db, url=short_url)
    return Response(status=204)

@bp_pastes.route("/<url_hash>/", methods=["PATCH"])
@auth_required
def patch_paste(auth_data: AuthData, url_hash: str):
    """
    Changes paste info (text, language). Auth Required
    PATCH params:
        - str `text` - new paste text
        - str `language` - new paste langauge
    """
    short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))

    text = get_post_param("text", None)
    validate_paste_text(text)
    language = get_post_param("language", None)
    validate_paste_language(language)

    validate_url_owner(
        url=short_url, owner_id=auth_data.user_id if auth_data else None
    )
    to_update = {k: v for k, v in {
        "text": text,
        "language": language,
    }.items() if v is not None}
    crud.paste_url.update(db=db, url=short_url, **to_update)
    return api_success(serialize_paste(short_url, include_stats=True))


@bp_pastes.route("/<url_hash>/stats", methods=["GET"])
def get_paste_stats(url_hash: str):
    """
    Returns statistics about paste. Auth required if
    stats is private (not public).
    """
    short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))
    if not short_url.stats_is_public:
        auth_data = query_auth_data_from_request(db=db)
        validate_url_owner(short_url, owner_id=auth_data.user_id)

    referer_views_value_as = request.args.get("referer_views_value_as", "percent")
    validate_referer_views_value_as(referer_views_value_as)
    dates_views_value_as = request.args.get("dates_views_value_as", "percent")
    validate_dates_views_value_as(dates_views_value_as)

    response = serialize_paste_stats(
        short_url, referer_views_value_as, dates_views_value_as
    )
    return api_success(response)


@bp_pastes.route("/<url_hash>/stats", methods=["DELETE"])
@auth_required
def clear_paste_stats(auth_data: AuthData, url_hash: str):
    short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))
    validate_url_owner(short_url, owner_id=auth_data.user_id)
    crud.url_view.delete_by_paste_id(db=db, paste_id=short_url.id)
    return Response(status=204)
