"""Analytics API Views"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import SEOAnalytics
from ..serializers import SEOAnalyticsSerializer


class SEOAnalyticsViewSet(viewsets.ModelViewSet):
    """ViewSet for SEO Analytics"""
    queryset = SEOAnalytics.objects.all()
    serializer_class = SEOAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['platform', 'is_active']
    search_fields = ['name', 'tracking_id']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active analytics"""
        analytics = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(analytics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_placement(self, request):
        """Get analytics grouped by placement"""
        placement = request.query_params.get('placement', 'head')
        
        if placement == 'head':
            analytics = self.queryset.filter(is_active=True, in_head=True)
        elif placement == 'body_start':
            analytics = self.queryset.filter(is_active=True, in_body_start=True)
        elif placement == 'body_end':
            analytics = self.queryset.filter(is_active=True, in_body_end=True)
        else:
            analytics = self.queryset.filter(is_active=True)
        
        serializer = self.get_serializer(analytics, many=True)
        return Response(serializer.data)
