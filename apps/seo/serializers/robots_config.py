"""Robots Config Serializer"""
from rest_framework import serializers
from ..models import RobotsConfig


class RobotsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotsConfig
        fields = [
            'id', 'user_agent', 'disallow', 'allow', 'crawl_delay',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
