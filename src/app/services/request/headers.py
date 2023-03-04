"""
    Functions for working with request/response headers.
"""
from flask import request


def get_ip() -> str:
    """
    Returns IP from X-Forwared-From header. If IP is hidden, returns 'untrackable'.
    """
    if "X-Forwarded-For" in request.headers:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(" ")[-1]
    else:
        remote_addr = request.remote_addr or "untrackable"

    return remote_addr
