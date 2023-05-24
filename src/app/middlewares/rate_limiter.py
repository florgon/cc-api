"""
    Rate limiter middleware that calls check_rate_limit function.
"""
from flask import Request, Blueprint

from app.services.rate_limiter import check_rate_limit
from app.services.api.errors import ApiErrorException


bp_rate_limiter = Blueprint("rate_limiter", __name__)

@bp_rate_limiter.before_app_request
def rate_limiter():
    check_rate_limit(15, minutes=1)

