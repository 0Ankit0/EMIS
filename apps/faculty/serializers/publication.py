"""Faculty Publication Serializer"""
from rest_framework import serializers
from ..models import FacultyPublication


class FacultyPublicationSerializer(serializers.ModelSerializer):
    """Serializer for FacultyPublication"""
    
    class Meta:
        model = FacultyPublication
        fields = ['id', 'title', 'publication_type', 'authors', 'journal_or_conference',
                  'volume', 'issue', 'pages', 'year', 'doi', 'isbn_issn', 'url',
                  'abstract', 'keywords', 'citation_count', 'impact_factor',
                  'is_indexed', 'document', 'created_at']
        read_only_fields = ['id', 'created_at']
