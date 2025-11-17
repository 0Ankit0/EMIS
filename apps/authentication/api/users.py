"""User management API endpoints"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.services.user_service import UserService
from apps.authentication.serializers.user import UserResponseSerializer, UserUpdateSerializer
from apps.core.middleware.rbac import require_permission


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('users', 'view')
def list_users(request):
    """Get paginated list of users"""
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    search = request.GET.get('search')
    is_active = request.GET.get('is_active')
    
    if is_active is not None:
        is_active = is_active.lower() == 'true'
    
    result = UserService.get_users(
        page=page,
        page_size=page_size,
        search=search,
        is_active=is_active
    )
    
    serializer = UserResponseSerializer(result['users'], many=True)
    
    return Response({
        'results': serializer.data,
        'page_info': {
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'total_pages': result['total_pages']
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('users', 'view')
def get_user(request, user_id):
    """Get user by ID"""
    user = UserService.get_user_by_id(user_id)
    serializer = UserResponseSerializer(user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@require_permission('users', 'update')
def update_user(request, user_id):
    """Update user information"""
    user = UserService.get_user_by_id(user_id)
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    
    updated_user = UserService.update_user(
        user_id=user_id,
        data=serializer.validated_data,
        actor=request.user
    )
    
    response_serializer = UserResponseSerializer(updated_user)
    return Response(response_serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@require_permission('users', 'delete')
def delete_user(request, user_id):
    """Soft delete a user"""
    UserService.delete_user(user_id, actor=request.user)
    return Response({'message': 'User successfully deleted'}, status=status.HTTP_200_OK)
