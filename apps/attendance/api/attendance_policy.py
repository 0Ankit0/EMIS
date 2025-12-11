"""Attendance Policy API Views"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import AttendancePolicy
from ..serializers import AttendancePolicySerializer


class AttendancePolicyViewSet(viewsets.ModelViewSet):
    """ViewSet for AttendancePolicy"""
    queryset = AttendancePolicy.objects.select_related('course').all()
    serializer_class = AttendancePolicySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'is_active']
    search_fields = ['name']
