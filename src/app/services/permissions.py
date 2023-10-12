"""
    Permission service, works with scope, permissions.
    OAuth permissions.
    Read more at docs: https://florgon.space/dev/apis/auth
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
from enum import Enum


class Permission(Enum):
    """
    Permissions scope string enumeration.
    """

    # Other.
    noexpire = "noexpire"
    edit = "edit"
    email = "email"

    # Private.
    admin = "admin"

    # Services.
    cc = "cc"


def normalize_scope(scope: str) -> str:
    """
    Returns normalized scope from scope, means there is no repeated scopes and maybe some unused symbols.
    :param str scope: scope
    :return: normalized scope
    :rtype: str
    """
    if not isinstance(scope, str):
        raise TypeError("Scope must be a string!")
    return SCOPE_PERMISSION_SEPARATOR.join(
        [permission.value for permission in parse_permissions_from_scope(scope)]
    )


def parse_permissions_from_scope(scope: str) -> list[Permission]:
    """
    Returns list of permissions from scope, by parsing it.
    :param str scope: scope
    :returns: list of Permissions from scope
    :rtype: list[Permission]
    """
    if not isinstance(scope, str):
        raise TypeError("Scope must be a string!")
    if SCOPE_PERMISSION_GRANT_ALL_TAG in scope:
        return SCOPE_ALL_PERMISSIONS
    return list(
        {
            Permission(permission)
            for permission in scope.split(SCOPE_PERMISSION_SEPARATOR)
            if (permission and permission in SCOPE_ALLOWED_PERMISSIONS)
        }
    )


# String tags, for separator and modificator that gives all permissions.
SCOPE_PERMISSION_GRANT_ALL_TAG = "*"
SCOPE_PERMISSION_SEPARATOR = ","

# List of all permissions.
SCOPE_ALL_PERMISSIONS = [
    Permission.email,
    Permission.noexpire,
    Permission.admin,
    Permission.edit,
    Permission.cc,
]

# Allowed permission, as string list.
SCOPE_ALLOWED_PERMISSIONS = list(
    map(
        lambda p: p.value,
        SCOPE_ALL_PERMISSIONS,
    )
)
