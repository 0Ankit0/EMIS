"""Redirect API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Redirect
from ..serializers import RedirectSerializer
from ..permissions import CanManageSEO


class RedirectViewSet(viewsets.ModelViewSet):
    """ViewSet for URL Redirects"""
    queryset = Redirect.objects.all()
    serializer_class = RedirectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['redirect_type', 'is_active']
    search_fields = ['old_path', 'new_path']
    ordering_fields = ['created_at', 'hit_count']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanManageSEO()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def most_used(self, request):
        """Get most used redirects"""
        redirects = self.queryset.filter(is_active=True).order_by('-hit_count')[:20]
        serializer = self.get_serializer(redirects, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reset_count(self, request, pk=None):
        """Reset hit count"""
        redirect = self.get_object()
        redirect.hit_count = 0
        redirect.save(update_fields=['hit_count'])
        serializer = self.get_serializer(redirect)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def check_path(self, request):
        """Check if a path has a redirect"""
        path = request.query_params.get('path')
        if not path:
            return Response(
                {'error': 'path parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            redirect = Redirect.objects.get(old_path=path, is_active=True)
            serializer = self.get_serializer(redirect)
            return Response(serializer.data)
        except Redirect.DoesNotExist:
            return Response(
                {'has_redirect': False},
                status=status.HTTP_200_OK
            )
