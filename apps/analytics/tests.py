"""
Analytics Tests
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import AnalyticsItem

User = get_user_model()


class AnalyticsItemModelTest(TestCase):
    """Test AnalyticsItem model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.item = AnalyticsItem.objects.create(
            name='Test Item',
            description='Test Description',
            status='active',
            created_by=self.user
        )
    
    def test_item_creation(self):
        """Test item can be created"""
        self.assertTrue(isinstance(self.item, AnalyticsItem))
        self.assertEqual(str(self.item), 'Test Item')
    
    def test_item_status(self):
        """Test item status"""
        self.assertEqual(self.item.status, 'active')
    
    def test_item_created_by(self):
        """Test item created_by"""
        self.assertEqual(self.item.created_by, self.user)


class AnalyticsViewsTest(TestCase):
    """Test analytics views"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_dashboard_view(self):
        """Test dashboard view"""
        response = self.client.get(reverse('analytics:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        """Clean up"""
        self.client.logout()
