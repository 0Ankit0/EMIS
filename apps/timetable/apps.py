"""
Timetable App Configuration
"""
from django.apps import AppConfig


class TimetableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.timetable'
    verbose_name = 'Timetable'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.timetable.signals
        except ImportError:
            pass
