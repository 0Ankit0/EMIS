"""
Notifications Tests
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import (
    Notification, NotificationTemplate, NotificationPreference,
    ScheduledNotification, NotificationLog, NotificationType
)
from .utils import send_notification, send_bulk_notifications, cleanup_old_notifications

User = get_user_model()


class NotificationModelTest(TestCase):
    """Test Notification model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@test.com',
            password='testpass123'
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            sender=self.sender,
            title='Test Notification',
            message='Test Message',
            notification_type='info',
            channels=['in_app']
        )
    
    def test_notification_creation(self):
        """Test notification can be created"""
        self.assertTrue(isinstance(self.notification, Notification))
        self.assertEqual(str(self.notification), f'Test Notification - {self.user.get_full_name()}')
    
    def test_notification_unread_default(self):
        """Test notification is unread by default"""
        self.assertFalse(self.notification.is_read)
        self.assertIsNone(self.notification.read_at)
    
    def test_mark_as_read(self):
        """Test marking notification as read"""
        self.notification.mark_as_read()
        self.assertTrue(self.notification.is_read)
        self.assertIsNotNone(self.notification.read_at)
    
    def test_mark_as_unread(self):
        """Test marking notification as unread"""
        self.notification.mark_as_read()
        self.notification.mark_as_unread()
        self.assertFalse(self.notification.is_read)
        self.assertIsNone(self.notification.read_at)


class NotificationManagerTest(TestCase):
    """Test Notification manager and queryset"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='other',
            email='other@test.com',
            password='testpass123'
        )
        
        # Create notifications
        self.unread = Notification.objects.create(
            recipient=self.user,
            title='Unread',
            message='Test',
            notification_type='info'
        )
        self.read = Notification.objects.create(
            recipient=self.user,
            title='Read',
            message='Test',
            notification_type='info',
            is_read=True
        )
        self.other = Notification.objects.create(
            recipient=self.other_user,
            title='Other',
            message='Test',
            notification_type='info'
        )
    
    def test_for_user(self):
        """Test for_user filter"""
        notifications = Notification.objects.for_user(self.user)
        self.assertEqual(notifications.count(), 2)
        self.assertIn(self.unread, notifications)
        self.assertIn(self.read, notifications)
        self.assertNotIn(self.other, notifications)
    
    def test_unread_filter(self):
        """Test unread filter"""
        unread = Notification.objects.for_user(self.user).unread()
        self.assertEqual(unread.count(), 1)
        self.assertIn(self.unread, unread)
    
    def test_read_filter(self):
        """Test read filter"""
        read = Notification.objects.for_user(self.user).read()
        self.assertEqual(read.count(), 1)
        self.assertIn(self.read, read)
    
    def test_by_type(self):
        """Test by_type filter"""
        notifications = Notification.objects.by_type('info')
        self.assertEqual(notifications.count(), 3)


class NotificationTemplateTest(TestCase):
    """Test NotificationTemplate model"""
    
    def setUp(self):
        """Set up test data"""
        self.template = NotificationTemplate.objects.create(
            name='Welcome Template',
            code='welcome',
            title_template='Welcome {{ user.first_name }}!',
            message_template='Hello {{ user.first_name }}, welcome to {{ platform }}',
            notification_type='info',
            default_channels=['in_app', 'email'],
            is_active=True
        )
    
    def test_template_creation(self):
        """Test template can be created"""
        self.assertTrue(isinstance(self.template, NotificationTemplate))
        self.assertEqual(str(self.template), 'Welcome Template')
    
    def test_template_render(self):
        """Test template rendering"""
        context = {
            'user': type('User', (), {'first_name': 'John'}),
            'platform': 'EMIS'
        }
        rendered = self.template.render(context)
        
        self.assertEqual(rendered['title'], 'Welcome John!')
        self.assertIn('John', rendered['message'])
        self.assertIn('EMIS', rendered['message'])


class NotificationPreferenceTest(TestCase):
    """Test NotificationPreference model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.preference = NotificationPreference.objects.create(
            user=self.user,
            enable_email=True,
            enable_sms=False,
            enable_push=True,
            enable_in_app=True
        )
    
    def test_preference_creation(self):
        """Test preference can be created"""
        self.assertTrue(isinstance(self.preference, NotificationPreference))
        self.assertEqual(self.preference.user, self.user)
    
    def test_default_preferences(self):
        """Test default preferences"""
        self.assertTrue(self.preference.enable_email)
        self.assertFalse(self.preference.enable_sms)


class UtilsTest(TestCase):
    """Test utility functions"""
    
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_send_notification(self):
        """Test sending single notification"""
        notification = send_notification(
            recipient=self.user1,
            title='Test',
            message='Test Message',
            notification_type='info',
            channels=['in_app']
        )
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.title, 'Test')
    
    def test_send_bulk_notifications(self):
        """Test sending bulk notifications"""
        count = send_bulk_notifications(
            recipients=[self.user1, self.user2],
            title='Bulk Test',
            message='Test Message',
            notification_type='info',
            channels=['in_app']
        )
        
        self.assertEqual(count, 2)
        self.assertEqual(Notification.objects.count(), 2)
    
    def test_cleanup_old_notifications(self):
        """Test cleanup of old notifications"""
        # Create old read notification
        old_notification = Notification.objects.create(
            recipient=self.user1,
            title='Old',
            message='Old message',
            is_read=True
        )
        old_notification.read_at = timezone.now() - timedelta(days=35)
        old_notification.save()
        
        # Create recent notification
        Notification.objects.create(
            recipient=self.user1,
            title='Recent',
            message='Recent message',
            is_read=True
        )
        
        # Cleanup
        deleted = cleanup_old_notifications(days=30)
        
        self.assertEqual(deleted, 1)
        self.assertEqual(Notification.objects.count(), 1)


class NotificationsViewsTest(TestCase):
    """Test notifications views"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.notification = Notification.objects.create(
            recipient=self.user,
            title='Test',
            message='Test Message'
        )
    
    def test_dashboard_view(self):
        """Test dashboard view"""
        response = self.client.get(reverse('notifications:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'notifications')
    
    def test_notification_list_view(self):
        """Test notification list view"""
        response = self.client.get(reverse('notifications:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_notification_detail_view(self):
        """Test notification detail view"""
        response = self.client.get(
            reverse('notifications:detail', kwargs={'pk': self.notification.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # Should be marked as read after viewing
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
    
    def test_preferences_view(self):
        """Test preferences view"""
        response = self.client.get(reverse('notifications:preferences'))
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        """Clean up"""
        self.client.logout()


class APITest(TestCase):
    """Test API endpoints"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.notification = Notification.objects.create(
            recipient=self.user,
            title='Test',
            message='Test Message'
        )
    
    def test_get_unread_count(self):
        """Test unread count API"""
        response = self.client.get(reverse('notifications:api_unread_count'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
    
    def test_mark_as_read_api(self):
        """Test mark as read API"""
        response = self.client.post(
            reverse('notifications:mark_read', kwargs={'pk': self.notification.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
    
    def tearDown(self):
        """Clean up"""
        self.client.logout()
