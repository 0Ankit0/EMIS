"""SEO Services"""
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from ..models import SEOMetadata, SitemapConfig
import xml.etree.ElementTree as ET
from datetime import datetime


class SEOService:
    """Service for SEO operations"""
    
    @staticmethod
    def get_or_create_metadata(obj, defaults=None):
        """Get or create SEO metadata for an object"""
        content_type = ContentType.objects.get_for_model(obj)
        seo, created = SEOMetadata.objects.get_or_create(
            content_type=content_type,
            object_id=obj.pk,
            defaults=defaults or {}
        )
        return seo, created
    
    @staticmethod
    def update_metadata(obj, **kwargs):
        """Update SEO metadata for an object"""
        content_type = ContentType.objects.get_for_model(obj)
        SEOMetadata.objects.update_or_create(
            content_type=content_type,
            object_id=obj.pk,
            defaults=kwargs
        )
    
    @staticmethod
    def delete_metadata(obj):
        """Delete SEO metadata for an object"""
        content_type = ContentType.objects.get_for_model(obj)
        SEOMetadata.objects.filter(
            content_type=content_type,
            object_id=obj.pk
        ).delete()


class SitemapService:
    """Service for sitemap generation"""
    
    @staticmethod
    def generate_sitemap_xml():
        """Generate sitemap.xml content"""
        urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
        
        configs = SitemapConfig.objects.filter(is_enabled=True)
        
        for config in configs:
            try:
                model = apps.get_model(config.app_label, config.model_name)
                objects = model.objects.all()
                
                for obj in objects:
                    if hasattr(obj, config.url_field):
                        url_method = getattr(obj, config.url_field)
                        if callable(url_method):
                            loc = url_method()
                        else:
                            loc = url_method
                    else:
                        continue
                    
                    url_element = ET.SubElement(urlset, 'url')
                    ET.SubElement(url_element, 'loc').text = loc
                    
                    if hasattr(obj, config.lastmod_field):
                        lastmod = getattr(obj, config.lastmod_field)
                        if isinstance(lastmod, datetime):
                            ET.SubElement(url_element, 'lastmod').text = lastmod.strftime('%Y-%m-%d')
                    
                    ET.SubElement(url_element, 'changefreq').text = config.changefreq
                    ET.SubElement(url_element, 'priority').text = str(config.priority)
            
            except Exception as e:
                print(f"Error generating sitemap for {config.app_label}.{config.model_name}: {e}")
                continue
        
        return ET.tostring(urlset, encoding='unicode')
    
    @staticmethod
    def get_sitemap_urls():
        """Get list of URLs for sitemap"""
        urls = []
        configs = SitemapConfig.objects.filter(is_enabled=True)
        
        for config in configs:
            try:
                model = apps.get_model(config.app_label, config.model_name)
                objects = model.objects.all()
                
                for obj in objects:
                    if hasattr(obj, config.url_field):
                        url_method = getattr(obj, config.url_field)
                        if callable(url_method):
                            url = url_method()
                        else:
                            url = url_method
                        
                        lastmod = None
                        if hasattr(obj, config.lastmod_field):
                            lastmod = getattr(obj, config.lastmod_field)
                        
                        urls.append({
                            'loc': url,
                            'lastmod': lastmod,
                            'changefreq': config.changefreq,
                            'priority': float(config.priority)
                        })
            except Exception:
                continue
        
        return urls


class RobotsService:
    """Service for robots.txt generation"""
    
    @staticmethod
    def generate_robots_txt(request=None):
        """Generate robots.txt content"""
        from ..models import RobotsConfig
        
        lines = []
        configs = RobotsConfig.objects.filter(is_active=True).order_by('order', 'user_agent')
        
        for config in configs:
            lines.append(f"User-agent: {config.user_agent}")
            
            if config.disallow:
                for path in config.disallow.split('\n'):
                    path = path.strip()
                    if path:
                        lines.append(f"Disallow: {path}")
            
            if config.allow:
                for path in config.allow.split('\n'):
                    path = path.strip()
                    if path:
                        lines.append(f"Allow: {path}")
            
            if config.crawl_delay:
                lines.append(f"Crawl-delay: {config.crawl_delay}")
            
            lines.append("")
        
        if request:
            sitemap_url = request.build_absolute_uri('/sitemap.xml')
            lines.append(f"Sitemap: {sitemap_url}")
        
        return '\n'.join(lines)
