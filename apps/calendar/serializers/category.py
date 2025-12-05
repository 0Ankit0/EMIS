from rest_framework import serializers
from ..models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['id']
        lookup_field = 'ukid'