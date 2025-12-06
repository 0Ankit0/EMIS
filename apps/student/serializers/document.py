from rest_framework import serializers
from ..models import Document, DocumentType, Student
from .student import StudentResponseSerializer

class DocumentCreateSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(slug_field='ukid', queryset=Student.objects.all())

    class Meta:
        model = Document
        fields = ['student', 'document_type', 'file']

class DocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_type', 'file', 'is_verified', 'updated_by']
        extra_kwargs = {field: {'required': False} for field in fields}

class DocumentResponseSerializer(serializers.ModelSerializer):
    student = StudentResponseSerializer(read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'ukid', 'student', 'document_type', 'document_type_display', 'file', 
            'is_verified', 'verified_by', 'verified_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'ukid', 'verified_by', 'verified_at', 'created_at', 'updated_at'
        ]