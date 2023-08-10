"""
    Blueprint that provides info about API source code.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
