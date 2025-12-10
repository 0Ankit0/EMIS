"""
Reports API Views
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import (
    ReportTemplate, GeneratedReport, ScheduledReport,
    ReportWidget, ReportFavorite, ReportAccessLog
)
from .serializers import (
    ReportTemplateSerializer, ReportTemplateListSerializer,
    GeneratedReportSerializer, GeneratedReportListSerializer,
    ScheduledReportSerializer, ReportWidgetSerializer,
    ReportFavoriteSerializer, ReportAccessLogSerializer
)
from .filters import ReportTemplateFilter, GeneratedReportFilter, ScheduledReportFilter
from .permissions import ReportPermission


class ReportTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for ReportTemplate"""
    queryset = ReportTemplate.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReportTemplateFilter
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['category', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReportTemplateListSerializer
        return ReportTemplateSerializer
    
    def get_queryset(self):
        return ReportTemplate.objects.for_user(self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """Generate report from this template"""
        template = self.get_object()
        
        title = request.data.get('title', template.name)
        parameters = request.data.get('parameters', {})
        output_format = request.data.get('format', template.default_format)
        
        # Create generated report record
        generated_report = GeneratedReport.objects.create(
            template=template,
            title=title,
            generated_by=request.user,
            parameters=parameters,
            format=output_format,
            status='pending'
        )
        
        # Trigger async generation here (e.g., Celery task)
        # For now, return the created record
        
        serializer = GeneratedReportSerializer(generated_report)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get templates grouped by category"""
        templates = self.get_queryset()
        categories = {}
        
        for template in templates:
            cat = template.get_category_display()
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ReportTemplateListSerializer(template).data)
        
        return Response(categories)


class GeneratedReportViewSet(viewsets.ModelViewSet):
    """ViewSet for GeneratedReport"""
    queryset = GeneratedReport.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GeneratedReportFilter
    search_fields = ['title', 'description']
    ordering_fields = ['generated_at', 'title', 'status']
    ordering = ['-generated_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GeneratedReportListSerializer
        return GeneratedReportSerializer
    
    def get_queryset(self):
        return GeneratedReport.objects.for_user(self.request.user)
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Record download and return file URL"""
        report = self.get_object()
        
        # Update download stats
        report.download_count += 1
        report.last_downloaded_at = timezone.now()
        report.save(update_fields=['download_count', 'last_downloaded_at'])
        
        return Response({
            'file_url': request.build_absolute_uri(report.file.url) if report.file else None,
            'download_count': report.download_count
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get report generation statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'completed': queryset.filter(status='completed').count(),
            'pending': queryset.filter(status='pending').count(),
            'failed': queryset.filter(status='failed').count(),
            'today': queryset.filter(generated_at__date=timezone.now().date()).count(),
        }
        
        return Response(stats)


class ScheduledReportViewSet(viewsets.ModelViewSet):
    """ViewSet for ScheduledReport"""
    queryset = ScheduledReport.objects.all()
    serializer_class = ScheduledReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ScheduledReportFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'next_run']
    ordering = ['next_run']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ScheduledReport.objects.all()
        return ScheduledReport.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle scheduled report active status"""
        scheduled = self.get_object()
        scheduled.is_active = not scheduled.is_active
        scheduled.save(update_fields=['is_active'])
        
        return Response({
            'is_active': scheduled.is_active,
            'message': 'Activated' if scheduled.is_active else 'Deactivated'
        })


class ReportWidgetViewSet(viewsets.ModelViewSet):
    """ViewSet for ReportWidget"""
    queryset = ReportWidget.objects.filter(is_active=True)
    serializer_class = ReportWidgetSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['order', 'name']
    
    def get_queryset(self):
        """Filter widgets by user roles"""
        queryset = super().get_queryset()
        
        # Get user roles
        user_roles = []
        if hasattr(self.request.user, 'student'):
            user_roles.append('student')
        if hasattr(self.request.user, 'faculty'):
            user_roles.append('faculty')
        if self.request.user.is_staff:
            user_roles.append('admin')
        
        # Filter by roles if not empty
        if user_roles:
            queryset = queryset.filter(roles_allowed__overlap=user_roles)
        
        return queryset


class ReportFavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet for ReportFavorite"""
    queryset = ReportFavorite.objects.all()
    serializer_class = ReportFavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ReportFavorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle favorite status for a template"""
        template_id = request.data.get('template_id')
        
        if not template_id:
            return Response({'error': 'template_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite, created = ReportFavorite.objects.get_or_create(
            user=request.user,
            template_id=template_id
        )
        
        if not created:
            favorite.delete()
            return Response({'status': 'removed', 'is_favorite': False})
        
        return Response({'status': 'added', 'is_favorite': True}, status=status.HTTP_201_CREATED)


class ReportAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ReportAccessLog (read-only)"""
    queryset = ReportAccessLog.objects.all()
    serializer_class = ReportAccessLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['action', 'template', 'user']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ReportAccessLog.objects.all()
        return ReportAccessLog.objects.filter(user=self.request.user)
