"""
    Functions for working with request/response headers.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from flask import request


def get_ip() -> str:
    """
    Returns IP from HTTP_CF_CONNECTING_IP header. If IP is hidden, returns 'untrackable'.
    :rtype: str
    :return: IP
    """
    if "HTTP_CF_CONNECTING_IP" in request.headers:
        remote_addr = request.headers.get("HTTP_CF_CONNECTING_IP")
    else:
        remote_addr = request.remote_addr or "untrackable"

    return remote_addr
