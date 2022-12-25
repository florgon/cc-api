"""
    API Response wrappers.
"""
import json


from flask import Response, jsonify, make_response

from .errors import ApiErrorCode
from .version import API_VERSION


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
