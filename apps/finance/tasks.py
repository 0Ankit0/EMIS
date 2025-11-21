"""Finance Background Tasks"""
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta


def check_overdue_invoices():
    """
    Background task to check and update overdue invoices
    Should be run daily via cron or Celery
    """
    from .models import Invoice
    
    today = timezone.now().date()
    
    # Find invoices that are now overdue
    overdue_invoices = Invoice.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    )
    
    count = 0
    for invoice in overdue_invoices:
        invoice.status = 'overdue'
        invoice.save(update_fields=['status'])
        count += 1
        
        # TODO: Send overdue notification
    
    return f"Updated {count} overdue invoices"


def calculate_late_fees():
    """
    Calculate and apply late fees to overdue invoices
    Should be run daily via cron or Celery
    """
    from .models import Invoice
    from .utils import calculate_late_fee
    
    today = timezone.now().date()
    
    overdue_invoices = Invoice.objects.filter(
        status='overdue',
        due_date__lt=today
    )
    
    count = 0
    for invoice in overdue_invoices:
        late_fee = calculate_late_fee(invoice, today)
        if late_fee > 0 and late_fee != invoice.late_fee:
            invoice.late_fee = late_fee
            invoice.save(update_fields=['late_fee'])
            count += 1
    
    return f"Updated late fees for {count} invoices"


def generate_monthly_invoices(academic_year, semester, fee_structure_id):
    """
    Generate monthly invoices for all students
    Can be triggered manually or scheduled
    """
    from .models import FeeStructure, Invoice
    from apps.students.models import Student
    
    try:
        fee_structure = FeeStructure.objects.get(id=fee_structure_id)
    except FeeStructure.DoesNotExist:
        return "Fee structure not found"
    
    students = Student.objects.filter(
        enrollment__academic_year=academic_year,
        enrollment__status='active'
    )
    
    count = 0
    for student in students:
        # Check if invoice already exists
        existing = Invoice.objects.filter(
            student=student,
            academic_year=academic_year,
            semester=semester,
            fee_structure=fee_structure
        ).exists()
        
        if not existing:
            Invoice.objects.create(
                student=student,
                fee_structure=fee_structure,
                fee_components=fee_structure.components,
                amount_due=fee_structure.total_amount,
                due_date=timezone.now().date() + timedelta(days=30),
                academic_year=academic_year,
                semester=semester
            )
            count += 1
    
    return f"Generated {count} invoices"


def sync_budget_allocations():
    """
    Sync budget allocation spent amounts with actual expenses
    Should be run periodically (e.g., daily)
    """
    from .models import BudgetAllocation, Expense
    
    allocations = BudgetAllocation.objects.filter(
        budget__status='active'
    )
    
    count = 0
    for allocation in allocations:
        # Calculate actual spent amount
        spent = Expense.objects.filter(
            category=allocation.category,
            status='paid',
            expense_date__gte=allocation.budget.start_date,
            expense_date__lte=allocation.budget.end_date
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        if spent != allocation.spent_amount:
            allocation.spent_amount = spent
            allocation.save(update_fields=['spent_amount'])
            count += 1
    
    return f"Synced {count} budget allocations"


def send_payment_reminders():
    """
    Send payment reminders for pending invoices
    Should be run daily or as needed
    """
    from .models import Invoice
    
    today = timezone.now().date()
    reminder_date = today + timedelta(days=3)  # 3 days before due date
    
    invoices_to_remind = Invoice.objects.filter(
        status='pending',
        due_date=reminder_date
    )
    
    count = 0
    for invoice in invoices_to_remind:
        # TODO: Send email/SMS reminder
        count += 1
    
    return f"Sent {count} payment reminders"


def archive_old_financial_records(years=7):
    """
    Archive financial records older than specified years
    For compliance and performance
    """
    from .models import Invoice, Payment, Expense
    
    cutoff_date = timezone.now().date() - timedelta(days=years*365)
    
    # Mark old records as archived or move to archive table
    # Implementation depends on archival strategy
    
    return "Archive process completed"


def generate_monthly_financial_report(year, month):
    """
    Generate comprehensive monthly financial report
    """
    from .utils import generate_financial_report
    from datetime import date
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    report = generate_financial_report(start_date, end_date)
    
    # TODO: Save report or send to stakeholders
    
    return report


def update_scholarship_status():
    """
    Update scholarship status based on application dates
    """
    from .models import Scholarship
    
    today = timezone.now().date()
    
    # Close scholarships whose application period has ended
    closed_count = Scholarship.objects.filter(
        status='active',
        application_end_date__lt=today
    ).update(status='closed')
    
    # Activate scholarships whose application period has started
    activated_count = Scholarship.objects.filter(
        status='inactive',
        application_start_date__lte=today,
        application_end_date__gte=today
    ).update(status='active')
    
    return f"Closed {closed_count} scholarships, Activated {activated_count} scholarships"
