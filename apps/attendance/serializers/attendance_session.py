"""Attendance Session Serializer"""
from rest_framework import serializers
from ..models import AttendanceSession


class AttendanceSessionSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_students = serializers.SerializerMethodField()
    present_count = serializers.SerializerMethodField()
    absent_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AttendanceSession
        fields = [
            'id', 'name', 'course', 'course_name', 'date', 'start_time',
            'end_time', 'is_active', 'total_students', 'present_count',
            'absent_count', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def get_total_students(self, obj):
        return obj.attendance_records.count()
    
    def get_present_count(self, obj):
        return obj.attendance_records.filter(status='present').count()
    
    def get_absent_count(self, obj):
        return obj.attendance_records.filter(status='absent').count()


class AttendanceSessionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = AttendanceSession
        fields = ['id', 'name', 'course_name', 'date', 'is_active', 'created_at']
