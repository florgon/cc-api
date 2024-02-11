"""
    DTO for authentication request.
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

from app.services.permissions import Permission
from app.database.models.user import User


class AuthData:
    """DTO for authenticated request."""

    user_id: int

    def __init__(self, user: User) -> None:
        """
        :param int user_id: User index.
        :param User user: user object
        """
        self.user_id = user.id
        self.user = user
