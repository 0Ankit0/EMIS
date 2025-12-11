"""Page Serializer"""
from rest_framework import serializers
from ..models import Page


class PageSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'featured_image',
            'status', 'is_homepage', 'template', 'author', 'author_name',
            'meta_title', 'meta_description', 'meta_keywords',
            'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'author']


class PageListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'status', 'is_homepage', 'author_name', 'published_at']
