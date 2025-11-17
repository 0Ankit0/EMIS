"""
Redis caching utilities for EMIS
"""

import hashlib
from functools import wraps
from typing import Any, Callable, Optional

from django.conf import settings
from django.core.cache import cache


class CacheService:
    """Service for managing Redis cache operations"""

    DEFAULT_TIMEOUT = getattr(settings, "CACHE_DEFAULT_TIMEOUT", 300)  # 5 minutes

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get value from cache"""
        return cache.get(key, default)

    @staticmethod
    def set(key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """Set value in cache with optional timeout"""
        if timeout is None:
            timeout = CacheService.DEFAULT_TIMEOUT
        return cache.set(key, value, timeout)

    @staticmethod
    def delete(key: str) -> bool:
        """Delete key from cache"""
        return cache.delete(key)

    @staticmethod
    def clear_pattern(pattern: str):
        """Clear all keys matching pattern (requires Redis)"""
        try:
            from django.core.cache import caches

            redis_cache = caches["default"]
            if hasattr(redis_cache, "delete_pattern"):
                redis_cache.delete_pattern(pattern)
        except Exception:
            pass

    @staticmethod
    def get_or_set(
        key: str, default_func: Callable, timeout: Optional[int] = None
    ) -> Any:
        """Get value from cache or compute and cache it"""
        value = CacheService.get(key)
        if value is None:
            value = default_func()
            CacheService.set(key, value, timeout)
        return value


def cache_key(*args, prefix: str = "", **kwargs) -> str:
    """
    Generate a cache key from arguments

    Args:
        *args: Positional arguments to include in key
        prefix: Prefix for the cache key
        **kwargs: Keyword arguments to include in key

    Returns:
        String cache key
    """
    # Create a stable representation of args and kwargs
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_string = ":".join(key_parts)

    # Hash if too long
    if len(key_string) > 200:
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        key_string = key_hash

    if prefix:
        return f"{prefix}:{key_string}"
    return key_string


def cached(timeout: int = None, key_prefix: str = ""):
    """
    Decorator to cache function results

    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for cache keys

    Example:
        @cached(timeout=300, key_prefix='users')
        def get_user(user_id):
            return User.objects.get(id=user_id)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            func_name = f"{func.__module__}.{func.__name__}"
            key = cache_key(*args, prefix=f"{key_prefix}:{func_name}", **kwargs)

            # Try to get from cache
            result = CacheService.get(key)
            if result is not None:
                return result

            # Compute and cache result
            result = func(*args, **kwargs)
            CacheService.set(key, result, timeout)
            return result

        return wrapper

    return decorator


# Specialized caching functions for frequently accessed data


def cache_role(role_id: str, role_data: dict, timeout: int = 3600):
    """Cache role data (1 hour default)"""
    key = f"role:{role_id}"
    CacheService.set(key, role_data, timeout)


def get_cached_role(role_id: str) -> Optional[dict]:
    """Get cached role data"""
    key = f"role:{role_id}"
    return CacheService.get(key)


def invalidate_role_cache(role_id: str):
    """Invalidate cached role data"""
    key = f"role:{role_id}"
    CacheService.delete(key)


def cache_permission(permission_id: str, permission_data: dict, timeout: int = 3600):
    """Cache permission data (1 hour default)"""
    key = f"permission:{permission_id}"
    CacheService.set(key, permission_data, timeout)


def get_cached_permission(permission_id: str) -> Optional[dict]:
    """Get cached permission data"""
    key = f"permission:{permission_id}"
    return CacheService.get(key)


def invalidate_permission_cache(permission_id: str):
    """Invalidate cached permission data"""
    key = f"permission:{permission_id}"
    CacheService.delete(key)


def cache_user_permissions(user_id: str, permissions: list, timeout: int = 1800):
    """Cache user permissions (30 minutes default)"""
    key = f"user_permissions:{user_id}"
    CacheService.set(key, permissions, timeout)


def get_cached_user_permissions(user_id: str) -> Optional[list]:
    """Get cached user permissions"""
    key = f"user_permissions:{user_id}"
    return CacheService.get(key)


def invalidate_user_permissions_cache(user_id: str):
    """Invalidate cached user permissions"""
    key = f"user_permissions:{user_id}"
    CacheService.delete(key)


def invalidate_all_role_caches():
    """Invalidate all role-related caches"""
    CacheService.clear_pattern("role:*")
    CacheService.clear_pattern("user_permissions:*")


def invalidate_all_permission_caches():
    """Invalidate all permission-related caches"""
    CacheService.clear_pattern("permission:*")
    CacheService.clear_pattern("user_permissions:*")
