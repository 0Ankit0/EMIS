"""Faculty Leave Serializer"""
from rest_framework import serializers
from ..models import FacultyLeave


class FacultyLeaveSerializer(serializers.ModelSerializer):
    """Serializer for FacultyLeave"""
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = FacultyLeave
        fields = ['id', 'faculty', 'faculty_name', 'leave_type', 'start_date',
                  'end_date', 'number_of_days', 'reason', 'status',
                  'approved_by', 'approved_by_name', 'approval_date',
                  'rejection_reason', 'supporting_document', 'created_at']
        read_only_fields = ['id', 'number_of_days', 'created_at', 'approved_by', 'approval_date']
    
    def validate(self, data):
        """Validate leave dates"""
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("End date must be after start date.")
        return data
