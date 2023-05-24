"""
    Rate limiter middleware that calls check_rate_limit function.
"""
from app.services.rate_limiter import check_rate_limit


class RateLimiterMiddleware():
    """Calls check_rate_limit_function."""
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app
        self.minutes_window = 1
        self.requests_limit = 10
    def __call__(self, environ, start_response):
        check_rate_limit(self.requests_limit, minutes=self.minutes_window)
        return self.wsgi_app(environ, start_response)

