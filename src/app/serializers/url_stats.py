"""
    Serializers for url stats.
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

from typing import Any

from app.database.models.url import RedirectUrl
from app.database import crud, db


def serialize_url_stats(
    url: RedirectUrl,
    referer_views_value_as: str = "percent",
    dates_views_value_as: str = "percent",
) -> dict[str, Any]:
    """
    Serialize url stats into response dictionary (json).
    :param RedirectUrl url: url object
    :param str referer_views_value_as: how to represent views by referers.
        Accepted values: 'percent', 'number'
        Defaults to: 'percent'
    :param str dates_views_value_as: how to represent views by dates.
        Accepted values: 'percent', 'number'
        Defaults to: 'percent'
    :return: json dictionary
    :rtype: dict[str, Any]
    """
    referers = crud.url_view.get_referers(
        db=db,
        url_id=url.id,
        value_as=referer_views_value_as,
    )
    dates = crud.url_view.get_dates(
        db=db,
        url_id=url.id,
        value_as=dates_views_value_as,
    )

    response = {
        "views": {
            "total": url.views.count(),
        },
    }
    if referers:
        response["views"]["by_referers"] = referers
    if dates:
        response["views"]["by_dates"] = dates

    return response
