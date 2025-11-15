"""
Django test configuration
"""
import pytest
from django.conf import settings
from django.test import RequestFactory
from rest_framework.test import APIClient
from apps.authentication.models import User


@pytest.fixture
def api_client():
    """DRF API test client"""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticated API client"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )


@pytest.fixture
def request_factory():
    """Django request factory"""
    return RequestFactory()


@pytest.fixture
def sample_data(db):
    """Create sample test data"""
    # Add sample data creation here
    pass


# Configure pytest-django
def pytest_configure(config):
    """Configure Django settings for tests"""
    settings.DEBUG = False
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
