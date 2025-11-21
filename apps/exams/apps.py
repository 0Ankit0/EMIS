"""
Exams App Configuration
"""
from django.apps import AppConfig


class ExamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.exams'
    verbose_name = 'Exams'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.exams.signals
        except ImportError:
            pass
