"""
Health check and readiness endpoints
"""

import time

from django.core.cache import cache
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Basic health check endpoint
    Returns 200 if service is running
    """
    return Response(
        {"status": "healthy", "service": "EMIS", "timestamp": time.time()},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def readiness_check(request):
    """
    Readiness check endpoint
    Verifies database and Redis connectivity
    """
    checks = {"database": False, "cache": False, "overall": False}
    errors = []

    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = True
    except Exception as e:
        errors.append(f"Database error: {str(e)}")

    # Check Redis/cache connectivity
    try:
        cache_key = "__health_check__"
        cache.set(cache_key, "ok", 10)
        cache_value = cache.get(cache_key)
        if cache_value == "ok":
            checks["cache"] = True
        else:
            errors.append("Cache read/write verification failed")
        cache.delete(cache_key)
    except Exception as e:
        errors.append(f"Cache error: {str(e)}")

    # Overall status
    checks["overall"] = checks["database"] and checks["cache"]

    response_status = (
        status.HTTP_200_OK if checks["overall"] else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    response_data = {
        "status": "ready" if checks["overall"] else "not_ready",
        "checks": checks,
        "timestamp": time.time(),
    }

    if errors:
        response_data["errors"] = errors

    return Response(response_data, status=response_status)


@api_view(["GET"])
@permission_classes([AllowAny])
def liveness_check(request):
    """
    Liveness check endpoint
    Returns 200 if the service is alive
    """
    return Response(
        {"status": "alive", "timestamp": time.time()}, status=status.HTTP_200_OK
    )
