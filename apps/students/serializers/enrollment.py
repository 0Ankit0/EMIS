"""Enrollment serializers"""
from rest_framework import serializers
from ..models import Enrollment


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating enrollments"""
    
    class Meta:
        model = Enrollment
        fields = [
            'student', 'program', 'batch', 'section', 'start_date',
            'expected_end_date', 'status', 'application', 'enrollment_data'
        ]
    
    def validate(self, data):
        # Check for duplicate enrollment
        student = data.get('student')
        program = data.get('program')
        start_date = data.get('start_date')
        
        if Enrollment.objects.filter(
            student=student,
            program=program,
            start_date=start_date
        ).exists():
            raise serializers.ValidationError(
                "Enrollment already exists for this student, program, and start date"
            )
        
        return data


class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating enrollments"""
    
    class Meta:
        model = Enrollment
        fields = [
            'section', 'expected_end_date', 'actual_end_date', 'status',
            'enrollment_data'
        ]


class EnrollmentResponseSerializer(serializers.ModelSerializer):
    """Serializer for enrollment responses"""
    
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'student_id', 'student_email',
            'program', 'batch', 'section', 'start_date', 'expected_end_date',
            'actual_end_date', 'status', 'application', 'enrollment_data',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
