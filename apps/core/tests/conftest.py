"""Django test configuration"""
import pytest
from django.conf import settings
import os


# Set test database to SQLite before Django setup
os.environ.setdefault('TEST_DB_ENGINE', 'sqlite3')


@pytest.fixture(scope='session', autouse=True)
def setup_test_db(django_db_blocker):
    """Setup test database with migrations"""
    with django_db_blocker.unblock():
        from django.core.management import call_command
        # Run migrations
        call_command('migrate', verbosity=0)


@pytest.fixture
def api_client():
    """DRF API test client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user"""
    from apps.authentication.models import User
    return User.objects.create(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
