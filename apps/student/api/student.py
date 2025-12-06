from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from ..models.student import Student
from ..serializers.student import (
    StudentCreateSerializer,
    StudentUpdateSerializer,
    StudentResponseSerializer
)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    lookup_field = 'ukid'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return StudentUpdateSerializer
        return StudentResponseSerializer
    
    def perform_destroy(self, instance):
        """Soft delete - mark as inactive instead of deleting"""
        instance.is_active = False
        instance.deleted_at = timezone.now()
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            instance.deleted_by = self.request.user.username
        instance.save()
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active students"""
        active_students = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactive(self, request):
        """Get only inactive students"""
        inactive_students = self.queryset.filter(is_active=False)
        serializer = self.get_serializer(inactive_students, many=True)
        return Response(serializer.data)
