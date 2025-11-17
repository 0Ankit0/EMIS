"""Tests for audit logging functionality"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestAuditLogging:
    def setup_method(self):
        self.client = APIClient()
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='Test123!'
        )
    
    def test_login_creates_audit_log(self):
        """Test that successful login creates audit log entry"""
        from apps.authentication.models import AuditLog
        
        # Clear existing logs
        AuditLog.objects.all().delete()
        
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'Test123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check audit log was created
        log = AuditLog.objects.filter(
            actor=self.user,
            action='login',
            outcome='success'
        ).first()
        
        assert log is not None
        assert log.ip_address is not None
    
    def test_failed_login_creates_audit_log(self):
        """Test that failed login creates audit log entry"""
        from apps.authentication.models import AuditLog
        
        AuditLog.objects.all().delete()
        
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'WrongPassword!'
        }, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Check audit log was created
        log = AuditLog.objects.filter(
            action='failed_login',
            outcome='failure'
        ).first()
        
        assert log is not None
        assert 'testuser' in str(log.details)
    
    def test_logout_creates_audit_log(self):
        """Test that logout creates audit log entry"""
        from apps.authentication.models import AuditLog
        
        # Login first
        login_response = self.client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'Test123!'
        }, format='json')
        
        token = login_response.data['access']
        
        AuditLog.objects.all().delete()
        
        # Logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/v1/auth/logout/')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check audit log
        log = AuditLog.objects.filter(
            actor=self.user,
            action='logout',
            outcome='success'
        ).first()
        
        assert log is not None
    
    def test_user_creation_creates_audit_log(self):
        """Test that user creation creates audit log entry"""
        from apps.authentication.models import AuditLog
        
        AuditLog.objects.all().delete()
        
        response = self.client.post('/api/v1/auth/register/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Check audit log
        log = AuditLog.objects.filter(
            action='create',
            target_model='User',
            outcome='success'
        ).first()
        
        assert log is not None
    
    def test_audit_log_captures_ip_address(self):
        """Test that audit logs capture IP address"""
        from apps.authentication.models import AuditLog
        
        AuditLog.objects.all().delete()
        
        # Login with specific IP
        response = self.client.post(
            '/api/v1/auth/login/',
            {
                'username': 'testuser',
                'password': 'Test123!'
            },
            format='json',
            REMOTE_ADDR='192.168.1.100'
        )
        
        assert response.status_code == status.HTTP_200_OK
        
        log = AuditLog.objects.filter(action='login').first()
        assert log.ip_address == '192.168.1.100'
    
    def test_multiple_failed_logins_tracked(self):
        """Test that multiple failed login attempts are tracked"""
        from apps.authentication.models import AuditLog
        
        AuditLog.objects.all().delete()
        
        # Attempt multiple failed logins
        for i in range(3):
            self.client.post('/api/v1/auth/login/', {
                'username': 'testuser',
                'password': f'WrongPass{i}!'
            }, format='json')
        
        # Check all attempts were logged
        failed_attempts = AuditLog.objects.filter(
            action='failed_login',
            outcome='failure'
        )
        
        assert failed_attempts.count() == 3


@pytest.mark.django_db
class TestAuditLogAPI:
    def setup_method(self):
        self.client = APIClient()
        from django.contrib.auth import get_user_model
        from apps.authentication.models import Role, Permission, ResourceGroup, RolePermission, UserRole
        
        User = get_user_model()
        
        # Create admin user with audit view permission
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='Admin123!'
        )
        
        # Create resource group and permission
        rg = ResourceGroup.objects.create(name='audit', module='auth')
        perm = Permission.objects.create(resource_group=rg, action='view')
        role = Role.objects.create(name='Auditor')
        RolePermission.objects.create(role=role, permission=perm)
        UserRole.objects.create(user=self.admin, role=role)
    
    def get_token(self):
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'admin',
            'password': 'Admin123!'
        }, format='json')
        return response.data['access']
    
    def test_can_retrieve_audit_logs(self):
        """Test that audit logs can be retrieved via API"""
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/v1/auth/audit/logs/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'page_info' in response.data
    
    def test_audit_logs_include_login_events(self):
        """Test that audit logs include login events"""
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/v1/auth/audit/logs/?action=login')
        assert response.status_code == status.HTTP_200_OK
        
        # Should have at least the login we just made
        assert len(response.data['results']) > 0
