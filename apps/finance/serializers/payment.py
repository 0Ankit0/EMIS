"""Payment serializers"""
from rest_framework import serializers
from apps.finance.models.payment import Payment
from apps.finance.models.invoice import Invoice
from apps.students.models.student import Student
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating payments"""
    
    invoice_id = serializers.IntegerField(write_only=True)
    processed_by_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Payment
        fields = [
            'invoice_id',
            'amount_paid',
            'late_fee_applied',
            'method',
            'payment_date',
            'reference_number',
            'remarks',
            'processed_by_id',
        ]
    
    def validate_invoice_id(self, value):
        """Validate invoice exists"""
        try:
            Invoice.objects.get(id=value)
        except Invoice.DoesNotExist:
            raise serializers.ValidationError(f"Invoice with id {value} does not exist")
        return value
    
    def validate_processed_by_id(self, value):
        """Validate user exists"""
        if value is not None:
            try:
                User.objects.get(id=value)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with id {value} does not exist")
        return value
    
    def validate(self, data):
        """Validate payment data"""
        invoice_id = data.get('invoice_id')
        amount_paid = data.get('amount_paid')
        
        if invoice_id and amount_paid:
            try:
                invoice = Invoice.objects.get(id=invoice_id)
                # Check if payment amount is valid
                if amount_paid <= 0:
                    raise serializers.ValidationError("Payment amount must be greater than zero")
                
                # Optional: Check if payment doesn't exceed balance
                balance = invoice.balance
                if amount_paid > balance:
                    raise serializers.ValidationError(
                        f"Payment amount (${amount_paid}) exceeds invoice balance (${balance})"
                    )
            except Invoice.DoesNotExist:
                pass  # Already validated
        
        return data
    
    def create(self, validated_data):
        """Create payment"""
        invoice_id = validated_data.pop('invoice_id')
        processed_by_id = validated_data.pop('processed_by_id', None)
        
        invoice = Invoice.objects.get(id=invoice_id)
        processed_by = User.objects.get(id=processed_by_id) if processed_by_id else None
        
        payment = Payment.objects.create(
            invoice=invoice,
            student=invoice.student,
            processed_by=processed_by,
            **validated_data
        )
        return payment


class PaymentResponseSerializer(serializers.ModelSerializer):
    """Serializer for payment responses"""
    
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.user.email', read_only=True)
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'receipt_number',
            'transaction_id',
            'invoice',
            'invoice_number',
            'student',
            'student_name',
            'student_email',
            'amount_paid',
            'late_fee_applied',
            'method',
            'payment_date',
            'reference_number',
            'remarks',
            'processed_by',
            'processed_by_name',
            'created_at',
            'updated_at',
        ]
