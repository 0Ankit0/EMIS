"""SEO Tests Init"""
from .test_models import *
from .test_api import *

__all__ = [
    'SEOMetadataModelTest',
    'RedirectModelTest',
    'SitemapConfigModelTest',
    'RobotsConfigModelTest',
    'SEOAnalyticsModelTest',
    'SEOServiceTest',
    'RobotsServiceTest',
    'SEOMetadataAPITest',
    'RedirectAPITest',
]
