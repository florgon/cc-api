"""
    Services for validating and generating qr-codes.
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

from typing import NoReturn, Any, overload, Literal
from io import BytesIO

import pyqrcode

from app.services.api.errors import ApiErrorCode, ApiErrorException


@overload
def generate_qr_code(
    text: str, result_type: Literal["txt"], scale: int = 3, quiet_zone: int = 4
) -> str:
    ...


@overload
def generate_qr_code(
    text: str, result_type: Literal["png", "xml"], scale: int = 3, quiet_zone: int = 4
) -> tuple[bytes, int, dict[str, Any]]:
    """
    :returns: tuple in format: (response text, http response code, headers dict)
    """
    ...


def generate_qr_code(text: str, result_type: str, scale: int = 3, quiet_zone: int = 4):
    """
    Generates qr-code for given text using given params.
    :param str text: text to be encoded in qr-code.
    :param str result_type: type of expected result. May be one of: png, xml, txt.
    :param int scale: scaling of image. Defaults to 3.
    :param int quiet_zone: white border around qr-code.
    :rtype: str or tuple[bytes, int, dict[str, Any]]
    :return: str if result type is txt.
             tuple[bytes, int, dict[str, Any]] if result type is png, xml
             Returned object should be returned from view as is.
    """
    qr_code = pyqrcode.create(text)
    if result_type == "txt":
        return qr_code.text()

    qr_code_stream = BytesIO()
    if result_type == "svg":
        qr_code.svg(qr_code_stream, scale=scale, quiet_zone=quiet_zone)
    elif result_type == "png":
        qr_code.png(qr_code_stream, scale=scale, quiet_zone=quiet_zone)

    headers_no_cache = get_no_cache_headers_for_qr_code(result_type, qr_code_stream)
    return qr_code_stream.getvalue(), 200, headers_no_cache


def validate_qr_result_type(result_type: str) -> None | NoReturn:
    """
    Validates qr-code result type (from user request args).
    :param str result_type: type of expected result.
    :rtype: None | NoReturn
    :return: None if successfully, NoReturn (API Error) if not
    """
    if result_type not in ("svg", "txt", "png"):
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "Expected `result_type` to be `svg`, `png` or `txt`!",
        )


def validate_qr_code_scale(scale: str) -> None | NoReturn:
    """
    Validates qr-code scale (from user request args). Should be number from 0 to 8
    :param str scale: scale
    :rtype: None | NoReturn
    :return: None if successfully, NoReturn (API Error) if not
    """
    if not scale.isdigit() or scale == "0" or int(scale) > 8:
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "`scale` argument must be an integer number in range from 1 to 8!",
        )


def validate_qr_code_quiet_zone(quiet_zone: str) -> None | NoReturn:
    """
    Validates qr-code quiet zone (from user request args).
    :param str quiet_zone: quiet zone (white border around qr-code)
    :rtype: None | NoReturn
    :return: None if successfully, NoReturn (API Error) if not
    """
    if not quiet_zone.isdigit() or int(quiet_zone) > 25:
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "`quiet_zone` argument must be an integer number in range from 0 to 25!",
        )


def get_content_type_header_for_result_type(result_type: str) -> str:
    match result_type:
        case "png":
            return "image/png"
        case "svg":
            return "image/svg+xml"
        case _:
            return "text/plain"


def get_no_cache_headers_for_qr_code(
    result_type: str, qr_code_stream: BytesIO
) -> dict[str, Any]:
    """
    Returns headers to disable caching for image.
    """
    return {
        "Content-Type": get_content_type_header_for_result_type(result_type),
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
        "Content-Length": str(qr_code_stream.getbuffer().nbytes),
    }
