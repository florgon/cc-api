"""
    Services for working with request params (GET, POST) from flask `request` object.
"""
from typing import TypeVar

from flask import request
import pydantic

from app.services.api.errors import ApiErrorCode, ApiErrorException

T = TypeVar("T")


def get_post_param(name: str, default: str = "", type_: type | None = T) -> T:
    """
    Returns value of post request parameter (from post or from json).
    :param str name: name of parameter
    :param str default: default value that will return if param not found. defaults to empty string."
    :param type type_: type of result variable.
    :returns: value of param
    """
    if request.is_json:
        param = request.get_json().get(name, default)
    else:
        param = request.form.get(name, default)

    if type_ == bool:
        param = _parse_as_bool(param)
    if type_ == int:
        # Int conversion can be changed
        param = pydantic.parse_obj_as(int, param)

    return param


def _parse_as_bool(param: str) -> bool:
    """
    Parses string param as bool.
    :param str param: str object to parse
    :rtype: bool
    :raises ApiErrorException: if param is invalid to parse.
    """
    try:
        return pydantic.parse_obj_as(bool, param)
    except pydantic.ValidationError as exc:
        # TODO: Return param name in error instead of 'param'
        raise ApiErrorException(ApiErrorCode.API_INVALID_REQUEST, "param is invalid bool!") from exc
