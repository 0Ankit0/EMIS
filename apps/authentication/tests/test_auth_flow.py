"""Integration tests for authentication flow"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestAuthenticationFlow:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = '/api/v1/auth/register/'
        self.login_url = '/api/v1/auth/login/'
        self.logout_url = '/api/v1/auth/logout/'
        self.me_url = '/api/v1/auth/me/'
    
    def test_user_registration_success(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='testuser').exists()
    
    def test_user_login_success(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        data = {'username': 'testuser', 'password': 'SecurePass123!'}
        response = self.client.post(self.login_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
