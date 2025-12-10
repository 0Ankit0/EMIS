from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.portal.models import (
    Dashboard, Widget, QuickLink, Announcement, AnnouncementView,
    StudentPortalProfile, FacultyPortalProfile, PortalActivity
)
from apps.students.models import Student, AcademicYear, Department
from apps.faculty.models import Faculty

User = get_user_model()


class DashboardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_dashboard_creation(self):
        dashboard = Dashboard.objects.create(
            user=self.user,
            role='student'
        )
        self.assertEqual(dashboard.user, self.user)
        self.assertEqual(dashboard.role, 'student')
        self.assertTrue(dashboard.is_active)
    
    def test_dashboard_str(self):
        dashboard = Dashboard.objects.create(
            user=self.user,
            role='student'
        )
        expected = f"{self.user.username} - student Dashboard"
        self.assertEqual(str(dashboard), expected)


class WidgetModelTest(TestCase):
    def test_widget_creation(self):
        widget = Widget.objects.create(
            name='Attendance Widget',
            widget_type='attendance',
            description='Shows attendance summary',
            roles=['student', 'faculty'],
            order=1
        )
        self.assertEqual(widget.name, 'Attendance Widget')
        self.assertEqual(widget.widget_type, 'attendance')
        self.assertTrue(widget.is_active)


class QuickLinkModelTest(TestCase):
    def test_quicklink_creation(self):
        link = QuickLink.objects.create(
            title='My Courses',
            url='/courses/',
            category='academic',
            roles=['student'],
            order=1
        )
        self.assertEqual(link.title, 'My Courses')
        self.assertEqual(link.category, 'academic')
        self.assertTrue(link.is_active)


class AnnouncementModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
    
    def test_announcement_creation(self):
        announcement = Announcement.objects.create(
            title='Test Announcement',
            content='This is a test announcement',
            author=self.user,
            priority='high',
            target_roles=['student'],
            is_published=True
        )
        self.assertEqual(announcement.title, 'Test Announcement')
        self.assertEqual(announcement.priority, 'high')
        self.assertTrue(announcement.is_published)
    
    def test_announcement_is_active(self):
        # Active announcement
        announcement = Announcement.objects.create(
            title='Active Announcement',
            content='Content',
            author=self.user,
            is_published=True,
            publish_date=timezone.now() - timedelta(days=1),
            expiry_date=timezone.now() + timedelta(days=1)
        )
        self.assertTrue(announcement.is_active())
        
        # Expired announcement
        expired = Announcement.objects.create(
            title='Expired Announcement',
            content='Content',
            author=self.user,
            is_published=True,
            publish_date=timezone.now() - timedelta(days=2),
            expiry_date=timezone.now() - timedelta(days=1)
        )
        self.assertFalse(expired.is_active())


class PortalActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_activity_creation(self):
        activity = PortalActivity.objects.create(
            user=self.user,
            activity_type='login',
            description='User logged in',
            ip_address='127.0.0.1'
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'login')


class PortalViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create academic year and department
        self.academic_year = AcademicYear.objects.create(
            year='2024-2025',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365),
            is_current=True
        )
        
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS'
        )
    
    def test_portal_home_requires_login(self):
        response = self.client.get('/portal/')
        self.assertEqual(response.status_code, 302)
    
    def test_portal_home_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/portal/')
        self.assertEqual(response.status_code, 200)


class DashboardAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_get_my_dashboard(self):
        Dashboard.objects.create(user=self.user, role='student')
        response = self.client.get('/api/portal/dashboards/my_dashboard/')
        self.assertEqual(response.status_code, 200)
