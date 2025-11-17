"""Merit list serializers"""
from rest_framework import serializers
from ..models import MeritList
from .application import ApplicationResponseSerializer


class MeritListCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating merit lists"""
    
    class Meta:
        model = MeritList
        fields = [
            'name', 'program', 'admission_year', 'admission_semester',
            'criteria', 'version', 'cutoff_score', 'total_seats',
            'merit_list_data'
        ]


class MeritListResponseSerializer(serializers.ModelSerializer):
    """Serializer for merit list responses"""
    
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    total_applications = serializers.SerializerMethodField()
    
    class Meta:
        model = MeritList
        fields = [
            'id', 'name', 'program', 'admission_year', 'admission_semester',
            'criteria', 'version', 'cutoff_score', 'total_seats',
            'is_published', 'generation_timestamp', 'generated_by',
            'generated_by_name', 'total_applications', 'merit_list_data',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'generation_timestamp', 'created_at', 'updated_at']
    
    def get_total_applications(self, obj):
        from ..models import Application
        return Application.objects.filter(
            program=obj.program,
            admission_year=obj.admission_year,
            admission_semester=obj.admission_semester,
            status='accepted'
        ).count()


class MeritListDetailSerializer(MeritListResponseSerializer):
    """Detailed merit list with applications"""
    
    applications = serializers.SerializerMethodField()
    
    class Meta(MeritListResponseSerializer.Meta):
        fields = MeritListResponseSerializer.Meta.fields + ['applications']
    
    def get_applications(self, obj):
        from ..models import Application
        applications = Application.objects.filter(
            program=obj.program,
            admission_year=obj.admission_year,
            admission_semester=obj.admission_semester,
            status='accepted',
            rank__isnull=False
        ).order_by('rank')[:obj.total_seats] if obj.total_seats else applications
        
        return ApplicationResponseSerializer(applications, many=True).data
