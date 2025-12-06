from rest_framework import serializers
from ..models import AcademicRecord
from .student import StudentResponseSerializer

class AcademicRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = ['student', 'semester', 'gpa', 'total_credits', 'remarks']
    
    def validate(self, attrs):
        errors = {}
        
        if attrs.get('gpa') is not None:
            if attrs['gpa'] < 0 or attrs['gpa'] > 4.00:
                errors['gpa'] = 'GPA must be between 0.00 and 4.00.'
        
        if attrs.get('total_credits') is not None and attrs['total_credits'] < 0:
            errors['total_credits'] = 'Total credits cannot be negative.'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

class AcademicRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = ['semester', 'gpa', 'total_credits', 'remarks', 'updated_by']
        extra_kwargs = {field: {'required': False} for field in fields}
    
    def validate(self, attrs):
        instance = self.instance
        errors = {}
        
        gpa = attrs.get('gpa', instance.gpa if instance else None)
        if gpa is not None:
            if gpa < 0 or gpa > 4.00:
                errors['gpa'] = 'GPA must be between 0.00 and 4.00.'
        
        total_credits = attrs.get('total_credits', instance.total_credits if instance else None)
        if total_credits is not None and total_credits < 0:
            errors['total_credits'] = 'Total credits cannot be negative.'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

class AcademicRecordResponseSerializer(serializers.ModelSerializer):
    student = StudentResponseSerializer(read_only=True)
    
    class Meta:
        model = AcademicRecord
        fields = [
            'ukid', 'student', 'semester', 'gpa', 'total_credits', 'remarks', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['ukid', 'created_at', 'updated_at']