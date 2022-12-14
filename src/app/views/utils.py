"""
    URL shortener application utils views.
"""
from time import time

from flask import Blueprint
from app.services.response import api_success

bp_utils = Blueprint("utils", __name__)


@bp_utils.route("/utils.getServerTime", methods=["GET"])
def get_server_time():
    return api_success({"server_time": time()})


