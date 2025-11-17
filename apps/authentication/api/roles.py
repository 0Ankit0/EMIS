"""Role management API endpoints"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.services.role_service import RoleService
from apps.authentication.services.user_service import UserService
from apps.authentication.serializers.role import (
    RoleResponseSerializer,
    PermissionSerializer,
    ResourceGroupSerializer
)
from apps.core.middleware.rbac import require_permission


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('roles', 'view')
def list_roles(request):
    """Get all roles"""
    is_active = request.GET.get('is_active')
    if is_active is not None:
        is_active = is_active.lower() == 'true'
    
    roles = RoleService.get_all_roles(is_active=is_active)
    serializer = RoleResponseSerializer(roles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('roles', 'create')
def create_role(request):
    """Create a new role"""
    name = request.data.get('name')
    description = request.data.get('description', '')
    
    if not name:
        return Response(
            {'error': 'Role name is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    role = RoleService.create_role(
        name=name,
        description=description,
        actor=request.user
    )
    
    serializer = RoleResponseSerializer(role)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('roles', 'view')
def get_role(request, role_id):
    """Get role by ID"""
    role = RoleService.get_role_by_id(role_id)
    serializer = RoleResponseSerializer(role)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('roles', 'update')
def assign_permissions(request, role_id):
    """Assign permissions to a role"""
    permission_ids = request.data.get('permission_ids', [])
    
    if not permission_ids:
        return Response(
            {'error': 'At least one permission ID required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    role = RoleService.assign_permissions_to_role(
        role_id=role_id,
        permission_ids=permission_ids,
        actor=request.user
    )
    
    serializer = RoleResponseSerializer(role)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('users', 'update')
def assign_role_to_user(request, user_id):
    """Assign a role to a user"""
    role_id = request.data.get('role_id')
    
    if not role_id:
        return Response(
            {'error': 'Role ID is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = UserService.get_user_by_id(user_id)
    RoleService.assign_role_to_user(user, role_id, actor=request.user)
    
    return Response({'message': 'Role successfully assigned to user'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@require_permission('users', 'update')
def remove_role_from_user(request, user_id, role_id):
    """Remove a role from a user"""
    user = UserService.get_user_by_id(user_id)
    RoleService.remove_role_from_user(user, role_id, actor=request.user)
    
    return Response({'message': 'Role successfully removed from user'})
