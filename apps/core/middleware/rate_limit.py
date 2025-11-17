"""
Rate limiting middleware for authentication endpoints
"""

import time
from typing import Callable

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware using Redis
    Limits requests per IP address
    """

    # Rate limit configuration
    RATE_LIMITS = {
        "/auth/login": (5, 300),  # 5 requests per 5 minutes
        "/auth/register": (3, 600),  # 3 requests per 10 minutes
        "/auth/password-reset": (3, 600),  # 3 requests per 10 minutes
    }

    DEFAULT_RATE_LIMIT = (100, 60)  # 100 requests per minute for other endpoints

    def process_request(self, request):
        """Check rate limit before processing request"""
        # Skip rate limiting for non-auth endpoints in production
        path = request.path

        # Get rate limit for this endpoint
        max_requests, window_seconds = self._get_rate_limit(path)

        # Get client IP
        client_ip = self._get_client_ip(request)

        # Create cache key
        cache_key = f"rate_limit:{client_ip}:{path}"

        # Get current request count
        request_data = cache.get(cache_key)

        if request_data is None:
            # First request in this window
            cache.set(
                cache_key,
                {"count": 1, "reset_at": time.time() + window_seconds},
                window_seconds,
            )
            return None

        # Check if window has expired
        if time.time() > request_data.get("reset_at", 0):
            # Reset window
            cache.set(
                cache_key,
                {"count": 1, "reset_at": time.time() + window_seconds},
                window_seconds,
            )
            return None

        # Increment request count
        request_data["count"] += 1

        # Check if limit exceeded
        if request_data["count"] > max_requests:
            retry_after = int(request_data["reset_at"] - time.time())
            return JsonResponse(
                {
                    "error": "Rate limit exceeded",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": f"Too many requests. Please try again in {retry_after} seconds.",
                    "retry_after": retry_after,
                },
                status=429,
            )

        # Update request count
        cache.set(cache_key, request_data, window_seconds)
        return None

    def _get_rate_limit(self, path: str) -> tuple:
        """Get rate limit for endpoint"""
        for endpoint, limit in self.RATE_LIMITS.items():
            if endpoint in path:
                return limit
        return self.DEFAULT_RATE_LIMIT

    def _get_client_ip(self, request) -> str:
        """Get client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Decorator for rate limiting specific views

    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds

    Example:
        @rate_limit(max_requests=10, window_seconds=60)
        def my_view(request):
            ...
    """

    def decorator(view_func: Callable) -> Callable:
        def wrapper(request, *args, **kwargs):
            # Get client IP
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(",")[0].strip()
            else:
                client_ip = request.META.get("REMOTE_ADDR")

            # Create cache key
            cache_key = f"rate_limit:{client_ip}:{request.path}"

            # Get current request count
            request_data = cache.get(cache_key)

            if request_data is None:
                # First request in this window
                cache.set(
                    cache_key,
                    {"count": 1, "reset_at": time.time() + window_seconds},
                    window_seconds,
                )
                return view_func(request, *args, **kwargs)

            # Check if window has expired
            if time.time() > request_data.get("reset_at", 0):
                # Reset window
                cache.set(
                    cache_key,
                    {"count": 1, "reset_at": time.time() + window_seconds},
                    window_seconds,
                )
                return view_func(request, *args, **kwargs)

            # Increment request count
            request_data["count"] += 1

            # Check if limit exceeded
            if request_data["count"] > max_requests:
                retry_after = int(request_data["reset_at"] - time.time())
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded",
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Too many requests. Please try again in {retry_after} seconds.",
                        "retry_after": retry_after,
                    },
                    status=429,
                )

            # Update request count
            cache.set(cache_key, request_data, window_seconds)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
