import uuid
from django.db import models
from .user import User

class APIKey(models.Model):
    """API keys for programmatic access"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, db_index=True)
    scopes = models.JSONField(default=list, help_text="List of allowed scopes")
    rate_limit = models.IntegerField(default=1000, help_text="Requests per hour")
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    allowed_ips = models.JSONField(default=list, help_text="Whitelist of allowed IP addresses")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'api_keys'
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.user.email} - {self.name}"
    @classmethod
    def generate_key(cls):
        import secrets
        return secrets.token_urlsafe(48)
    def is_valid(self):
        from django.utils import timezone
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True
