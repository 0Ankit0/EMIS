"""Finance Custom Managers"""
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone


class InvoiceQuerySet(models.QuerySet):
    """Custom queryset for Invoice"""
    
    def pending(self):
        return self.filter(status='pending')
    
    def paid(self):
        return self.filter(status='paid')
    
    def overdue(self):
        return self.filter(status='overdue')
    
    def partial(self):
        return self.filter(status='partial')
    
    def for_academic_year(self, year):
        return self.filter(academic_year=year)


class InvoiceManager(models.Manager):
    def get_queryset(self):
        return InvoiceQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def paid(self):
        return self.get_queryset().paid()
    
    def overdue(self):
        return self.get_queryset().overdue()


class ExpenseQuerySet(models.QuerySet):
    """Custom queryset for Expense"""
    
    def pending(self):
        return self.filter(status='pending')
    
    def approved(self):
        return self.filter(status='approved')
    
    def paid(self):
        return self.filter(status='paid')
    
    def by_category(self, category):
        return self.filter(category=category)


class ExpenseManager(models.Manager):
    def get_queryset(self):
        return ExpenseQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def approved(self):
        return self.get_queryset().approved()
    
    def paid(self):
        return self.get_queryset().paid()


class ScholarshipQuerySet(models.QuerySet):
    """Custom queryset for Scholarship"""
    
    def active(self):
        return self.filter(status='active')
    
    def open_for_application(self):
        today = timezone.now().date()
        return self.filter(
            status='active',
            application_start_date__lte=today,
            application_end_date__gte=today
        )


class ScholarshipManager(models.Manager):
    def get_queryset(self):
        return ScholarshipQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def open_for_application(self):
        return self.get_queryset().open_for_application()
