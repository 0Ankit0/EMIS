"""SEO Metadata Serializer"""
from rest_framework import serializers
from ..models import SEOMetadata


class SEOMetadataSerializer(serializers.ModelSerializer):
    content_type_display = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = SEOMetadata
        fields = [
            'id', 'content_type', 'content_type_display', 'object_id',
            'meta_title', 'meta_description', 'meta_keywords',
            'canonical_url', 'robots',
            'og_title', 'og_description', 'og_image', 'og_type', 'og_url',
            'twitter_card', 'twitter_title', 'twitter_description', 'twitter_image',
            'twitter_site', 'twitter_creator',
            'schema_markup',
            'include_in_sitemap', 'sitemap_priority', 'sitemap_changefreq',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_meta_title(self, value):
        if len(value) > 70:
            raise serializers.ValidationError("Meta title should be 70 characters or less for optimal SEO")
        return value
    
    def validate_meta_description(self, value):
        if len(value) > 160:
            raise serializers.ValidationError("Meta description should be 160 characters or less for optimal SEO")
        return value
