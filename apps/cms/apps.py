"""
Cms App Configuration
"""
from django.apps import AppConfig


class CmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cms'
    verbose_name = 'Cms'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.cms.signals
        except ImportError:
            pass
