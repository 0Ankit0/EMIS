from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.portal.models import PortalActivity


class Command(BaseCommand):
    help = 'Clean up old portal activity logs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Delete activities older than this many days (default: 90)',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Count activities to be deleted
        count = PortalActivity.objects.filter(created_at__lt=cutoff_date).count()
        
        if count == 0:
            self.stdout.write(
                self.style.WARNING(f'No activities found older than {days} days')
            )
            return
        
        # Delete old activities
        deleted = PortalActivity.objects.filter(created_at__lt=cutoff_date).delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {deleted[0]} portal activities older than {days} days'
            )
        )
