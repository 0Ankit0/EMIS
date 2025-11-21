"""HR Custom Managers"""
from django.db import models
from django.utils import timezone


class EmployeeQuerySet(models.QuerySet):
    """Custom queryset for Employee"""
    
    def active(self):
        return self.filter(status='active')
    
    def on_leave(self):
        return self.filter(status='on_leave')
    
    def full_time(self):
        return self.filter(employment_type='full_time')
    
    def part_time(self):
        return self.filter(employment_type='part_time')
    
    def by_department(self, department):
        return self.filter(department=department)
    
    def by_designation(self, designation):
        return self.filter(designation=designation)


class EmployeeManager(models.Manager):
    def get_queryset(self):
        return EmployeeQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def on_leave(self):
        return self.get_queryset().on_leave()
    
    def full_time(self):
        return self.get_queryset().full_time()


class LeaveQuerySet(models.QuerySet):
    """Custom queryset for Leave"""
    
    def pending(self):
        return self.filter(status='pending')
    
    def approved(self):
        return self.filter(status='approved')
    
    def rejected(self):
        return self.filter(status='rejected')
    
    def for_employee(self, employee):
        return self.filter(employee=employee)


class LeaveManager(models.Manager):
    def get_queryset(self):
        return LeaveQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def approved(self):
        return self.get_queryset().approved()


class PayrollQuerySet(models.QuerySet):
    """Custom queryset for Payroll"""
    
    def draft(self):
        return self.filter(status='draft')
    
    def processed(self):
        return self.filter(status='processed')
    
    def paid(self):
        return self.filter(status='paid')
    
    def for_month(self, month, year):
        return self.filter(month=month, year=year)


class PayrollManager(models.Manager):
    def get_queryset(self):
        return PayrollQuerySet(self.model, using=self._db)
    
    def draft(self):
        return self.get_queryset().draft()
    
    def processed(self):
        return self.get_queryset().processed()
    
    def paid(self):
        return self.get_queryset().paid()


class JobPostingQuerySet(models.QuerySet):
    """Custom queryset for JobPosting"""
    
    def open(self):
        return self.filter(status='open')
    
    def closed(self):
        return self.filter(status='closed')
    
    def active(self):
        today = timezone.now().date()
        return self.filter(
            models.Q(closing_date__isnull=True) | models.Q(closing_date__gte=today),
            status='open'
        )


class JobPostingManager(models.Manager):
    def get_queryset(self):
        return JobPostingQuerySet(self.model, using=self._db)
    
    def open(self):
        return self.get_queryset().open()
    
    def active(self):
        return self.get_queryset().active()


class JobApplicationQuerySet(models.QuerySet):
    """Custom queryset for JobApplication"""
    
    def submitted(self):
        return self.filter(status='submitted')
    
    def shortlisted(self):
        return self.filter(status='shortlisted')
    
    def selected(self):
        return self.filter(status='selected')
    
    def rejected(self):
        return self.filter(status='rejected')


class JobApplicationManager(models.Manager):
    def get_queryset(self):
        return JobApplicationQuerySet(self.model, using=self._db)
    
    def submitted(self):
        return self.get_queryset().submitted()
    
    def shortlisted(self):
        return self.get_queryset().shortlisted()
