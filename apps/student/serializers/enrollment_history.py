from rest_framework import serializers
from ..models import EnrollmentHistory

class EnrollmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentHistory
        fields = '__all__'
        exclude = ['id']
        lookup_field = 'ukid'