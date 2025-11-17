"""Role and Permission serializers"""
from rest_framework import serializers
from apps.authentication.models import Role, Permission, ResourceGroup
from apps.core.serializers.base import BaseModelSerializer

class ResourceGroupSerializer(BaseModelSerializer):
    class Meta:
        model = ResourceGroup
        fields = ['id', 'name', 'description', 'module', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PermissionSerializer(BaseModelSerializer):
    resource_group_name = serializers.CharField(source='resource_group.name', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'resource_group', 'resource_group_name', 'action', 'description', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class RoleResponseSerializer(BaseModelSerializer):
    permission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'is_active', 'permission_count', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_permission_count(self, obj):
        return obj.role_permissions.count()
