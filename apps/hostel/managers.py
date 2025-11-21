"""Hostel Custom Managers"""
from django.db import models
from django.utils import timezone


class HostelQuerySet(models.QuerySet):
    """Custom queryset for Hostel"""
    
    def active(self):
        return self.filter(status='active', is_active=True)
    
    def boys_hostels(self):
        return self.filter(hostel_type='boys', is_active=True)
    
    def girls_hostels(self):
        return self.filter(hostel_type='girls', is_active=True)
    
    def with_vacancy(self):
        return self.filter(occupied_capacity__lt=models.F('total_capacity'), is_active=True)


class HostelManager(models.Manager):
    def get_queryset(self):
        return HostelQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def boys_hostels(self):
        return self.get_queryset().boys_hostels()
    
    def girls_hostels(self):
        return self.get_queryset().girls_hostels()
    
    def with_vacancy(self):
        return self.get_queryset().with_vacancy()


class RoomQuerySet(models.QuerySet):
    """Custom queryset for Room"""
    
    def available(self):
        return self.filter(status='available', occupied_beds__lt=models.F('capacity'))
    
    def full(self):
        return self.filter(status='full')
    
    def under_maintenance(self):
        return self.filter(status='maintenance')
    
    def by_type(self, room_type):
        return self.filter(room_type=room_type)
    
    def with_ac(self):
        return self.filter(has_ac=True)
    
    def with_vacancy(self):
        return self.filter(occupied_beds__lt=models.F('capacity'))


class RoomManager(models.Manager):
    def get_queryset(self):
        return RoomQuerySet(self.model, using=self._db)
    
    def available(self):
        return self.get_queryset().available()
    
    def full(self):
        return self.get_queryset().full()
    
    def with_vacancy(self):
        return self.get_queryset().with_vacancy()


class RoomAllocationQuerySet(models.QuerySet):
    """Custom queryset for RoomAllocation"""
    
    def active(self):
        return self.filter(status='active')
    
    def vacated(self):
        return self.filter(status='vacated')
    
    def for_academic_year(self, year):
        return self.filter(academic_year=year)


class RoomAllocationManager(models.Manager):
    def get_queryset(self):
        return RoomAllocationQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def vacated(self):
        return self.get_queryset().vacated()


class ComplaintQuerySet(models.QuerySet):
    """Custom queryset for Complaint"""
    
    def pending(self):
        return self.filter(status__in=['submitted', 'acknowledged', 'in_progress'])
    
    def resolved(self):
        return self.filter(status='resolved')
    
    def urgent(self):
        return self.filter(priority='urgent')
    
    def by_category(self, category):
        return self.filter(category=category)


class ComplaintManager(models.Manager):
    def get_queryset(self):
        return ComplaintQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def resolved(self):
        return self.get_queryset().resolved()
    
    def urgent(self):
        return self.get_queryset().urgent()


class OutingRequestQuerySet(models.QuerySet):
    """Custom queryset for OutingRequest"""
    
    def pending(self):
        return self.filter(status='pending')
    
    def approved(self):
        return self.filter(status='approved')
    
    def currently_out(self):
        today = timezone.now().date()
        return self.filter(
            status='approved',
            out_date__lte=today,
            expected_return_date__gte=today
        )


class OutingRequestManager(models.Manager):
    def get_queryset(self):
        return OutingRequestQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def approved(self):
        return self.get_queryset().approved()
    
    def currently_out(self):
        return self.get_queryset().currently_out()
