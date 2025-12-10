import uuid
from django.db import models
from .page import Page

class Widget(models.Model):
    """Sidebar widgets"""
    WIDGET_TYPES = [
        ('html', 'HTML'),
        ('recent_posts', 'Recent Posts'),
        ('popular_posts', 'Popular Posts'),
        ('categories', 'Categories'),
        ('tags', 'Tags'),
        ('search', 'Search'),
        ('newsletter', 'Newsletter'),
        ('social', 'Social Media'),
        ('custom', 'Custom'),
    ]
    POSITIONS = [
        ('sidebar_left', 'Left Sidebar'),
        ('sidebar_right', 'Right Sidebar'),
        ('footer_1', 'Footer Column 1'),
        ('footer_2', 'Footer Column 2'),
        ('footer_3', 'Footer Column 3'),
        ('footer_4', 'Footer Column 4'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    position = models.CharField(max_length=20, choices=POSITIONS)
    content = models.TextField(blank=True)
    settings = models.JSONField(default=dict, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_on_pages = models.ManyToManyField(Page, blank=True)
    show_on_posts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cms_widgets'
        ordering = ['position', 'order']
    def __str__(self):
        return f'{self.title} ({self.position})'
