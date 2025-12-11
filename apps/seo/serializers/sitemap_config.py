"""Sitemap Config Serializer"""
from rest_framework import serializers
from ..models import SitemapConfig


class SitemapConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitemapConfig
        fields = [
            'id', 'app_label', 'model_name', 'is_enabled',
            'priority', 'changefreq', 'url_field', 'lastmod_field',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
