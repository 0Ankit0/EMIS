"""
CMS Context Processors
"""
from .models import Menu, Widget, Category


def cms_context(request):
    """Add CMS data to all templates"""
    context = {}
    
    # Menus
    context['header_menu'] = Menu.objects.filter(
        location='header',
        is_active=True
    ).prefetch_related('items').first()
    
    context['footer_menu'] = Menu.objects.filter(
        location='footer',
        is_active=True
    ).prefetch_related('items').first()
    
    # Categories
    context['all_categories'] = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    ).prefetch_related('children')
    
    # Widgets
    context['sidebar_widgets'] = Widget.objects.filter(
        is_active=True,
        position__startswith='sidebar'
    ).order_by('order')
    
    context['footer_widgets'] = Widget.objects.filter(
        is_active=True,
        position__startswith='footer'
    ).order_by('position', 'order')
    
    return context
