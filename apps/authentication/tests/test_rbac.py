"""Tests for RBAC enforcement"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestRBACEnforcement:
    def setup_method(self):
        self.client = APIClient()
        from django.contrib.auth import get_user_model
        from apps.authentication.models import Role, Permission, ResourceGroup, RolePermission, UserRole
        
        User = get_user_model()
        
        # Create resource group and permissions
        self.rg_users = ResourceGroup.objects.create(
            name='users',
            module='authentication',
            description='User management'
        )
        
        self.view_perm = Permission.objects.create(
            resource_group=self.rg_users,
            action='view'
        )
        
        self.update_perm = Permission.objects.create(
            resource_group=self.rg_users,
            action='update'
        )
        
        # Create roles
        self.admin_role = Role.objects.create(
            name='Admin',
            description='Administrator with full permissions'
        )
        RolePermission.objects.create(role=self.admin_role, permission=self.view_perm)
        RolePermission.objects.create(role=self.admin_role, permission=self.update_perm)
        
        self.staff_role = Role.objects.create(
            name='Staff',
            description='Staff with limited permissions'
        )
        RolePermission.objects.create(role=self.staff_role, permission=self.view_perm)
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='Admin123!'
        )
        UserRole.objects.create(user=self.admin_user, role=self.admin_role)
        
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            password='Staff123!'
        )
        UserRole.objects.create(user=self.staff_user, role=self.staff_role)
        
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='Regular123!'
        )
    
    def get_token(self, username, password):
        """Get JWT token for user"""
        response = self.client.post('/api/v1/auth/login/', {
            'username': username,
            'password': password
        }, format='json')
        return response.data.get('access')
    
    def test_admin_can_view_users(self):
        """Test admin with view permission can list users"""
        token = self.get_token('admin', 'Admin123!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_admin_can_update_users(self):
        """Test admin with update permission can update users"""
        token = self.get_token('admin', 'Admin123!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(
            f'/api/v1/auth/users/{self.staff_user.id}/update/',
            {'first_name': 'Updated'},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_staff_can_view_users(self):
        """Test staff with view permission can list users"""
        token = self.get_token('staff', 'Staff123!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_staff_cannot_update_users(self):
        """Test staff without update permission cannot update users"""
        token = self.get_token('staff', 'Staff123!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(
            f'/api/v1/auth/users/{self.admin_user.id}/update/',
            {'first_name': 'Hacked'},
            format='json'
        )
        # Should be denied
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
    
    def test_regular_user_cannot_view_users(self):
        """Test regular user without permissions cannot access user list"""
        token = self.get_token('regular', 'Regular123!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_cannot_access(self):
        """Test unauthenticated user cannot access protected endpoints"""
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRolePermissionPropagation:
    def setup_method(self):
        self.client = APIClient()
        from django.contrib.auth import get_user_model
        from apps.authentication.models import Role, Permission, ResourceGroup, RolePermission, UserRole
        
        User = get_user_model()
        
        # Setup
        self.rg = ResourceGroup.objects.create(name='users', module='auth')
        self.perm = Permission.objects.create(resource_group=self.rg, action='view')
        self.role = Role.objects.create(name='TestRole')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='Test123!'
        )
        UserRole.objects.create(user=self.user, role=self.role)
    
    def get_token(self):
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'Test123!'
        }, format='json')
        return response.data.get('access')
    
    def test_permission_change_takes_effect(self):
        """Test that permission changes propagate to next request"""
        from apps.authentication.models import RolePermission
        
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Initially no permission - should fail
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Grant permission
        RolePermission.objects.create(role=self.role, permission=self.perm)
        
        # Now should succeed
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_200_OK
        
        # Revoke permission
        RolePermission.objects.filter(role=self.role, permission=self.perm).delete()
        
        # Should fail again
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
