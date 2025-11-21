"""Finance Utility Functions"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum, Q, Avg
from decimal import Decimal
from datetime import timedelta, date
import csv
from io import StringIO


def generate_invoice_number(prefix='INV'):
    """Generate unique invoice number"""
    from .models import Invoice
    year = timezone.now().year
    count = Invoice.objects.filter(created_at__year=year).count() + 1
    return f"{prefix}-{year}-{count:06d}"


def generate_receipt_number(prefix='RCP'):
    """Generate unique receipt number"""
    from .models import Payment
    year = timezone.now().year
    count = Payment.objects.filter(created_at__year=year).count() + 1
    return f"{prefix}-{year}-{count:06d}"


def generate_expense_number(prefix='EXP'):
    """Generate unique expense number"""
    from .models import Expense
    year = timezone.now().year
    count = Expense.objects.filter(created_at__year=year).count() + 1
    return f"{prefix}-{year}-{count:06d}"


def calculate_late_fee(invoice, current_date=None):
    """
    Calculate late fee for an invoice
    
    Args:
        invoice: Invoice instance
        current_date: Date to calculate from (default: today)
    
    Returns:
        Decimal: Late fee amount
    """
    if current_date is None:
        current_date = timezone.now().date()
    
    if current_date <= invoice.due_date:
        return Decimal('0.00')
    
    days_overdue = (current_date - invoice.due_date).days
    
    if hasattr(invoice.fee_structure, 'late_fee_policy') and invoice.fee_structure.late_fee_policy:
        policy = invoice.fee_structure.late_fee_policy
        grace_days = policy.get('grace_days', 0)
        
        if days_overdue <= grace_days:
            return Decimal('0.00')
        
        # Calculate based on percentage or flat fee
        if 'percentage' in policy:
            percentage = Decimal(str(policy['percentage']))
            return (invoice.amount_due * percentage / 100).quantize(Decimal('0.01'))
        elif 'flat_fee' in policy:
            return Decimal(str(policy['flat_fee']))
    
    # Default late fee: 1% of amount due
    return (invoice.amount_due * Decimal('0.01')).quantize(Decimal('0.01'))


def calculate_installment_schedule(fee_structure, start_date=None):
    """
    Calculate installment schedule based on fee structure
    
    Args:
        fee_structure: FeeStructure instance
        start_date: Start date for installments (default: today)
    
    Returns:
        list: List of installment details
    """
    if start_date is None:
        start_date = timezone.now().date()
    
    installments = []
    
    if not fee_structure.installment_rules or not fee_structure.installment_rules.get('enabled'):
        # Single payment
        installments.append({
            'number': 1,
            'due_date': start_date + timedelta(days=30),
            'amount': fee_structure.total_amount
        })
        return installments
    
    count = fee_structure.installment_rules.get('count', 1)
    schedule = fee_structure.installment_rules.get('schedule', [])
    
    if schedule:
        # Custom schedule provided
        for idx, item in enumerate(schedule, 1):
            installments.append({
                'number': idx,
                'due_date': start_date + timedelta(days=item.get('days_from_start', idx * 30)),
                'amount': Decimal(str(item.get('amount', fee_structure.total_amount / count)))
            })
    else:
        # Equal installments
        amount_per_installment = (fee_structure.total_amount / count).quantize(Decimal('0.01'))
        for i in range(count):
            installments.append({
                'number': i + 1,
                'due_date': start_date + timedelta(days=(i + 1) * 30),
                'amount': amount_per_installment
            })
    
    return installments


def generate_financial_report(start_date, end_date, department=None):
    """
    Generate comprehensive financial report
    
    Args:
        start_date: Report start date
        end_date: Report end date
        department: Optional department filter
    
    Returns:
        dict: Financial report data
    """
    from .models import Invoice, Payment, Expense, Budget
    
    # Revenue data
    invoices = Invoice.objects.filter(
        invoice_date__gte=start_date,
        invoice_date__lte=end_date
    )
    
    payments = Payment.objects.filter(
        payment_date__gte=start_date,
        payment_date__lte=end_date
    )
    
    # Expense data
    expenses = Expense.objects.filter(
        expense_date__gte=start_date,
        expense_date__lte=end_date,
        status='paid'
    )
    
    if department:
        expenses = expenses.filter(category__budget_allocations__budget__department=department)
    
    report = {
        'period': {
            'start_date': start_date,
            'end_date': end_date,
        },
        'revenue': {
            'invoices_generated': invoices.count(),
            'total_billed': invoices.aggregate(Sum('amount_due'))['amount_due__sum'] or 0,
            'total_collected': payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0,
            'pending': invoices.filter(status__in=['pending', 'partial', 'overdue']).aggregate(Sum('amount_due'))['amount_due__sum'] or 0,
        },
        'expenses': {
            'total_expenses': expenses.count(),
            'total_amount': expenses.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'by_category': {},
        },
        'net': {
            'income': (payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0) - (expenses.aggregate(Sum('total_amount'))['total_amount__sum'] or 0),
        }
    }
    
    # Expenses by category
    expense_categories = expenses.values('category__name').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    for cat in expense_categories:
        report['expenses']['by_category'][cat['category__name']] = {
            'count': cat['count'],
            'total': cat['total']
        }
    
    return report


def export_invoices_to_csv(queryset):
    """Export invoices to CSV format"""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Invoice Number', 'Student Email', 'Amount Due', 'Amount Paid', 
        'Balance', 'Status', 'Invoice Date', 'Due Date', 'Academic Year'
    ])
    
    for invoice in queryset:
        writer.writerow([
            invoice.invoice_number,
            invoice.student.user.email,
            invoice.amount_due,
            invoice.amount_paid,
            invoice.balance,
            invoice.get_status_display(),
            invoice.invoice_date.strftime('%Y-%m-%d'),
            invoice.due_date.strftime('%Y-%m-%d'),
            invoice.academic_year
        ])
    
    return output.getvalue()


def export_payments_to_csv(queryset):
    """Export payments to CSV format"""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Receipt Number', 'Invoice Number', 'Student Email', 'Amount Paid',
        'Method', 'Payment Date', 'Transaction ID', 'Processed By'
    ])
    
    for payment in queryset:
        writer.writerow([
            payment.receipt_number,
            payment.invoice.invoice_number,
            payment.student.user.email,
            payment.amount_paid,
            payment.get_method_display(),
            payment.payment_date.strftime('%Y-%m-%d %H:%M'),
            payment.transaction_id or '',
            payment.processed_by.get_full_name() if payment.processed_by else ''
        ])
    
    return output.getvalue()


def export_expenses_to_csv(queryset):
    """Export expenses to CSV format"""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Expense Number', 'Title', 'Category', 'Amount', 'Tax', 'Total Amount',
        'Status', 'Expense Date', 'Vendor', 'Requested By', 'Approved By'
    ])
    
    for expense in queryset:
        writer.writerow([
            expense.expense_number,
            expense.title,
            expense.category.name,
            expense.amount,
            expense.tax_amount,
            expense.total_amount,
            expense.get_status_display(),
            expense.expense_date.strftime('%Y-%m-%d'),
            expense.vendor_name,
            expense.requested_by.get_full_name() if expense.requested_by else '',
            expense.approved_by.get_full_name() if expense.approved_by else ''
        ])
    
    return output.getvalue()


def validate_payment_amount(invoice, payment_amount):
    """
    Validate payment amount against invoice
    
    Args:
        invoice: Invoice instance
        payment_amount: Amount being paid
    
    Returns:
        tuple: (is_valid, error_message)
    """
    payment_amount = Decimal(str(payment_amount))
    
    if payment_amount <= 0:
        return False, "Payment amount must be greater than zero"
    
    outstanding = invoice.balance
    
    if payment_amount > outstanding:
        return False, f"Payment amount (${payment_amount}) exceeds outstanding balance (${outstanding})"
    
    return True, None


def calculate_scholarship_amount(scholarship, student_fee_amount=None):
    """
    Calculate scholarship amount for a student
    
    Args:
        scholarship: Scholarship instance
        student_fee_amount: Student's total fee amount (required if scholarship is percentage-based)
    
    Returns:
        Decimal: Scholarship amount
    """
    if scholarship.amount:
        return scholarship.amount
    
    if scholarship.percentage and student_fee_amount:
        return (Decimal(str(student_fee_amount)) * scholarship.percentage / 100).quantize(Decimal('0.01'))
    
    return Decimal('0.00')


def check_budget_availability(category, amount):
    """
    Check if budget is available for an expense
    
    Args:
        category: ExpenseCategory instance
        amount: Expense amount to check
    
    Returns:
        tuple: (is_available, message)
    """
    from .models import BudgetAllocation
    
    today = timezone.now().date()
    
    # Find active budget allocations for this category
    allocations = BudgetAllocation.objects.filter(
        category=category,
        budget__status='active',
        budget__start_date__lte=today,
        budget__end_date__gte=today
    )
    
    if not allocations.exists():
        return True, "No active budget found - approval required"
    
    for allocation in allocations:
        if allocation.balance >= Decimal(str(amount)):
            return True, f"Budget available: ${allocation.balance}"
    
    return False, "Insufficient budget allocation"


def send_invoice_notification(invoice):
    """Send invoice notification to student"""
    # TODO: Implement email/SMS notification
    pass


def send_payment_confirmation(payment):
    """Send payment confirmation to student"""
    # TODO: Implement email/SMS notification
    pass


def send_scholarship_notification(application, status):
    """Send scholarship application status notification"""
    # TODO: Implement email notification
    pass


from django.db.models import Count

def get_revenue_trends(months=12):
    """Get revenue trends for the last N months"""
    from .models import Payment
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    end_date = timezone.now()
    start_date = end_date - relativedelta(months=months)
    
    # Group payments by month
    payments = Payment.objects.filter(
        payment_date__gte=start_date,
        payment_date__lte=end_date
    ).extra(
        select={'month': "DATE_TRUNC('month', payment_date)"}
    ).values('month').annotate(
        total=Sum('amount_paid'),
        count=Count('id')
    ).order_by('month')
    
    return list(payments)


def get_expense_trends(months=12):
    """Get expense trends for the last N months"""
    from .models import Expense
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    end_date = timezone.now()
    start_date = end_date - relativedelta(months=months)
    
    expenses = Expense.objects.filter(
        expense_date__gte=start_date,
        expense_date__lte=end_date,
        status='paid'
    ).extra(
        select={'month': "DATE_TRUNC('month', expense_date)"}
    ).values('month').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    ).order_by('month')
    
    return list(expenses)
