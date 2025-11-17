"""Student serializers"""
from rest_framework import serializers
from ..models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'phone', 'date_of_birth', 'gender', 'admission_year', 
            'program', 'batch', 'section', 'student_status', 'guardian_name',
            'guardian_phone', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'student_id', 'created_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
