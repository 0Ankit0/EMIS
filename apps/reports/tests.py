"""
Reports Tests
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import (
    ReportTemplate, GeneratedReport, ScheduledReport,
    ReportWidget, ReportFavorite
)

User = get_user_model()


class ReportTemplateModelTest(TestCase):
    """Test ReportTemplate model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.template = ReportTemplate.objects.create(
            name='Test Report',
            code='test-report',
            category='academic',
            created_by=self.user,
            is_active=True
        )
    
    def test_template_creation(self):
        """Test template is created correctly"""
        self.assertEqual(self.template.name, 'Test Report')
        self.assertEqual(self.template.code, 'test-report')
        self.assertTrue(self.template.is_active)
    
    def test_template_str(self):
        """Test template string representation"""
        self.assertEqual(str(self.template), 'Test Report')


class GeneratedReportModelTest(TestCase):
    """Test GeneratedReport model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.template = ReportTemplate.objects.create(
            name='Test Report',
            code='test-report',
            category='academic',
            created_by=self.user
        )
        
        self.generated = GeneratedReport.objects.create(
            template=self.template,
            title='Generated Test Report',
            generated_by=self.user,
            format='pdf',
            status='completed'
        )
    
    def test_generated_report_creation(self):
        """Test generated report is created correctly"""
        self.assertEqual(self.generated.title, 'Generated Test Report')
        self.assertEqual(self.generated.format, 'pdf')
        self.assertEqual(self.generated.status, 'completed')
    
    def test_generated_report_relationships(self):
        """Test generated report relationships"""
        self.assertEqual(self.generated.template, self.template)
        self.assertEqual(self.generated.generated_by, self.user)


class ReportTemplateViewTest(TestCase):
    """Test ReportTemplate views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpass123',
            is_staff=True
        )
        
        self.template = ReportTemplate.objects.create(
            name='Test Report',
            code='test-report',
            category='academic',
            created_by=self.staff_user,
            is_public=True,
            is_active=True
        )
    
    def test_template_list_view(self):
        """Test template list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:template_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_detail_view(self):
        """Test template detail view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:template_detail', args=[self.template.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Report')
    
    def test_template_create_requires_staff(self):
        """Test template creation requires staff permission"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:template_create'))
        self.assertEqual(response.status_code, 302)  # Redirect


class ReportFavoriteTest(TestCase):
    """Test ReportFavorite functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.template = ReportTemplate.objects.create(
            name='Test Report',
            code='test-report',
            category='academic',
            is_public=True,
            is_active=True
        )
    
    def test_create_favorite(self):
        """Test creating a favorite"""
        favorite = ReportFavorite.objects.create(
            user=self.user,
            template=self.template
        )
        
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.template, self.template)
    
    def test_unique_favorite(self):
        """Test that favorites are unique per user-template combination"""
        ReportFavorite.objects.create(
            user=self.user,
            template=self.template
        )
        
        # Attempting to create duplicate should raise error
        with self.assertRaises(Exception):
            ReportFavorite.objects.create(
                user=self.user,
                template=self.template
            )


class ReportManagerTest(TestCase):
    """Test custom managers"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.active_template = ReportTemplate.objects.create(
            name='Active Report',
            code='active-report',
            category='academic',
            is_active=True
        )
        
        self.inactive_template = ReportTemplate.objects.create(
            name='Inactive Report',
            code='inactive-report',
            category='academic',
            is_active=False
        )
    
    def test_active_manager(self):
        """Test active manager method"""
        active_templates = ReportTemplate.objects.active()
        self.assertEqual(active_templates.count(), 1)
        self.assertIn(self.active_template, active_templates)
        self.assertNotIn(self.inactive_template, active_templates)
