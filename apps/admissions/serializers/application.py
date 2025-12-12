"""Application serializers for admissions"""
from rest_framework import serializers
from ..models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications"""
    
    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'previous_school', 'previous_grade', 'gpa', 'program', 'admission_year',
            'admission_semester', 'application_data'
        ]
    
    def create(self, validated_data):
        # Application number will be generated automatically
        return Application.objects.create(**validated_data)


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating applications"""
    
    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'previous_school', 'previous_grade', 'gpa', 'application_data'
        ]


class ApplicationResponseSerializer(serializers.ModelSerializer):
    """Serializer for application responses"""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'application_number', 'full_name', 'first_name', 'last_name', 
            'email', 'phone', 'date_of_birth', 'gender',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'previous_school', 'previous_grade', 'gpa', 'program', 'admission_year',
            'admission_semester', 'status', 'merit_score', 'rank', 'submitted_at',
            'reviewed_by', 'reviewed_at', 'review_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'application_number', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ApplicationStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating application status"""
    
    status = serializers.ChoiceField(choices=Application.Status.choices)
    review_notes = serializers.CharField(required=False, allow_blank=True)
    merit_score = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    rank = serializers.IntegerField(required=False, allow_null=True)
