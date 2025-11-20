"""
Analytics Custom Managers and QuerySets
"""
from django.db import models


class AnalyticsItemQuerySet(models.QuerySet):
    """Custom queryset for AnalyticsItem"""
    
    def active(self):
        """Get only active items"""
        return self.filter(status='active')
    
    def inactive(self):
        """Get only inactive items"""
        return self.filter(status='inactive')
    
    def pending(self):
        """Get only pending items"""
        return self.filter(status='pending')
    
    def created_by_user(self, user):
        """Get items created by specific user"""
        return self.filter(created_by=user)


class AnalyticsItemManager(models.Manager):
    """Custom manager for AnalyticsItem"""
    
    def get_queryset(self):
        return AnalyticsItemQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def inactive(self):
        return self.get_queryset().inactive()
    
    def pending(self):
        return self.get_queryset().pending()
    
    def created_by_user(self, user):
        return self.get_queryset().created_by_user(user)
