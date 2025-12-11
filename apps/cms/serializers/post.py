"""Post Serializer"""
from rest_framework import serializers
from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, source='tags', queryset=None
    )
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'featured_image',
            'category', 'category_name', 'tags', 'tag_ids', 'author', 'author_name',
            'status', 'is_featured', 'views', 'comment_count',
            'meta_title', 'meta_description', 'meta_keywords',
            'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'views', 'created_at', 'updated_at', 'author']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'tag_ids' in self.fields:
            from ..models import Tag
            self.fields['tag_ids'].queryset = Tag.objects.all()
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class PostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'category_name', 'author_name', 'status', 'is_featured',
            'views', 'published_at'
        ]
