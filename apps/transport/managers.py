"""
Transport Custom Managers and QuerySets
"""
from django.db import models


class VehicleQuerySet(models.QuerySet):
    """Custom queryset for Vehicle"""
    
    def active(self):
        """Get only active vehicles"""
        return self.filter(status='active')
    
    def available(self):
        """Get vehicles not under maintenance"""
        return self.exclude(status='maintenance')
    
    def by_type(self, vehicle_type):
        """Get vehicles by type"""
        return self.filter(vehicle_type=vehicle_type)


class VehicleManager(models.Manager):
    """Custom manager for Vehicle"""
    
    def get_queryset(self):
        return VehicleQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def available(self):
        return self.get_queryset().available()
    
    def by_type(self, vehicle_type):
        return self.get_queryset().by_type(vehicle_type)


class DriverQuerySet(models.QuerySet):
    """Custom queryset for Driver"""
    
    def active(self):
        """Get only active drivers"""
        return self.filter(employment_status='active')
    
    def available(self):
        """Get drivers not on leave"""
        return self.exclude(employment_status__in=['on_leave', 'suspended'])


class DriverManager(models.Manager):
    """Custom manager for Driver"""
    
    def get_queryset(self):
        return DriverQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def available(self):
        return self.get_queryset().available()


class RouteQuerySet(models.QuerySet):
    """Custom queryset for Route"""
    
    def active(self):
        """Get only active routes"""
        return self.filter(is_active=True)
    
    def for_day(self, day_name):
        """Get routes operating on a specific day"""
        day_field = f'operates_{day_name.lower()}'
        return self.filter(**{day_field: True})


class RouteManager(models.Manager):
    """Custom manager for Route"""
    
    def get_queryset(self):
        return RouteQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def for_day(self, day_name):
        return self.get_queryset().for_day(day_name)
