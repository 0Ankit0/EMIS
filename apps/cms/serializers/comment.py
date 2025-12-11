"""Comment Serializer"""
from rest_framework import serializers
from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'author', 'author_name', 'name',
            'email', 'content', 'is_approved', 'parent',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']
