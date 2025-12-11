"""Tag Serializer"""
from rest_framework import serializers
from ..models import Tag


class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()
