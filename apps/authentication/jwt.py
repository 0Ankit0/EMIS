"""
JWT token generation and validation for authentication
Uses djangorestframework-simplejwt
"""
from datetime import timedelta
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for a user
    
    Args:
        user: User instance
    
    Returns:
        Dict with 'access' and 'refresh' tokens
    """
    refresh = RefreshToken.for_user(user)
    
    # Add custom claims
    refresh['email'] = user.email
    refresh['username'] = user.username
    refresh['user_id'] = str(user.id)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'access_expires_in': int(settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=60)).total_seconds()),
        'refresh_expires_in': int(settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME', timedelta(days=7)).total_seconds()),
    }


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        InvalidToken: If token is invalid or expired
    """
    try:
        access_token = AccessToken(token)
        return dict(access_token.payload)
    except TokenError as e:
        raise InvalidToken(str(e))


def refresh_access_token(refresh_token: str) -> dict:
    """
    Generate a new access token from a refresh token
    
    Args:
        refresh_token: Refresh token string
    
    Returns:
        Dict with new 'access' token
    
    Raises:
        InvalidToken: If refresh token is invalid or expired
    """
    try:
        refresh = RefreshToken(refresh_token)
        return {
            'access': str(refresh.access_token),
            'access_expires_in': int(settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=60)).total_seconds()),
        }
    except TokenError as e:
        raise InvalidToken(str(e))


def blacklist_token(token: str):
    """
    Blacklist a token (requires djangorestframework-simplejwt.token_blacklist)
    
    Args:
        token: Token to blacklist
    """
    try:
        refresh = RefreshToken(token)
        refresh.blacklist()
    except Exception:
        pass  # Token already invalid or blacklisted


def get_user_from_token(token: str):
    """
    Get user instance from a JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        User instance
    
    Raises:
        InvalidToken: If token is invalid
        User.DoesNotExist: If user not found
    """
    payload = verify_token(token)
    user_id = payload.get('user_id')
    
    if not user_id:
        raise InvalidToken("Token does not contain user_id")
    
    return User.objects.get(id=user_id)
