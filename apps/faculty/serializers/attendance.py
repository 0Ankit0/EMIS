"""Faculty Attendance Serializer"""
from rest_framework import serializers
from ..models import FacultyAttendance


class FacultyAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for FacultyAttendance"""
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)
    
    class Meta:
        model = FacultyAttendance
        fields = ['id', 'faculty', 'faculty_name', 'date', 'status',
                  'check_in_time', 'check_out_time', 'working_hours', 'remarks',
                  'marked_by', 'marked_by_name', 'created_at']
        read_only_fields = ['id', 'created_at', 'marked_by']
