"""Calendar App Configuration"""
from django.apps import AppConfig


class CalendarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.calendar'
    verbose_name = 'Calendar Management'
    
    def ready(self):
        import apps.calendar.signals
