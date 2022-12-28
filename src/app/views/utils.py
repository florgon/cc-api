"""
    URL shortener application utils views.
"""
from time import time

from flask import Blueprint

from app.services.api.response import api_success

bp_utils = Blueprint("utils", __name__)


@bp_utils.route("/serverTime", methods=["GET"])
def get_server_time():
    """
    Returns current time at the server, used for debugging.
    """
    return api_success({"server_time": time()})


