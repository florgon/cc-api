"""
    API Response wrappers.
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
import json


from flask import Response, jsonify, make_response

from app.services.api.errors import ApiErrorCode
from app.services.api.version import API_VERSION


def api_error(
    api_code: ApiErrorCode,
    message: str = "",
    data: dict | None = None,
    headers: dict | None = None,
) -> Response:
    """Returns API error response."""

    if data is None:
        data = {}
    if headers is None:
        headers = {}

    code, status = api_code.value

    response = make_response(
        json.dumps(
            {
                "v": API_VERSION,
                "error": {
                    "message": message,
                    "code": code,
                    "status": status,
                    **data,
                },
            }
        )
    )
    response.headers.extend(headers)
    response.headers["Content-Type"] = "application/json"
    response.status = status

    return response


def api_success(data: dict, *, http_status: int = 200) -> tuple[Response, int]:
    """Returns API success response."""
    return jsonify({"v": API_VERSION, "success": data}), http_status
