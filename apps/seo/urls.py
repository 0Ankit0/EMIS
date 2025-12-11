"""SEO URL Configuration"""
from django.urls import path, include
from .views import sitemap_view, robots_txt_view

app_name = 'seo'

urlpatterns = [
    # Public endpoints
    path('sitemap.xml', sitemap_view, name='sitemap'),
    path('robots.txt', robots_txt_view, name='robots'),
    
    # API endpoints
    path('api/', include('apps.seo.api.urls')),
]
