from django.apps import AppConfig


class CalendarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.calendar'

    def ready(self):
        """Import signal handlers."""
        try:
            import apps.calendar.signals.event_remainder  
        except ImportError:
            pass