"""
    URL shortener views for text pastes urls.
"""
from flask import Blueprint, request, Response
import pydantic

from app.services.api.errors import ApiErrorException, ApiErrorCode
from app.services.api.response import api_success
from app.serializers.paste import serialize_paste, serialize_pastes
from app.services.request.auth import try_query_auth_data_from_request, query_auth_data_from_request
from app.services.request.params import get_post_param
from app.services.request.headers import get_ip
from app.services.url import is_accessed_to_stats, validate_short_url, validate_url_owner
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
            raise ApiErrorException(ApiErrorCode.API_INVALID_REQUEST, "Paste text must be at least 10 characters length!")
        if len(text) > 4096:
            raise ApiErrorException(ApiErrorCode.API_INVALID_REQUEST, "Paste text must be less than 4096 characters length!")

        stats_is_public = get_post_param("stats_is_public", "False", bool)

        is_authorized, auth_data = try_query_auth_data_from_request(db=db)
        if is_authorized and auth_data:
            owner_id = auth_data.user_id
        else:
            owner_id = None

        url = crud.paste_url.create_url(
            db=db,
            content=text,
            stats_is_public=stats_is_public,
            owner_id=owner_id,
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
    short_url = validate_short_url(crud.paste_url.get_by_hash(url_hash=url_hash))
    _, auth_data = try_query_auth_data_from_request(db=db)

    if request.method == "DELETE":
        validate_url_owner(
            url=short_url, owner_id=auth_data.user_id if auth_data else None
        )
        crud.paste_url.delete(db=db, url=short_url)
        return Response(status=204)

    if request.method == "PATCH":
        raise ApiErrorException(
            ApiErrorCode.API_NOT_IMPLEMENTED, "Patching pastes is not implemented yet!"
        )

    include_stats = is_accessed_to_stats(
        url=short_url, owner_id=auth_data.user_id if auth_data else None
    )
    
    remote_addr = get_ip()
    user_agent = request.user_agent.string
    referer = request.headers.get("Referer")

    crud.url_view.create(
        db=db, paste=short_url, ip=remote_addr, referer=referer, user_agent=user_agent,
    )
    return api_success(serialize_paste(short_url, include_stats=include_stats))



@bp_pastes.route("/<url_hash>/stats", methods=["GET", "DELETE"])
def paste_url_stats(url_hash: str):
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
        db=db, paste_id=short_url.id, value_as=referer_views_value_as,
    )

    dates_views_value_as = request.args.get("dates_views_value_as", "percent")
    if dates_views_value_as not in ("percent", "number"):
        return ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "`dates_views_value_as` must be a `percent` or `number`!",
        )
    dates = crud.url_view.get_dates(
        db=db, paste_id=short_url.id, value_as=dates_views_value_as,
    )

    response = {"views": {"total": short_url.views.count()}}
    if referers:
        response["views"]["by_referers"] = referers
    if dates:
        response["views"]["by_dates"] = dates

    return api_success(response)
