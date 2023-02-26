"""
    Services for working with request params (GET, POST) from flask `request` object.
"""
from typing import Any, TypeVar

from flask import request
import pydantic

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
        param = pydantic.parse_obj_as(bool, param)
    if type_ == int:
        # Int conversion can be change
        param = pydantic.parse_obj_as(int, param)

    return param
