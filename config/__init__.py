"""
EMIS Configuration Package
"""
# Import celery app to ensure it's loaded
from .celery import app as celery_app

__all__ = ('celery_app',)
