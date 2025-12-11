"""Attendance Record Serializer"""
from rest_framework import serializers
from ..models import AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    session_name = serializers.CharField(source='session.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = [
            'id', 'student', 'student_name', 'session', 'session_name',
            'status', 'remarks', 'marked_by', 'marked_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'marked_by']


class AttendanceRecordListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'student_name', 'status', 'created_at']
