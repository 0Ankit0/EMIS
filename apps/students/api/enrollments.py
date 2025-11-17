"""Enrollment API views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Enrollment
from ..serializers import (
    EnrollmentCreateSerializer,
    EnrollmentUpdateSerializer,
    EnrollmentResponseSerializer
)
from ..services import EnrollmentService
from apps.admissions.models import Application
from apps.core.permissions import IsAdminOrReadOnly


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'program', 'batch', 'section', 'status']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']
    
    def get_queryset(self):
        return Enrollment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EnrollmentUpdateSerializer
        return EnrollmentResponseSerializer
    
    @action(detail=False, methods=['post'], url_path='from-application')
    def create_from_application(self, request):
        """Create enrollment from an accepted application"""
        application_id = request.data.get('application_id')
        
        if not application_id:
            return Response(
                {'error': 'application_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            application = Application.objects.get(id=application_id)
            enrollment = EnrollmentService.create_enrollment_from_application(application)
            
            serializer = EnrollmentResponseSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Application.DoesNotExist:
            return Response(
                {'error': 'Application not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """Update enrollment status"""
        enrollment = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_enrollment = EnrollmentService.update_enrollment_status(
                enrollment, new_status
            )
            
            serializer = EnrollmentResponseSerializer(updated_enrollment)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'], url_path='assign-section')
    def assign_section(self, request, pk=None):
        """Assign section to enrollment"""
        enrollment = self.get_object()
        section = request.data.get('section')
        
        if not section:
            return Response(
                {'error': 'section is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_enrollment = EnrollmentService.assign_section(enrollment, section)
        
        serializer = EnrollmentResponseSerializer(updated_enrollment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='bulk-enroll')
    def bulk_enroll(self, request):
        """Bulk enroll students from applications"""
        application_ids = request.data.get('application_ids', [])
        
        if not application_ids:
            return Response(
                {'error': 'application_ids are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = EnrollmentService.bulk_enroll(application_ids)
        return Response(results)
