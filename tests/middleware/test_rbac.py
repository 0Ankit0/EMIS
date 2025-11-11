"""Unit tests for RBAC Middleware"""
import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock, patch

from src.middleware.rbac import require_permissions, check_permissions


class TestRBACMiddleware:
    """Test suite for RBAC middleware"""
    
    def test_require_permissions_decorator_success(self):
        """Test require_permissions decorator with valid permissions"""
        # Arrange
        required_perms = ["student:read", "student:write"]
        decorator = require_permissions(required_perms)
        
        # Assert decorator is callable
        assert callable(decorator)
        
    @pytest.mark.asyncio
    async def test_check_permissions_all_granted(self):
        """Test permission check when all required permissions are granted"""
        # Arrange
        user_permissions = ["student:read", "student:write", "student:delete"]
        required_permissions = ["student:read", "student:write"]
        
        # Act
        result = check_permissions(user_permissions, required_permissions)
        
        # Assert
        assert result is True
        
    @pytest.mark.asyncio
    async def test_check_permissions_missing_permission(self):
        """Test permission check when required permission is missing"""
        # Arrange
        user_permissions = ["student:read"]
        required_permissions = ["student:read", "student:write"]
        
        # Act
        result = check_permissions(user_permissions, required_permissions)
        
        # Assert
        assert result is False
        
    @pytest.mark.asyncio
    async def test_check_permissions_no_permissions(self):
        """Test permission check when user has no permissions"""
        # Arrange
        user_permissions = []
        required_permissions = ["student:read"]
        
        # Act
        result = check_permissions(user_permissions, required_permissions)
        
        # Assert
        assert result is False
        
    @pytest.mark.asyncio
    async def test_check_permissions_wildcard(self):
        """Test permission check with wildcard permission"""
        # Arrange
        user_permissions = ["*"]  # Admin wildcard
        required_permissions = ["student:read", "student:write"]
        
        # Act
        result = check_permissions(user_permissions, required_permissions)
        
        # Assert
        assert result is True
        
    @pytest.mark.asyncio
    async def test_check_permissions_partial_wildcard(self):
        """Test permission check with partial wildcard"""
        # Arrange
        user_permissions = ["student:*"]  # All student permissions
        required_permissions = ["student:read", "student:write"]
        
        # Act
        result = check_permissions(user_permissions, required_permissions)
        
        # Assert
        assert result is True
        
    @pytest.mark.asyncio
    async def test_check_permissions_case_sensitive(self):
        """Test that permission check is case-sensitive"""
        # Arrange
        user_permissions = ["Student:Read"]
        required_permissions = ["student:read"]
        
        # Act
        result = check_permissions(user_permissions, required_permissions)
        
        # Assert - should fail due to case mismatch
        assert result is False
