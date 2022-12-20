"""
    Handlers for exceptions in app.
"""
from flask import Blueprint

from app.services.api.errors import ApiErrorException
from app.services.api.response import api_error

bp_handlers = Blueprint("exception_handlers", __name__)

@bp_handlers.app_errorhandler(ApiErrorException)
def api_error_exception_to_response(e: ApiErrorException):
    """
    Return api error from raised ApiErrorException
    """
    return api_error(e.api_code, e.message, e.data)
