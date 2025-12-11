"""Newsletter & SEO Serializers"""
from rest_framework import serializers
from ..models import Newsletter, SEO


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'is_active', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']


class SEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEO
        fields = [
            'id', 'page', 'post', 'meta_title', 'meta_description',
            'meta_keywords', 'og_title', 'og_description', 'og_image',
            'twitter_card', 'canonical_url', 'robots',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
