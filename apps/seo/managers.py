"""SEO Managers"""
from django.db import models


class SEOMetadataManager(models.Manager):
    """Manager for SEO Metadata"""
    
    def for_object(self, obj):
        """Get SEO metadata for a specific object"""
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.pk).first()
    
    def in_sitemap(self):
        """Get all metadata that should be in sitemap"""
        return self.filter(include_in_sitemap=True)


class RedirectManager(models.Manager):
    """Manager for Redirects"""
    
    def active(self):
        """Get only active redirects"""
        return self.filter(is_active=True)
    
    def most_used(self, limit=20):
        """Get most used redirects"""
        return self.filter(is_active=True).order_by('-hit_count')[:limit]
    
    def by_type(self, redirect_type):
        """Get redirects by type"""
        return self.filter(redirect_type=redirect_type, is_active=True)
