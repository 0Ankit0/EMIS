"""
LMS App Configuration
"""
from django.apps import AppConfig


class LmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lms'
    verbose_name = 'Learning Management System'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.lms.signals
        except ImportError:
            pass
