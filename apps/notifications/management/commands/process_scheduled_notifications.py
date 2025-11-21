"""
Management command to process scheduled notifications
Run with: python manage.py process_scheduled_notifications
"""
from django.core.management.base import BaseCommand
from apps.notifications.utils import process_scheduled_notifications


class Command(BaseCommand):
    help = 'Process and send scheduled notifications that are due'
    
    def handle(self, *args, **options):
        self.stdout.write('Processing scheduled notifications...')
        
        try:
            count = process_scheduled_notifications()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully processed {count} scheduled notifications')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing scheduled notifications: {str(e)}')
            )
