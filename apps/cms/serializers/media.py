"""Media Serializer"""
from rest_framework import serializers
from ..models import Media


class MediaSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    file_size_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Media
        fields = [
            'id', 'title', 'file', 'file_type', 'file_size', 'file_size_display',
            'alt_text', 'caption', 'uploaded_by', 'uploaded_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'file_size', 'created_at', 'updated_at', 'uploaded_by']
    
    def get_file_size_display(self, obj):
        """Return human-readable file size"""
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
