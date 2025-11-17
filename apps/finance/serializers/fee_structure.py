"""Fee structure serializers"""
from rest_framework import serializers
from apps.finance.models.fee_structure import FeeStructure
from decimal import Decimal


class FeeStructureCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating fee structures"""
    
    class Meta:
        model = FeeStructure
        fields = [
            'name',
            'code',
            'description',
            'program',
            'academic_year',
            'semester',
            'components',
            'installment_rules',
            'late_fee_policy',
            'valid_from',
            'valid_to',
            'is_active',
        ]
    
    def validate_components(self, value):
        """Validate fee components"""
        if not value:
            raise serializers.ValidationError("Fee components cannot be empty")
        
        # Ensure all values are numeric
        for key, amount in value.items():
            try:
                float(amount)
            except (ValueError, TypeError):
                raise serializers.ValidationError(f"Invalid amount for {key}: {amount}")
        
        return value
    
    def validate(self, data):
        """Validate fee structure data"""
        # Calculate total from components
        if data.get('components'):
            total = sum(float(v) for v in data['components'].values())
            data['total_amount'] = Decimal(str(total))
        
        # Validate date range
        if data.get('valid_from') and data.get('valid_to'):
            if data['valid_from'] > data['valid_to']:
                raise serializers.ValidationError("valid_from must be before valid_to")
        
        return data


class FeeStructureUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating fee structures"""
    
    class Meta:
        model = FeeStructure
        fields = [
            'name',
            'description',
            'components',
            'installment_rules',
            'late_fee_policy',
            'valid_from',
            'valid_to',
            'is_active',
        ]
    
    def validate_components(self, value):
        """Validate fee components"""
        if value is not None:
            for key, amount in value.items():
                try:
                    float(amount)
                except (ValueError, TypeError):
                    raise serializers.ValidationError(f"Invalid amount for {key}: {amount}")
        return value
    
    def validate(self, data):
        """Recalculate total if components changed"""
        if data.get('components'):
            total = sum(float(v) for v in data['components'].values())
            data['total_amount'] = Decimal(str(total))
        
        if data.get('valid_from') and data.get('valid_to'):
            if data['valid_from'] > data['valid_to']:
                raise serializers.ValidationError("valid_from must be before valid_to")
        
        return data


class FeeStructureResponseSerializer(serializers.ModelSerializer):
    """Serializer for fee structure responses"""
    
    total_calculated = serializers.SerializerMethodField()
    
    class Meta:
        model = FeeStructure
        fields = [
            'id',
            'name',
            'code',
            'description',
            'program',
            'academic_year',
            'semester',
            'components',
            'total_amount',
            'total_calculated',
            'installment_rules',
            'late_fee_policy',
            'valid_from',
            'valid_to',
            'is_active',
            'created_at',
            'updated_at',
        ]
    
    def get_total_calculated(self, obj):
        """Calculate total from components for verification"""
        return obj.calculate_total()
