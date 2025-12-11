"""SEO Views"""
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .services import SitemapService, RobotsService


@cache_page(60 * 60)  # Cache for 1 hour
def sitemap_view(request):
    """Generate and return sitemap.xml"""
    xml_content = SitemapService.generate_sitemap_xml()
    return HttpResponse(xml_content, content_type='application/xml')


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def robots_txt_view(request):
    """Generate and return robots.txt"""
    content = RobotsService.generate_robots_txt(request)
    return HttpResponse(content, content_type='text/plain')
