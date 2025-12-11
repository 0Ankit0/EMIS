"""Attendance Policy Serializer"""
from rest_framework import serializers
from ..models import AttendancePolicy


class AttendancePolicySerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = AttendancePolicy
        fields = [
            'id', 'name', 'course', 'course_name', 'minimum_percentage',
            'grace_period_days', 'penalty_type', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
