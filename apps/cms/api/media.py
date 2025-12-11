"""Media API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Media
from ..serializers import MediaSerializer


class MediaViewSet(viewsets.ModelViewSet):
    """ViewSet for Media"""
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_type']
    search_fields = ['title', 'alt_text']
    ordering_fields = ['created_at', 'file_size']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def images(self, request):
        """Get only images"""
        media = self.queryset.filter(file_type='image')
        serializer = self.get_serializer(media, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def documents(self, request):
        """Get only documents"""
        media = self.queryset.filter(file_type='document')
        serializer = self.get_serializer(media, many=True)
        return Response(serializer.data)
