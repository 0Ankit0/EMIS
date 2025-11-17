"""
Authentication API views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.authentication.serializers.user import (
    UserCreateSerializer,
    UserResponseSerializer,
    UserLoginSerializer
)
from apps.authentication.services.auth_service import AuthService
from apps.core.middleware.audit import log_audit

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.save()
    
    # Log registration
    log_audit(
        action='create',
        actor=user,
        target_model='User',
        target_id=str(user.id),
        outcome='success',
        request=request
    )
    
    response_serializer = UserResponseSerializer(user)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return tokens"""
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    result = AuthService.login(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    user_serializer = UserResponseSerializer(result['user'])
    
    return Response({
        'user': user_serializer.data,
        'access': result['tokens']['access'],
        'refresh': result['tokens']['refresh'],
        'access_expires_in': result['tokens']['access_expires_in'],
        'refresh_expires_in': result['tokens']['refresh_expires_in'],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout current user"""
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    AuthService.logout(
        user=request.user,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    return Response({'message': 'Successfully logged out'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Get current user profile"""
    serializer = UserResponseSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """Refresh access token using refresh token"""
    from rest_framework_simplejwt.tokens import RefreshToken
    from rest_framework_simplejwt.exceptions import TokenError
    
    refresh_token_str = request.data.get('refresh')
    
    if not refresh_token_str:
        return Response(
            {'error': {'code': 'AUTH_004', 'message': 'Refresh token is required'}},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token_str)
        access_token = str(refresh.access_token)
        
        return Response({
            'access': access_token,
            'access_expires_in': 1800  # 30 minutes
        })
    except TokenError as e:
        return Response(
            {'error': {'code': 'AUTH_003', 'message': 'Invalid or expired refresh token'}},
            status=status.HTTP_401_UNAUTHORIZED
        )
