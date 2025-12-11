"""Page API Views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Page
from ..serializers import PageSerializer, PageListSerializer


class PageViewSet(viewsets.ModelViewSet):
    """ViewSet for Page"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_homepage']
    search_fields = ['title', 'content']
    ordering_fields = ['published_at', 'created_at', 'title']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PageListSerializer
        return PageSerializer
    
    def get_queryset(self):
        queryset = Page.objects.all()
        
        # Public users see only published pages
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def homepage(self, request):
        """Get the homepage"""
        try:
            page = Page.objects.get(is_homepage=True, status='published')
            serializer = PageSerializer(page)
            return Response(serializer.data)
        except Page.DoesNotExist:
            return Response(
                {'error': 'Homepage not found'},
                status=status.HTTP_404_NOT_FOUND
            )
