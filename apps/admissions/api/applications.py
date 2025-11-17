"""Application API views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from ..models import Application
from ..serializers import (
    ApplicationCreateSerializer,
    ApplicationUpdateSerializer,
    ApplicationResponseSerializer,
    ApplicationStatusUpdateSerializer
)
from ..services import ApplicationService
from apps.core.permissions import IsAdminOrReadOnly


class ApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for Application CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'program', 'admission_year', 'admission_semester']
    search_fields = ['first_name', 'last_name', 'email', 'application_number']
    ordering_fields = ['submitted_at', 'merit_score', 'rank', 'created_at']
    ordering = ['-submitted_at']
    
    def get_queryset(self):
        return Application.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ApplicationUpdateSerializer
        return ApplicationResponseSerializer
    
    def create(self, request, *args, **kwargs):
        """Create and submit new application"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Use service to create application
        application = ApplicationService.submit_application(serializer.validated_data)
        
        response_serializer = ApplicationResponseSerializer(application)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """Update application status"""
        application = self.get_object()
        serializer = ApplicationStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            updated_application = ApplicationService.update_status(
                application=application,
                new_status=serializer.validated_data['status'],
                reviewer=request.user,
                review_notes=serializer.validated_data.get('review_notes'),
                merit_score=serializer.validated_data.get('merit_score'),
                rank=serializer.validated_data.get('rank')
            )
            
            response_serializer = ApplicationResponseSerializer(updated_application)
            return Response(response_serializer.data)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'], url_path='validate')
    def validate_application(self, request, pk=None):
        """Validate application data"""
        application = self.get_object()
        errors = ApplicationService.validate_application(application)
        
        if errors:
            return Response(
                {'valid': False, 'errors': errors},
                status=status.HTTP_200_OK
            )
        
        return Response({'valid': True, 'errors': {}})
    
    @action(detail=False, methods=['post'], url_path='bulk-update-status')
    def bulk_update_status(self, request):
        """Bulk update application statuses"""
        application_ids = request.data.get('application_ids', [])
        new_status = request.data.get('status')
        
        if not application_ids or not new_status:
            return Response(
                {'error': 'application_ids and status are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_count = ApplicationService.bulk_update_status(
            application_ids, new_status, request.user
        )
        
        return Response({
            'updated_count': updated_count,
            'total_requested': len(application_ids)
        })
