from django.core.management.base import BaseCommand
from apps.portal.models import QuickLink


class Command(BaseCommand):
    help = 'Initialize default quick links'

    def handle(self, *args, **options):
        quick_links = [
            {
                'title': 'My Courses',
                'url': '/courses/my-courses/',
                'description': 'View and manage your enrolled courses',
                'icon': 'fa-book',
                'category': 'academic',
                'roles': ['student'],
                'order': 1,
            },
            {
                'title': 'Attendance',
                'url': '/attendance/',
                'description': 'View attendance records',
                'icon': 'fa-calendar-check',
                'category': 'academic',
                'roles': ['student', 'faculty'],
                'order': 2,
            },
            {
                'title': 'Grades',
                'url': '/exams/grades/',
                'description': 'View your grades and results',
                'icon': 'fa-graduation-cap',
                'category': 'academic',
                'roles': ['student'],
                'order': 3,
            },
            {
                'title': 'Timetable',
                'url': '/timetable/',
                'description': 'View class schedule',
                'icon': 'fa-clock',
                'category': 'academic',
                'roles': ['student', 'faculty'],
                'order': 4,
            },
            {
                'title': 'Library',
                'url': '/library/',
                'description': 'Access library resources',
                'icon': 'fa-book-open',
                'category': 'resources',
                'roles': ['student', 'faculty'],
                'order': 5,
            },
            {
                'title': 'Fee Payment',
                'url': '/finance/fees/',
                'description': 'Pay fees and view payment history',
                'icon': 'fa-money-bill',
                'category': 'administrative',
                'roles': ['student'],
                'order': 6,
            },
            {
                'title': 'Profile Settings',
                'url': '/portal/settings/profile/',
                'description': 'Manage your profile',
                'icon': 'fa-user-cog',
                'category': 'services',
                'roles': ['student', 'faculty'],
                'order': 7,
            },
            {
                'title': 'Help & Support',
                'url': '/help/',
                'description': 'Get help and support',
                'icon': 'fa-question-circle',
                'category': 'services',
                'roles': ['student', 'faculty'],
                'order': 8,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for link_data in quick_links:
            link, created = QuickLink.objects.update_or_create(
                title=link_data['title'],
                defaults=link_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created quick link: {link.title}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated quick link: {link.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully initialized {created_count} new quick links and updated {updated_count} existing quick links'
            )
        )
