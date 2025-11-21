"""
Custom admin site configuration
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class EMISAdminSite(AdminSite):
    """
    Custom admin site for EMIS
    """
    site_header = _('EMIS Administration')
    site_title = _('EMIS Admin Portal')
    index_title = _('Welcome to EMIS Administration')
    site_url = '/dashboard/'
    enable_nav_sidebar = True
    
    def each_context(self, request):
        """
        Add custom context to all admin pages
        """
        context = super().each_context(request)
        context.update({
            'app_name': 'EMIS',
            'app_version': '1.0.0',
        })
        return context


# Create custom admin site instance
admin_site = EMISAdminSite(name='emis_admin')


# Custom admin styling
class BaseModelAdmin(admin.ModelAdmin):
    """
    Base admin class with common configurations
    """
    list_per_page = 25
    show_full_result_count = True
    
    def get_list_display(self, request):
        """Add created_at to list display if available"""
        list_display = super().get_list_display(request)
        if hasattr(self.model, 'created_at') and 'created_at' not in list_display:
            list_display = list(list_display) + ['created_at']
        return list_display
    
    def get_list_filter(self, request):
        """Add created_at to list filter if available"""
        list_filter = super().get_list_filter(request)
        if hasattr(self.model, 'created_at') and 'created_at' not in list_filter:
            list_filter = list(list_filter) + ['created_at']
        return list_filter

# Register your models here
