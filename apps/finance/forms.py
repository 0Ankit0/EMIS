"""Finance Forms"""
from django import forms
from .models import (
    FeeStructure, Invoice, Payment, ExpenseCategory, Expense,
    Budget, BudgetAllocation, Scholarship, ScholarshipApplication
)


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['name', 'code', 'description', 'program', 'academic_year', 'semester',
                  'components', 'total_amount', 'installment_rules', 'late_fee_policy',
                  'valid_from', 'valid_to', 'is_active']
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valid_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['student', 'fee_structure', 'fee_components', 'amount_due',
                  'due_date', 'description', 'academic_year', 'semester']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['invoice', 'amount_paid', 'method', 'reference_number', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'title', 'description', 'amount', 'tax_amount',
                  'expense_date', 'priority', 'vendor_name', 'vendor_contact',
                  'invoice_number', 'attachment', 'notes']
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'code', 'description', 'period_type', 'fiscal_year',
                  'start_date', 'end_date', 'total_allocated', 'department', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['name', 'code', 'description', 'scholarship_type', 'amount',
                  'percentage', 'eligibility_criteria', 'total_slots', 'valid_from',
                  'valid_to', 'application_start_date', 'application_end_date', 'attachment']
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valid_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'application_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'application_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'eligibility_criteria': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = ['scholarship', 'student', 'justification', 'documents']
        widgets = {
            'justification': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
