"""Finance Serializers"""
from rest_framework import serializers
from .models import (
    FeeStructure, Invoice, Payment, ExpenseCategory, Expense,
    Budget, BudgetAllocation, Scholarship, ScholarshipApplication
)


class FeeStructureSerializer(serializers.ModelSerializer):
    """Serializer for FeeStructure"""
    total_calculated = serializers.SerializerMethodField()
    
    class Meta:
        model = FeeStructure
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_calculated(self, obj):
        return obj.calculate_total()


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['id', 'invoice_number', 'created_at', 'updated_at', 'balance', 'is_overdue']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'receipt_number', 'created_at', 'updated_at']


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Serializer for ExpenseCategory"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['id', 'expense_number', 'total_amount', 'created_at', 'updated_at']


class BudgetAllocationSerializer(serializers.ModelSerializer):
    """Serializer for BudgetAllocation"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    utilization_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = BudgetAllocation
        fields = '__all__'
        read_only_fields = ['id', 'balance', 'utilization_percentage', 'created_at', 'updated_at']


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget"""
    allocations = BudgetAllocationSerializer(many=True, read_only=True)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    utilization_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['id', 'balance', 'utilization_percentage', 'created_at', 'updated_at']


class ScholarshipSerializer(serializers.ModelSerializer):
    """Serializer for Scholarship"""
    available_slots = serializers.IntegerField(read_only=True)
    is_open_for_application = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ['id', 'filled_slots', 'available_slots', 'is_open_for_application', 'created_at', 'updated_at']


class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    """Serializer for ScholarshipApplication"""
    scholarship_name = serializers.CharField(source='scholarship.name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True)
    
    class Meta:
        model = ScholarshipApplication
        fields = '__all__'
        read_only_fields = ['id', 'application_date', 'created_at', 'updated_at']
