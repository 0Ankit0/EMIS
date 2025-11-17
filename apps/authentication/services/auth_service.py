"""Authentication service for user management"""
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from apps.authentication.jwt import generate_tokens_for_user
from apps.authentication.models import AuditLog
from apps.core.exceptions import AuthenticationException

User = get_user_model()

class AuthService:
    @staticmethod
    def register_user(username, email, password, **kwargs):
        if User.objects.filter(username=username).exists():
            raise AuthenticationException("Username already exists", code='AUTH_014')
        if User.objects.filter(email=email).exists():
            raise AuthenticationException("Email already exists", code='AUTH_013')
        return User.objects.create_user(username=username, email=email, password=password, **kwargs)
    
    @staticmethod
    def login(username, password, ip_address=None, user_agent=None):
        user = authenticate(username=username, password=password)
        if not user:
            AuditLog.objects.create(
                action='failed_login', outcome='failure',
                details={'username': username}, ip_address=ip_address, user_agent=user_agent or ''
            )
            raise AuthenticationException("Invalid credentials", code='AUTH_001')
        if not user.is_active:
            raise AuthenticationException("Account is inactive", code='AUTH_006')
        
        user.last_login = timezone.now()
        user.last_login_ip = ip_address
        user.save(update_fields=['last_login', 'last_login_ip'])
        
        tokens = generate_tokens_for_user(user)
        
        AuditLog.objects.create(
            actor=user, action='login', outcome='success',
            ip_address=ip_address, user_agent=user_agent or ''
        )
        return {'user': user, 'tokens': tokens}
    
    @staticmethod
    def logout(user, ip_address=None, user_agent=None):
        AuditLog.objects.create(
            actor=user, action='logout', outcome='success',
            ip_address=ip_address, user_agent=user_agent or ''
        )
        return True
