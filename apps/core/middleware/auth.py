"""
JWT Authentication middleware for EMIS
Validates JWT tokens and attaches user to request
"""
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.exceptions import InvalidToken
from apps.authentication.jwt import verify_token

User = get_user_model()


def get_user_from_request(request):
    """
    Extract and validate JWT token from request, return user
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = verify_token(token)
        user_id = payload.get('user_id')
        
        if user_id:
            return User.objects.get(id=user_id)
    except (InvalidToken, User.DoesNotExist):
        pass
    
    return None


class JWTAuthenticationMiddleware:
    """
    Middleware to authenticate requests using JWT tokens
    Attaches user to request.user if valid token provided
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Use SimpleLazyObject to defer user lookup
        request.user = SimpleLazyObject(lambda: get_user_from_request(request))
        
        response = self.get_response(request)
        return response
