#!usr/bin/python
"""
    URL shortener application root views.
"""

from flask import Blueprint, request

from .. import db
from ..models.url import Url

bp_root = Blueprint("root", __name__)


@bp_root.route("/", methods=["GET"])
def root_index():
    return "URL shortener application."


@bp_root.route("/add", methods=["GET"])
def root_add():
    url_redirect = request.args.get("for")

    if url_redirect:
        url = Url(url_redirect)
        db.session.add(url)
        db.session.commit()
        return f"Successfully added new URL with ID {url.id} that references (redirects) to URL {url_redirect}"
    return "Failed to add new URL!"


@bp_root.route("/<url_code>", methods=["GET"])
def root_get(url_code):
    return str(url_code)
