"""
Transport App Configuration
"""
from django.apps import AppConfig


class TransportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.transport'
    verbose_name = 'Transport'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.transport.signals
        except ImportError:
            pass
