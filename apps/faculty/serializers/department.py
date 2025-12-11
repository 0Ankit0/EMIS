"""Department Serializer"""
from rest_framework import serializers
from ..models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department"""
    head_name = serializers.CharField(source='head.get_full_name', read_only=True)
    faculty_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'head', 'head_name', 
                  'is_active', 'faculty_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_faculty_count(self, obj):
        return obj.faculty_members.filter(status='active').count()
