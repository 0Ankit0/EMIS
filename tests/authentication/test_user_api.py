"""Tests for user management API"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()
        from django.contrib.auth import get_user_model
        from apps.authentication.models import Role, Permission, ResourceGroup, RolePermission, UserRole
        
        User = get_user_model()
        
        # Create admin user with permissions
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='Admin123!'
        )
        
        # Create resource group and permissions
        rg = ResourceGroup.objects.create(
            name='users',
            module='authentication',
            description='User management'
        )
        
        view_perm = Permission.objects.create(
            resource_group=rg,
            action='view'
        )
        update_perm = Permission.objects.create(
            resource_group=rg,
            action='update'
        )
        
        # Create role with permissions
        admin_role = Role.objects.create(name='Admin', description='Administrator')
        RolePermission.objects.create(role=admin_role, permission=view_perm)
        RolePermission.objects.create(role=admin_role, permission=update_perm)
        UserRole.objects.create(user=self.admin, role=admin_role)
    
    def get_auth_token(self):
        """Login and get auth token"""
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'admin',
            'password': 'Admin123!'
        }, format='json')
        return response.data['access']
    
    def test_list_users_authenticated(self):
        """Test listing users requires authentication"""
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_list_users_with_auth(self):
        """Test listing users with authentication"""
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/api/v1/auth/users/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'page_info' in response.data
    
    def test_get_user_by_id(self):
        """Test getting user by ID"""
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get(f'/api/v1/auth/users/{self.admin.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'admin'
    
    def test_update_user(self):
        """Test updating user"""
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(
            f'/api/v1/auth/users/{self.admin.id}/update/',
            {'first_name': 'Updated', 'last_name': 'Admin'},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
