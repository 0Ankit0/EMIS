"""
Faculty App Configuration
"""
from django.apps import AppConfig


class FacultyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.faculty'
    verbose_name = 'Faculty'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.faculty.signals
        except ImportError:
            pass
