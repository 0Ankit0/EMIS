"""
Admissions App Configuration
"""
from django.apps import AppConfig


class AdmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admissions'
    verbose_name = 'Admissions'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.admissions.signals
        except ImportError:
            pass
