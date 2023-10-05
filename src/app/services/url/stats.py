"""
    Services for collecting and summarizing statisticts.
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

from flask_sqlalchemy import SQLAlchemy
from flask import request

from app.services.request.headers import get_ip
from app.database import crud
from app.database.models.url import RedirectUrl
from app.database.mixins import UrlMixin
from app.services.api.errors import ApiErrorCode, ApiErrorException
from app.services.url.url import validate_url_owner


def collect_stats_and_add_view(db: SQLAlchemy, short_url: RedirectUrl) -> None:
    """
    Collects stats (IP, headers, referer) and add view to short_url.
    :param SQLAlchemy db: database object
    :param RedirectUrl short_url: short url object
    :rtype: None
    """
    remote_addr = get_ip()
    user_agent = request.user_agent.string
    referer = request.headers.get("Referer")
    crud.url_view.create(
        db=db,
        url=short_url,
        ip=remote_addr,
        user_agent=user_agent,
        referer=referer,
    )


def validate_referer_views_value_as(referer_views_value_as: str) -> None:
    if referer_views_value_as not in ("percent", "number"):
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "`referer_views_value_as` must be a `percent` or `number`!",
        )


def validate_dates_views_value_as(dates_views_value_as: str) -> None:
    if dates_views_value_as not in ("percent", "number"):
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "`dates_views_value_as` must be a `percent` or `number`!",
        )

