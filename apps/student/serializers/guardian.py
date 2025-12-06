from rest_framework import serializers
from ..models import Guardian, Student

class GuardianCreateSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(slug_field='ukid', queryset=Student.objects.all(), many=True)

    class Meta:
        model = Guardian
        fields = [
            'student', 'first_name', 'last_name', 'relationship', 
            'phone_number', 'email', 'address'
        ]

class GuardianUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            'first_name', 'last_name', 'relationship', 'phone_number', 
            'email', 'address', 'updated_by'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}

class GuardianResponseSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Guardian
        fields = [
            'ukid', 'first_name', 'last_name', 'full_name', 'relationship', 
            'phone_number', 'email', 'address', 'student_count', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['ukid', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_student_count(self, obj):
        return obj.student.count()