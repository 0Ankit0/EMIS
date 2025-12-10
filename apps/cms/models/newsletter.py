import uuid
from django.db import models

class Newsletter(models.Model):
    """Newsletter subscriptions"""
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        UNSUBSCRIBED = 'unsubscribed', 'Unsubscribed'
        BOUNCED = 'bounced', 'Bounced'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cms_newsletter'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email

