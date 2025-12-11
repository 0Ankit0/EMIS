"""Robots.txt Configuration Model"""
from django.db import models
from apps.core.models import TimeStampedModel


class RobotsConfig(TimeStampedModel):
    """Robots.txt Configuration"""
    
    user_agent = models.CharField(max_length=100, default='*', help_text='User-agent (e.g., *, Googlebot)')
    
    # Rules
    disallow = models.TextField(blank=True, help_text='Paths to disallow (one per line)')
    allow = models.TextField(blank=True, help_text='Paths to allow (one per line)')
    
    crawl_delay = models.PositiveIntegerField(null=True, blank=True, help_text='Crawl delay in seconds')
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    
    class Meta:
        db_table = 'seo_robots_config'
        ordering = ['order', 'user_agent']
        verbose_name = 'Robots.txt Configuration'
        verbose_name_plural = 'Robots.txt Configurations'
    
    def __str__(self):
        return f"Robots for {self.user_agent}"
