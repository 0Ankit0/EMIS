import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .user import User

class PasswordResetToken(models.Model):
    """Secure password reset tokens"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    class Meta:
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']
    def __str__(self):
        return f"Reset token for {self.user.email}"
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    @classmethod
    def create_token(cls, user, ip_address, user_agent='', expiry_hours=1):
        import secrets
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=expiry_hours)
        return cls.objects.create(
            user=user,
            token=token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )
