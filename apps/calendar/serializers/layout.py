from rest_framework import serializers
from apps.calendar.models import CalendarLayout

class CalendarLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarLayout
        fields = ['id', 'name', 'active', 'configuration', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Assign the current user to the layout
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
