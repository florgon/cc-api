"""
    URL shortener application utils views.
"""
from time import time

from flask import Blueprint, jsonify

bp_utils = Blueprint("utils", __name__)


@bp_utils.route("/utils.getServerTime", methods=["GET"])
def get_server_time():
    return jsonify(server_time=time())


