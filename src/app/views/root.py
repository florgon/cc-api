#!usr/bin/python
"""
    URL shortener application root views.
"""

from urllib.parse import urlparse

from flask import Blueprint, request, redirect

from .. import db
from ..models.url import Url


bp_root = Blueprint("root", __name__)


@bp_root.route("/", methods=["GET"])
def root_index():
    return "URL shortener application."


@bp_root.route("/add", methods=["GET"])
def root_add():
    url_redirect = request.args.get("for", type=str, default="")
    if url_redirect:
        url_parsed = urlparse(url_redirect)
        url_is_valid = all([url_parsed.scheme, url_parsed.netloc])
        if url_is_valid:
            url = Url(url_redirect)
            db.session.add(url)
            db.session.commit()
            return f"Successfully added new URL with ID {url.id} that references (redirects) to URL {url_redirect}!"
        return "Failed to add new URL! Error: invalid URL to redirect! It should contain scheme and netloc!"
    return "Failed to add new URL! Error: invalid `for` GET parameter."


@bp_root.route("/<url_id>", methods=["GET"])
def root_get(url_id):
    url = Url.query.filter_by(id=url_id).first_or_404()

    url.views += 1
    db.session.commit()

    return redirect(url.redirect, 303)


@bp_root.route("/stats/<url_id>", methods=["GET"])
def root_stats(url_id):
    url = Url.query.filter_by(id=url_id).first_or_404()

    return str(url.views)
