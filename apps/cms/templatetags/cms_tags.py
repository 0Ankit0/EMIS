"""
CMS Template Tags
"""
from django import template
from django.utils.safestring import mark_safe
from apps.cms.models import Post, Widget
from apps.cms.utils import get_reading_time, truncate_html

register = template.Library()


@register.simple_tag
def get_recent_posts(count=5, post_type='post'):
    """Get recent posts"""
    return Post.objects.filter(
        status='published',
        post_type=post_type
    ).order_by('-published_at')[:count]


@register.simple_tag
def get_popular_posts(count=5, post_type='post'):
    """Get popular posts"""
    return Post.objects.filter(
        status='published',
        post_type='post_type'
    ).order_by('-view_count')[:count]


@register.simple_tag
def get_featured_posts(count=6):
    """Get featured posts"""
    return Post.objects.filter(
        status='published',
        is_featured=True
    ).order_by('-published_at')[:count]


@register.simple_tag
def get_widget(position):
    """Get widgets for position"""
    return Widget.objects.filter(
        position=position,
        is_active=True
    ).order_by('order')


@register.filter
def reading_time(content):
    """Calculate reading time"""
    return get_reading_time(content)


@register.filter
def truncate_content(content, length=200):
    """Truncate HTML content"""
    return mark_safe(truncate_html(content, length))


@register.filter
def excerpt(content, length=200):
    """Generate excerpt"""
    from apps.cms.utils import generate_excerpt
    return generate_excerpt(content, length)
