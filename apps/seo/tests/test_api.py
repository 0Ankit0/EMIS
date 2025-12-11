"""SEO API Tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from rest_framework import status
from apps.seo.models import SEOMetadata, Redirect

User = get_user_model()


class SEOMetadataAPITest(TestCase):
    """Test SEO Metadata API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apitest',
            email='api@example.com',
            password='testpass123'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        
        self.content_type = ContentType.objects.get_for_model(User)
    
    def test_list_seo_metadata(self):
        """Test listing SEO metadata"""
        response = self.client.get('/api/v1/seo/metadata/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_seo_metadata(self):
        """Test creating SEO metadata via API"""
        data = {
            'content_type': self.content_type.pk,
            'object_id': self.user.pk,
            'meta_title': 'API Test Title',
            'meta_description': 'API Test Description',
            'robots': 'index, follow'
        }
        response = self.client.post('/api/v1/seo/metadata/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['meta_title'], 'API Test Title')


class RedirectAPITest(TestCase):
    """Test Redirect API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='redirecttest',
            email='redirect@example.com',
            password='testpass123'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
    
    def test_list_redirects(self):
        """Test listing redirects"""
        response = self.client.get('/api/v1/seo/redirects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_redirect(self):
        """Test creating redirect via API"""
        data = {
            'old_path': '/old-api-path/',
            'new_path': '/new-api-path/',
            'redirect_type': '301',
            'is_active': True
        }
        response = self.client.post('/api/v1/seo/redirects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_check_path(self):
        """Test check path endpoint"""
        Redirect.objects.create(
            old_path='/check-this/',
            new_path='/new-location/',
            redirect_type='301'
        )
        
        response = self.client.get('/api/v1/seo/redirects/check_path/?path=/check-this/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
