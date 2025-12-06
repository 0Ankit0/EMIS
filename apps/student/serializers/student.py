from rest_framework import serializers
from ..models import Student

class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'registration_number', 'roll_number', 'first_name', 'middle_name', 
            'last_name', 'date_of_birth', 'gender', 'email', 'phone_number', 
            'address', 'city', 'state', 'postal_code', 'country', 'enrollment_date'
        ]
    
    def validate(self, attrs):
        from datetime import date
        errors = {}
        
        if attrs.get('date_of_birth'):
            age = (date.today() - attrs['date_of_birth']).days / 365.25
            if age < 3:
                errors['date_of_birth'] = 'Student must be at least 3 years old.'
            if age > 100:
                errors['date_of_birth'] = 'Invalid date of birth.'
        
        if attrs.get('enrollment_date') and attrs['enrollment_date'] > date.today():
            errors['enrollment_date'] = 'Enrollment date cannot be in the future.'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'roll_number', 'first_name', 'middle_name', 'last_name', 
            'date_of_birth', 'gender', 'email', 'phone_number', 'address', 
            'city', 'state', 'postal_code', 'country', 'is_active', 'updated_by'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}
    
    def validate(self, attrs):
        from datetime import date
        instance = self.instance
        errors = {}
        
        date_of_birth = attrs.get('date_of_birth', instance.date_of_birth if instance else None)
        if date_of_birth:
            age = (date.today() - date_of_birth).days / 365.25
            if age < 3:
                errors['date_of_birth'] = 'Student must be at least 3 years old.'
            if age > 100:
                errors['date_of_birth'] = 'Invalid date of birth.'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

class StudentResponseSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'ukid', 'registration_number', 'roll_number', 'first_name', 
            'middle_name', 'last_name', 'full_name', 'date_of_birth', 'gender', 
            'email', 'phone_number', 'address', 'city', 'state', 'postal_code', 
            'country', 'enrollment_date', 'is_active', 'enrollment_count', 
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'ukid', 'registration_number', 'created_at', 'updated_at'
        ]
    
    def get_full_name(self, obj):
        if obj.middle_name:
            return f"{obj.first_name} {obj.middle_name} {obj.last_name}"
        return f"{obj.first_name} {obj.last_name}"
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.count()