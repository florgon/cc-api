"""
    Tests for permissions service.
"""
import pytest

from app.services.permissions import (
    SCOPE_ALL_PERMISSIONS,
    normalize_scope,
    SCOPE_PERMISSION_GRANT_ALL_TAG,
    SCOPE_PERMISSION_SEPARATOR,
    SCOPE_ALLOWED_PERMISSIONS,
    Permission,
    parse_permissions_from_scope,
)


class TestNormalizeScope:
    """
    Tests for normalize_scope function.
    """

    @staticmethod
    def test_with_scope_with_wrong_type():
        """
        Tests that function raises error when scope is not str type.
        """
        with pytest.raises(TypeError):
            normalize_scope(scope=1)

    @staticmethod
    def test_with_wrong_permission_in_scope():
        """
        Tests that function deletes wrong permissions in scope.
        """
        assert normalize_scope(scope="cc,undefinedpermission") == "cc"

    @staticmethod
    def test_with_normal_scope():
        """
        Tests that function does nothing when scope is normal.
        """
        assert normalize_scope(scope="cc,email") == "cc,email"

    @staticmethod
    def test_with_grant_all_tag_scope():
        """
        Tests that function returns all permissions in scope if scope='*'.
        """
        assert normalize_scope(
            scope=SCOPE_PERMISSION_GRANT_ALL_TAG
        ) == SCOPE_PERMISSION_SEPARATOR.join(SCOPE_ALLOWED_PERMISSIONS)


class TestParsePermissionsFromScope:
    """
    Tests for parse_permissions_from_scope function.
    """

    @staticmethod
    def test_with_scope_with_wrong_type():
        with pytest.raises(TypeError):
            parse_permissions_from_scope(scope=1)

    @staticmethod
    def test_with_wrong_permission_in_scope():
        assert parse_permissions_from_scope(scope="cc,undefinedpermission") == [
            Permission.cc
        ]

    @staticmethod
    def test_with_normal_scope():
        assert parse_permissions_from_scope(scope="cc,email") == [
            Permission.cc,
            Permission.email,
        ]

    @staticmethod
    def test_with_grant_all_tag_scope():
        assert (
            parse_permissions_from_scope(scope=SCOPE_PERMISSION_GRANT_ALL_TAG)
            == SCOPE_ALL_PERMISSIONS
        )
