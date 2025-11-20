"""
Attendance Filters
"""
import django_filters
from .models import AttendanceRecord, AttendanceSession


class AttendanceRecordFilter(django_filters.FilterSet):
    """
    Filter for AttendanceRecord
    """
    date = django_filters.DateFromToRangeFilter()
    student_name = django_filters.CharFilter(field_name='student__first_name', lookup_expr='icontains')
    
    class Meta:
        model = AttendanceRecord
        fields = ['status', 'course', 'date', 'student']


class AttendanceSessionFilter(django_filters.FilterSet):
    """
    Filter for AttendanceSession
    """
    date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = AttendanceSession
        fields = ['status', 'course', 'session_type', 'date', 'instructor']
