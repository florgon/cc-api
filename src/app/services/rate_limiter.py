"""
    Provides a function that limits requests count from user.
"""
from flask import request, current_app
import redis

from app.services.request.headers import get_ip
from app.services.api.errors import ApiErrorException, ApiErrorCode


def check_rate_limit(
    requests_limit: int,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
) -> None:
    seconds = seconds + minutes * 60 + hours * 3600
    ip = get_ip()
    key = f"rate_limiter:{ip}:{request.endpoint}"

    r = redis.from_url(current_app.config["REDIS_DSN"])
    value = r.get(key)
    if not value:
        r.set(key, 1)
        r.expire(key, seconds)
    else:
        if int(value) + 1 >= requests_limit:
            ttl = r.ttl(key)
            raise ApiErrorException(
                ApiErrorCode.API_TOO_MANY_REQUESTS,
                "Too many requests! You are sending requests too fast!",
                headers={"Retry-After": ttl}
            )

        r.incr(key)

