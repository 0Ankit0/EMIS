"""Attendance Report Serializer"""
from rest_framework import serializers
from ..models import AttendanceReport


class AttendanceReportSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = AttendanceReport
        fields = [
            'id', 'student', 'student_name', 'course', 'course_name',
            'total_classes', 'attended_classes', 'attendance_percentage',
            'status', 'month', 'year', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
