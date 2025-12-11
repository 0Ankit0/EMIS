"""Sitemap Config API Views"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import SitemapConfig
from ..serializers import SitemapConfigSerializer


class SitemapConfigViewSet(viewsets.ModelViewSet):
    """ViewSet for Sitemap Configuration"""
    queryset = SitemapConfig.objects.all()
    serializer_class = SitemapConfigSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_enabled', 'changefreq']
    search_fields = ['app_label', 'model_name']
    
    @action(detail=False, methods=['get'])
    def enabled(self, request):
        """Get only enabled sitemap configs"""
        configs = self.queryset.filter(is_enabled=True)
        serializer = self.get_serializer(configs, many=True)
        return Response(serializer.data)
