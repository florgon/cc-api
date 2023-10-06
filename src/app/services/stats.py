"""
    Services for collecting and summarizing statisticts for
    both urls and pastes.
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

from app.database.mixins import UrlMixin
from app.services.url_mixin import validate_url_owner
from app.services.api.errors import ApiErrorException


def is_accessed_to_stats(
    url: UrlMixin, owner_id: int | None, fatal: bool = False
) -> bool:
    """
    Checks that user with owner_id has access to url stats.
    :param UrlMixin url: url object
    :param int owner_id: user id
    :return: True if has access, else False
    """
    if url.stats_is_public:
        return True

    try:
        validate_url_owner(url=url, owner_id=owner_id)
    except ApiErrorException as e:
        if fatal:
            raise e
        return False

    return True
