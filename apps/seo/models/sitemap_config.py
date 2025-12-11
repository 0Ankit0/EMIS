"""Sitemap Configuration Model"""
from django.db import models
from apps.core.models import TimeStampedModel


class SitemapConfig(TimeStampedModel):
    """Sitemap Configuration"""
    
    app_label = models.CharField(max_length=100, unique=True)
    model_name = models.CharField(max_length=100)
    
    is_enabled = models.BooleanField(default=True)
    priority = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    changefreq = models.CharField(
        max_length=20, default='weekly',
        choices=[
            ('always', 'Always'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('never', 'Never'),
        ]
    )
    
    # Field names
    url_field = models.CharField(max_length=100, default='get_absolute_url', help_text='Method/field for URL')
    lastmod_field = models.CharField(max_length=100, default='updated_at', help_text='Field for last modified')
    
    class Meta:
        db_table = 'seo_sitemap_config'
        unique_together = ['app_label', 'model_name']
        verbose_name = 'Sitemap Configuration'
        verbose_name_plural = 'Sitemap Configurations'
    
    def __str__(self):
        return f"{self.app_label}.{self.model_name}"
