"""
Library App Configuration
"""
from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.library'
    verbose_name = 'Library'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.library.signals
        except ImportError:
            pass
