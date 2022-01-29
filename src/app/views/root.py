#!usr/bin/python
"""
    URL shortener application root views.
"""

from flask import Blueprint

bp_root = Blueprint("root", __name__)


@bp_root.route("/", methods=["GET"])
def root_index():
    return "URL shortener application."


@bp_root.route("/<url_index>", methods=["GET"])
def root_url(url_index):
    return str(url_index)
