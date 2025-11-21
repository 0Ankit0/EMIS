"""Hostel App Configuration"""
from django.apps import AppConfig


class HostelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hostel'
    verbose_name = 'Hostel Management'
    
    def ready(self):
        """Import signals when app is ready"""
        import apps.hostel.signals
