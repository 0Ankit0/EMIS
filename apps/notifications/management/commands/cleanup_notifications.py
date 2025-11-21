"""
Management command to clean up old read notifications
Run with: python manage.py cleanup_notifications --days 30
"""
from django.core.management.base import BaseCommand
from apps.notifications.utils import cleanup_old_notifications


class Command(BaseCommand):
    help = 'Clean up old read notifications'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days to keep notifications (default: 30)'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        self.stdout.write(f'Cleaning up notifications older than {days} days...')
        
        try:
            count = cleanup_old_notifications(days=days)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} old notifications')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning up notifications: {str(e)}')
            )
