"""SEO API Views"""
from .seo_metadata import SEOMetadataViewSet
from .redirect import RedirectViewSet
from .sitemap_config import SitemapConfigViewSet
from .robots_config import RobotsConfigViewSet
from .analytics import SEOAnalyticsViewSet

__all__ = [
    'SEOMetadataViewSet',
    'RedirectViewSet',
    'SitemapConfigViewSet',
    'RobotsConfigViewSet',
    'SEOAnalyticsViewSet',
]
