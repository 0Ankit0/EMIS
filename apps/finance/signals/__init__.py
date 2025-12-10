"""Finance Signals"""
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Payment, Invoice, Expense, ScholarshipApplication, BudgetAllocation


@receiver(post_save, sender=Payment)
def update_invoice_on_payment(sender, instance, created, **kwargs):
    """Update invoice amount_paid when a payment is created or updated"""
    if instance.invoice:
        # Calculate total payments for this invoice
        total_paid = instance.invoice.payments.aggregate(
            total=models.Sum('amount_paid')
        )['total'] or 0
        
        # Update invoice
        Invoice.objects.filter(pk=instance.invoice.pk).update(
            amount_paid=total_paid
        )
        
        # Refresh invoice to update status
        instance.invoice.refresh_from_db()
        instance.invoice.save()


@receiver(pre_save, sender=Invoice)
def calculate_invoice_status(sender, instance, **kwargs):
    """Calculate and update invoice status before saving"""
    if instance.pk:  # Only for existing invoices
        # Status is calculated in the model's save method
        pass


@receiver(post_save, sender=Expense)
def update_budget_allocation_on_expense(sender, instance, created, **kwargs):
    """Update budget allocation when expense is paid"""
    if instance.status == 'paid' and instance.category:
        # Find active budget allocations for this category
        allocations = BudgetAllocation.objects.filter(
            category=instance.category,
            budget__status='active',
            budget__start_date__lte=instance.expense_date,
            budget__end_date__gte=instance.expense_date
        )
        
        for allocation in allocations:
            # Update spent amount
            total_spent = Expense.objects.filter(
                category=instance.category,
                status='paid',
                expense_date__gte=allocation.budget.start_date,
                expense_date__lte=allocation.budget.end_date
            ).aggregate(total=models.Sum('total_amount'))['total'] or 0
            
            allocation.spent_amount = total_spent
            allocation.save()


@receiver(post_save, sender=BudgetAllocation)
def update_budget_total_spent(sender, instance, **kwargs):
    """Update budget's total spent amount"""
    if instance.budget:
        total_spent = instance.budget.allocations.aggregate(
            total=models.Sum('spent_amount')
        )['total'] or 0
        
        instance.budget.total_spent = total_spent
        instance.budget.save(update_fields=['total_spent'])


@receiver(post_save, sender=ScholarshipApplication)
def update_scholarship_slots(sender, instance, created, **kwargs):
    """Update scholarship filled slots when application is awarded"""
    if instance.status == 'awarded':
        scholarship = instance.scholarship
        awarded_count = scholarship.applications.filter(status='awarded').count()
        scholarship.filled_slots = awarded_count
        scholarship.save(update_fields=['filled_slots'])


@receiver(post_save, sender=Invoice)
def check_overdue_invoices(sender, instance, **kwargs):
    """Check and update overdue invoices"""
    if instance.is_overdue and instance.status not in ['paid', 'overdue']:
        instance.status = 'overdue'
        instance.save(update_fields=['status'])


from django.db import models

@receiver(post_save, sender=Payment)
def send_payment_receipt(sender, instance, created, **kwargs):
    """Send payment receipt to student"""
    if created:
        # TODO: Send email/SMS with payment receipt
        pass


@receiver(post_save, sender=Invoice)
def send_invoice_notification(sender, instance, created, **kwargs):
    """Send invoice notification to student"""
    if created:
        # TODO: Send email/SMS notification
        pass


@receiver(post_save, sender=Expense)
def send_expense_approval_notification(sender, instance, **kwargs):
    """Send notification when expense is approved"""
    if instance.status == 'approved' and instance.requested_by:
        # TODO: Send notification to requester
        pass


@receiver(post_save, sender=ScholarshipApplication)
def send_scholarship_status_notification(sender, instance, **kwargs):
    """Send notification on scholarship application status change"""
    if instance.status in ['approved', 'rejected', 'awarded']:
        # TODO: Send email to student
        pass
