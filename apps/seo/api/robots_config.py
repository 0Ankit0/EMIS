"""Robots Config API Views"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import RobotsConfig
from ..serializers import RobotsConfigSerializer


class RobotsConfigViewSet(viewsets.ModelViewSet):
    """ViewSet for Robots.txt Configuration"""
    queryset = RobotsConfig.objects.all()
    serializer_class = RobotsConfigSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user_agent']
    ordering = ['order', 'user_agent']
    
    @action(detail=False, methods=['get'])
    def generate_robots_txt(self, request):
        """Generate robots.txt content"""
        configs = self.queryset.filter(is_active=True).order_by('order', 'user_agent')
        
        lines = []
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
            
            lines.append("")  # Empty line between user agents
        
        # Add sitemap URL
        sitemap_url = request.build_absolute_uri('/sitemap.xml')
        lines.append(f"Sitemap: {sitemap_url}")
        
        return Response({
            'robots_txt': '\n'.join(lines)
        })
