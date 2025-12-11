"""Redirect Model"""
from django.db import models
from apps.core.models import TimeStampedModel


class Redirect(TimeStampedModel):
    """URL Redirects for SEO"""
    
    class RedirectType(models.TextChoices):
        PERMANENT = '301', '301 - Permanent'
        TEMPORARY = '302', '302 - Temporary'
        FOUND = '307', '307 - Temporary (Method preserved)'
        PERMANENT_METHOD = '308', '308 - Permanent (Method preserved)'
    
    old_path = models.CharField(max_length=500, unique=True, db_index=True, help_text='Old URL path')
    new_path = models.CharField(max_length=500, help_text='New URL path or full URL')
    
    redirect_type = models.CharField(
        max_length=3,
        choices=RedirectType.choices,
        default=RedirectType.PERMANENT
    )
    
    is_active = models.BooleanField(default=True)
    hit_count = models.PositiveIntegerField(default=0, help_text='Number of redirects')
    
    class Meta:
        db_table = 'seo_redirects'
        ordering = ['-created_at']
        verbose_name = 'Redirect'
        verbose_name_plural = 'Redirects'
        indexes = [
            models.Index(fields=['old_path', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.old_path} → {self.new_path} ({self.redirect_type})"
    
    def increment_hits(self):
        """Increment hit counter"""
        self.hit_count += 1
        self.save(update_fields=['hit_count'])
