"""
    Functions for working with request/response headers.
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
