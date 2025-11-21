"""Finance Filters"""
import django_filters
from .models import Invoice, Payment, Expense, Budget, Scholarship


class InvoiceFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Invoice.STATUS_CHOICES)
    academic_year = django_filters.CharFilter(lookup_expr='icontains')
    invoice_date = django_filters.DateFromToRangeFilter()
    due_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Invoice
        fields = ['status', 'academic_year', 'semester', 'student']


class PaymentFilter(django_filters.FilterSet):
    method = django_filters.ChoiceFilter(choices=Payment.METHOD_CHOICES)
    payment_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Payment
        fields = ['method', 'invoice', 'student']


class ExpenseFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Expense.STATUS_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Expense.PRIORITY_CHOICES)
    expense_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Expense
        fields = ['status', 'priority', 'category']


class BudgetFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Budget.STATUS_CHOICES)
    
    class Meta:
        model = Budget
        fields = ['status', 'fiscal_year', 'period_type', 'department']


class ScholarshipFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Scholarship.STATUS_CHOICES)
    scholarship_type = django_filters.ChoiceFilter(choices=Scholarship.TYPE_CHOICES)
    
    class Meta:
        model = Scholarship
        fields = ['status', 'scholarship_type']
