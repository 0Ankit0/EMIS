"""Category Serializer"""
from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent', 'parent_name',
            'is_active', 'post_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()
