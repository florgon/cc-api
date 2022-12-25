"""
    Handlers for exceptions in app.
"""
from flask import Blueprint
from werkzeug.exceptions import HTTPException

from app.services.api.errors import ApiErrorException
from app.services.api.response import api_error, ApiErrorCode

bp_handlers = Blueprint("exception_handlers", __name__)


@bp_handlers.app_errorhandler(ApiErrorException)
def api_error_exception_to_response(e: ApiErrorException):
    """
    Return api error from raised ApiErrorException
    """
    return api_error(e.api_code, e.message, e.data)


@bp_handlers.app_errorhandler(Exception)
def http_500_error_handler(e: Exception):
    """
    HTTP 500 status code error handler.
    """
    # Pass directly as http direct exception.
    if isinstance(e, HTTPException):
        return e

    return api_error(ApiErrorCode.API_INTERNAL_SERVER_ERROR, "Internal server error!")


@bp_handlers.app_errorhandler(404)
def http_404_error_handler(_):
    """
    HTTP 404 status code error handler.
    """
    return api_error(
        ApiErrorCode.API_METHOD_NOT_FOUND,
        "Method not found! Please read documentation!",
    )


@bp_handlers.app_errorhandler(429)
def http_429_error_handler(_):
    """
    HTTP 429 status code error handler.
    """
    return api_error(
        ApiErrorCode.API_TOO_MANY_REQUESTS,
        "Too many requests! You are sending requests too fast!",
    )


@bp_handlers.app_errorhandler(405)
def http_405_error_handler(_):
    """
    HTTP 405 status code error handler.
    """
    return api_error(
        ApiErrorCode.API_METHOD_NOT_ALLOWED,
        "HTTP Method not allowed!",
    )
