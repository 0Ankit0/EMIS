from django.core.management.base import BaseCommand
from apps.portal.models import Widget


class Command(BaseCommand):
    help = 'Initialize default portal widgets'

    def handle(self, *args, **options):
        widgets = [
            {
                'name': 'Attendance Summary',
                'widget_type': 'attendance',
                'description': 'Shows attendance summary and statistics',
                'roles': ['student', 'faculty'],
                'order': 1,
            },
            {
                'name': 'Grades Overview',
                'widget_type': 'grades',
                'description': 'Displays recent grades and performance',
                'roles': ['student'],
                'order': 2,
            },
            {
                'name': 'Announcements',
                'widget_type': 'announcements',
                'description': 'Latest announcements and notices',
                'roles': ['student', 'faculty', 'admin'],
                'order': 3,
            },
            {
                'name': 'Class Schedule',
                'widget_type': 'schedule',
                'description': 'Today\'s class schedule',
                'roles': ['student', 'faculty'],
                'order': 4,
            },
            {
                'name': 'Assignments',
                'widget_type': 'assignments',
                'description': 'Pending and upcoming assignments',
                'roles': ['student', 'faculty'],
                'order': 5,
            },
            {
                'name': 'Fee Status',
                'widget_type': 'fees',
                'description': 'Fee payment status and dues',
                'roles': ['student'],
                'order': 6,
            },
            {
                'name': 'Notifications',
                'widget_type': 'notifications',
                'description': 'Recent notifications',
                'roles': ['student', 'faculty', 'admin'],
                'order': 7,
            },
            {
                'name': 'Calendar',
                'widget_type': 'calendar',
                'description': 'Academic calendar and events',
                'roles': ['student', 'faculty'],
                'order': 8,
            },
            {
                'name': 'Performance Chart',
                'widget_type': 'performance',
                'description': 'Performance trends and analytics',
                'roles': ['student', 'faculty'],
                'order': 9,
            },
            {
                'name': 'Quick Links',
                'widget_type': 'quick_links',
                'description': 'Quick access to important links',
                'roles': ['student', 'faculty', 'admin'],
                'order': 10,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for widget_data in widgets:
            widget, created = Widget.objects.update_or_create(
                widget_type=widget_data['widget_type'],
                defaults=widget_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created widget: {widget.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated widget: {widget.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully initialized {created_count} new widgets and updated {updated_count} existing widgets'
            )
        )
