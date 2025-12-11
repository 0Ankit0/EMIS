"""Attendance Session API Views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import AttendanceSession
from ..serializers import AttendanceSessionSerializer, AttendanceSessionListSerializer


class AttendanceSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for AttendanceSession"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'date', 'is_active']
    search_fields = ['name']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AttendanceSessionListSerializer
        return AttendanceSessionSerializer
    
    def get_queryset(self):
        return AttendanceSession.objects.select_related(
            'course', 'created_by'
        ).prefetch_related('attendance_records').all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close an attendance session"""
        session = self.get_object()
        session.is_active = False
        session.save()
        
        serializer = AttendanceSessionSerializer(session)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get attendance statistics for a session"""
        session = self.get_object()
        records = session.attendance_records.all()
        
        stats = {
            'total': records.count(),
            'present': records.filter(status='present').count(),
            'absent': records.filter(status='absent').count(),
            'late': records.filter(status='late').count(),
            'excused': records.filter(status='excused').count(),
            'attendance_percentage': 0
        }
        
        if stats['total'] > 0:
            stats['attendance_percentage'] = round(
                (stats['present'] / stats['total']) * 100, 2
            )
        
        return Response(stats)
