"""
    DTO for authentication request.
"""

from app.services.permissions import Permission
from app.database.models.user import User


class AuthData:
    """DTO for authenticated request."""

    user_id: int
    permissions: list[Permission]

    def __init__(self, user_id: int, permissions: list[Permission], user: User) -> None:
        """
        :param int user_id: User index.
        :param list[Permission] permissions: List of permissions.
        :param User user: user object
        """
        self.user_id = user_id
        self.user = user
        self.permissions = permissions
