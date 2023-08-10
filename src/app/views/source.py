"""
    Blueprint that provides info about API source code.
"""

from flask import Blueprint

from app.services.api.response import api_success

bp_source = Blueprint("source", __name__)

@bp_source.route("/", methods=["GET"])
def source_index():
    return api_success({
        "license": "AGPLv3+",
        "repository": "https://github.com/florgon/cc-api",
        "download": "https://github.com/florgon/cc-api/archive/refs/heads/main.zip",
    })
