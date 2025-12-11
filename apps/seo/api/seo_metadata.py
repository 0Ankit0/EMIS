"""SEO Metadata API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType

from ..models import SEOMetadata
from ..serializers import SEOMetadataSerializer
from ..permissions import CanManageSEO


class SEOMetadataViewSet(viewsets.ModelViewSet):
    """ViewSet for SEO Metadata"""
    queryset = SEOMetadata.objects.all()
    serializer_class = SEOMetadataSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['content_type', 'robots', 'include_in_sitemap']
    search_fields = ['meta_title', 'meta_description', 'meta_keywords']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanManageSEO()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def for_object(self, request):
        """Get SEO metadata for a specific object"""
        app_label = request.query_params.get('app_label')
        model = request.query_params.get('model')
        object_id = request.query_params.get('object_id')
        
        if not all([app_label, model, object_id]):
            return Response(
                {'error': 'app_label, model, and object_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            seo = SEOMetadata.objects.get(content_type=content_type, object_id=object_id)
            serializer = self.get_serializer(seo)
            return Response(serializer.data)
        except ContentType.DoesNotExist:
            return Response(
                {'error': 'Content type not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except SEOMetadata.DoesNotExist:
            return Response(
                {'error': 'SEO metadata not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create SEO metadata"""
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
