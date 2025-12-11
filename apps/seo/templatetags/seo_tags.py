"""SEO Template Tags"""
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import SEOMetadata, SEOAnalytics

register = template.Library()


@register.inclusion_tag('seo/meta_tags.html')
def render_seo_meta(obj):
    """Render SEO meta tags for an object"""
    try:
        content_type = ContentType.objects.get_for_model(obj)
        seo = SEOMetadata.objects.get(content_type=content_type, object_id=obj.pk)
    except SEOMetadata.DoesNotExist:
        seo = None
    
    return {'seo': seo, 'obj': obj}


@register.inclusion_tag('seo/analytics.html')
def render_analytics(placement='head'):
    """Render analytics scripts"""
    if placement == 'head':
        scripts = SEOAnalytics.objects.filter(is_active=True, in_head=True)
    elif placement == 'body_start':
        scripts = SEOAnalytics.objects.filter(is_active=True, in_body_start=True)
    elif placement == 'body_end':
        scripts = SEOAnalytics.objects.filter(is_active=True, in_body_end=True)
    else:
        scripts = []
    
    return {'scripts': scripts}


@register.simple_tag
def get_seo_meta(obj, field='meta_title'):
    """Get specific SEO meta field for an object"""
    try:
        content_type = ContentType.objects.get_for_model(obj)
        seo = SEOMetadata.objects.get(content_type=content_type, object_id=obj.pk)
        return getattr(seo, field, '')
    except SEOMetadata.DoesNotExist:
        return ''
