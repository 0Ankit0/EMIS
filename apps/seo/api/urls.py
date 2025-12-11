"""SEO API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import (
    SEOMetadataViewSet,
    RedirectViewSet,
    SitemapConfigViewSet,
    RobotsConfigViewSet,
    SEOAnalyticsViewSet
)

router = DefaultRouter()
router.register(r'metadata', SEOMetadataViewSet, basename='seo-metadata')
router.register(r'redirects', RedirectViewSet, basename='redirect')
router.register(r'sitemap-config', SitemapConfigViewSet, basename='sitemap-config')
router.register(r'robots-config', RobotsConfigViewSet, basename='robots-config')
router.register(r'analytics', SEOAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]
