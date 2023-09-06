"""
    Request handler and decoder.
    Allows to query auth data from your token or request.
    Root handler for authentication decode.
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
import functools
import logging
from requests import request
from requests.exceptions import JSONDecodeError

from flask import current_app, request as flask_request
from flask_sqlalchemy import SQLAlchemy

from app.services.api.errors import ApiErrorCode, ApiErrorException
from app.services.request.auth_data import AuthData
from app.services.permissions import Permission, parse_permissions_from_scope
from app.database.models.user import User
from app.database import crud, db

# Scope that will be requested from SSO.
SSO_REQUESTED_SCOPE = "cc"


def auth_required(view):
    """
    Decorator requires that user is authenticated via Florgon SSO.
    Decorates API view.
    Passes auth_data as first argument of view function, then other arguments.
    :param view: API view function.
    """
    @functools.wraps(view)
    def wrap(*args, **kwargs):
        auth_data = query_auth_data_from_request(db=db)
        return view(auth_data, *args, **kwargs)
    return wrap


def query_auth_data_from_token(
    db: SQLAlchemy,
    token: str,
) -> AuthData:
    """
    Queries authentication data from your token.
    :param token: token
    :param db: database object
    """

    # Decode external token and query auth data from it.
    return _query_auth_data(db=db, response=_decode_token(token))


def query_auth_data_from_request(db: SQLAlchemy) -> AuthData:
    """
    Queries authentication data from request (from request token).
    :param db: Database session.
    """

    # Get token from request and query data from it as external token.
    token = get_token_from_request()
    return query_auth_data_from_token(db=db, token=token)


def try_query_auth_data_from_request(db: SQLAlchemy) -> tuple[bool, AuthData | None]:
    """
    Tries query authentication data from request (from request token), and returns tuple with status and auth data.
    :param db: Database session.
    :returns: (status, auth_data)
    :rtype: tuple[bool, AuthData]
    """

    try:
        # Try to authenticate, and if does not fall, return OK.
        auth_data = query_auth_data_from_request(db=db)
    except ApiErrorException:
        # Any exception occurred - unable to authorize.
        return False, None
    else:
        return True, auth_data


def _internal_service_auth(db: SQLAlchemy, user_id: int) -> User:
    """Processes internal service auth, do signup if there is no user, or return user date if exists."""
    return crud.user.get_or_create(db=db, user_id=user_id)


def get_token_from_request() -> str:
    """
    Returns token from request.
    """

    # Simple access token located in header and params.
    # Notice that if user gives header and param, header should taken and param should skiped!
    token_header = flask_request.headers.get("Authorization", "")
    token_param = flask_request.args.get("access_token", "")
    return token_header or token_param


def is_authorized() -> bool:
    """
    Checks that request has authorization (header or query param).
    :rtype: bool
    """
    return bool(get_token_from_request())


def _decode_token(
    token: str,
) -> AuthData:
    """
    Decodes given token, to user data.
    :param token: Token to decode.
    """

    if not token:
        raise ApiErrorException(ApiErrorCode.AUTH_REQUIRED, "Authentication required!")

    # Request data.
    response = _check_token_with_sso_server(token)
    return response["success"]  # Return response.


def _query_scope_permissions(
    scope: str, required_permissions: list[Permission] | Permission | None = None
) -> list[Permission]:
    """
    Queries scope permissions with checking required permission (if passed).
    :param scope: Scope string (From request).
    :param required_permissions: Permissions to require, or just one permission, or no permissions.
    """
    permissions: list[Permission] = parse_permissions_from_scope(scope)

    if not required_permissions:
        # If no permissions that should be required,
        # simply return parsed permissions.
        return permissions

    if isinstance(required_permissions, Permission):
        # If specified only one permission,
        # convert it to list as expected.
        required_permissions = [required_permissions]

    # Filter scope permissions, and build list with only those permissions that not satisfied.
    unsatisfied_permissions = list(
        filter(lambda permission: permission not in permissions, required_permissions)
    )

    if unsatisfied_permissions:
        # If we have any permission that not satisfied.

        # String of scope of required permissions.
        required_scope = ", ".join(
            [permission.value for permission in unsatisfied_permissions]
        )

        raise ApiErrorException(
            ApiErrorCode.AUTH_INSUFFICIENT_PERMISSIONS,
            f"Insufficient permissions to call this method! (required scope permissions: {required_scope})",
            {"required_scope": required_scope},
        )

    return permissions


def _check_token_with_sso_server(token: str) -> dict[str, Any]:
    """
    Checks that token is valid with SSO server.
    :param token: Token to check.
    :returns: json response from server
    :rtype: dict[str, Any]
    """

    config = current_app.config
    url = f"{config['SSO_API_URL']}/{config['SSO_API_METHOD']}"
    logging.error(url)
    params = {"access_token": token, "required_scope": SSO_REQUESTED_SCOPE}

    try:
        response = request("GET", url, params=params).json()
    except JSONDecodeError as e:
        raise ApiErrorException(
            ApiErrorCode.API_EXTERNAL_SERVER_ERROR,
            "Unable to process your request due to server being down!",
        ) from e

    _check_sso_server_response(response)
    return response


def _check_sso_server_response(response: dict[str, Any]) -> None:
    """
    Checks SSO server response to not contain any error.
    :param dict response: json response from SSO server.
    """
    if "error" in response:
        error_code = response["error"]["code"]
        error_message = response["error"]["message"]

        if error_code in (10, 20):  # AUTH_INVALID_TOKEN
            raise ApiErrorException(ApiErrorCode.AUTH_INVALID_TOKEN, error_message)

        if error_code == 11:  # AUTH_EXPIRED_TOKEN
            raise ApiErrorException(ApiErrorCode.AUTH_EXPIRED_TOKEN, error_message)

        if error_code == 100:  # USER_DEACTIVATED
            raise ApiErrorException(ApiErrorCode.USER_DEACTIVATED, error_message)
        if error_code == 33:  # AUTH_INSUFFICIENT_PERMISSIONS
            raise ApiErrorException(
                ApiErrorCode.AUTH_INSUFFICIENT_PERMISSIONS, error_message
            )

        raise ApiErrorException(
            ApiErrorCode.API_EXTERNAL_SERVER_ERROR,
            f"Unable to process your request due to server being down (Or internal server error)! Additional error information: External server returned error code: {error_code}!",
        )


def _query_auth_data(
    db: SQLAlchemy,
    response: dict[str, Any],
) -> AuthData:
    """
    Finalizes query of authentication data by return DTO.
    :param SQLAlchemy db: database object
    :param dict[str, Any] response: json response from SSO server
    """
    permissions = _query_scope_permissions(response.get("scope"), [Permission.cc])
    user_id = response.get("user_id")
    user = _internal_service_auth(db, user_id)
    return AuthData(user_id=user_id, permissions=permissions, user=user)
