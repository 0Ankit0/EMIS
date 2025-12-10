"""HR Signals"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Leave, Payroll, PerformanceReview

@receiver(post_save, sender=Leave)
def update_employee_status_on_leave(sender, instance, **kwargs):
    """Update employee status when leave is approved"""
    if instance.status == 'approved':
        today = timezone.now().date()
        if instance.start_date <= today <= instance.end_date:
            instance.employee.status = 'on_leave'
            instance.employee.save(update_fields=['status'])
        
        # TODO: Send notification to employee
        pass

@receiver(post_save, sender=Leave)
def notify_leave_status_change(sender, instance, created, **kwargs):
    """Send notification when leave status changes"""
    if not created and instance.status in ['approved', 'rejected']:
        # TODO: Send email/SMS notification
        pass

@receiver(pre_save, sender=PerformanceReview)
def calculate_overall_rating_on_save(sender, instance, **kwargs):
    """Calculate overall rating before saving review"""
    instance.overall_rating = instance.calculate_overall_rating()

@receiver(post_save, sender=Payroll)
def notify_payroll_processed(sender, instance, created, **kwargs):
    """Send notification when payroll is processed"""
    if instance.status == 'paid':
        # TODO: Send payslip to employee
        pass
