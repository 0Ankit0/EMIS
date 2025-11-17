"""Invoice serializers"""
from rest_framework import serializers
from apps.finance.models.invoice import Invoice
from apps.finance.models.fee_structure import FeeStructure
from apps.students.models.student import Student
from decimal import Decimal


class InvoiceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating invoices"""
    
    student_id = serializers.IntegerField(write_only=True)
    fee_structure_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Invoice
        fields = [
            'student_id',
            'fee_structure_id',
            'fee_components',
            'amount_due',
            'due_date',
            'description',
            'notes',
            'academic_year',
            'semester',
        ]
    
    def validate_student_id(self, value):
        """Validate student exists"""
        try:
            Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError(f"Student with id {value} does not exist")
        return value
    
    def validate_fee_structure_id(self, value):
        """Validate fee structure exists"""
        if value is not None:
            try:
                FeeStructure.objects.get(id=value)
            except FeeStructure.DoesNotExist:
                raise serializers.ValidationError(f"Fee structure with id {value} does not exist")
        return value
    
    def validate_fee_components(self, value):
        """Validate fee components"""
        if not value:
            raise serializers.ValidationError("Fee components cannot be empty")
        
        for key, amount in value.items():
            try:
                float(amount)
            except (ValueError, TypeError):
                raise serializers.ValidationError(f"Invalid amount for {key}: {amount}")
        
        return value
    
    def create(self, validated_data):
        """Create invoice"""
        student_id = validated_data.pop('student_id')
        fee_structure_id = validated_data.pop('fee_structure_id', None)
        
        student = Student.objects.get(id=student_id)
        fee_structure = FeeStructure.objects.get(id=fee_structure_id) if fee_structure_id else None
        
        invoice = Invoice.objects.create(
            student=student,
            fee_structure=fee_structure,
            **validated_data
        )
        return invoice


class InvoiceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating invoices"""
    
    class Meta:
        model = Invoice
        fields = [
            'fee_components',
            'amount_due',
            'late_fee',
            'due_date',
            'status',
            'description',
            'notes',
        ]


class InvoiceResponseSerializer(serializers.ModelSerializer):
    """Serializer for invoice responses"""
    
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.user.email', read_only=True)
    fee_structure_name = serializers.CharField(source='fee_structure.name', read_only=True, allow_null=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    is_paid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'student',
            'student_name',
            'student_email',
            'fee_structure',
            'fee_structure_name',
            'fee_components',
            'amount_due',
            'amount_paid',
            'late_fee',
            'balance',
            'invoice_date',
            'due_date',
            'status',
            'is_overdue',
            'is_paid',
            'description',
            'notes',
            'academic_year',
            'semester',
            'created_at',
            'updated_at',
        ]
