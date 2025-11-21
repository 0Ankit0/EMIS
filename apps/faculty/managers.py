"""
Faculty Custom Managers and QuerySets
"""
from django.db import models
from django.utils import timezone
from django.db.models import Q, Count, Avg


class FacultyQuerySet(models.QuerySet):
    """Custom queryset for Faculty"""
    
    def active(self):
        """Get only active faculty"""
        return self.filter(status='active')
    
    def on_leave(self):
        """Get faculty on leave"""
        return self.filter(status='on_leave')
    
    def teaching(self):
        """Get teaching faculty"""
        return self.filter(is_teaching=True, status='active')
    
    def research_active(self):
        """Get research active faculty"""
        return self.filter(is_research_active=True, status='active')
    
    def by_department(self, department):
        """Get faculty by department"""
        return self.filter(department=department)
    
    def hods(self):
        """Get all HODs"""
        return self.filter(is_hod=True, status='active')
    
    def available_for_teaching(self):
        """Get faculty available for additional teaching load"""
        return self.filter(
            status='active',
            is_teaching=True,
            current_weekly_hours__lt=models.F('max_weekly_hours')
        )
    
    def by_designation(self, designation):
        """Get faculty by designation"""
        return self.filter(designation=designation)
    
    def full_time(self):
        """Get full-time faculty"""
        return self.filter(employment_type='full_time')
    
    def part_time(self):
        """Get part-time faculty"""
        return self.filter(employment_type='part_time')
    
    def with_qualifications(self):
        """Get faculty with qualifications count"""
        return self.annotate(qualifications_count=Count('qualifications'))
    
    def with_publications(self):
        """Get faculty with publications count"""
        return self.annotate(publications_count_annotated=Count('publications'))


class FacultyManager(models.Manager):
    """Custom manager for Faculty"""
    
    def get_queryset(self):
        return FacultyQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def on_leave(self):
        return self.get_queryset().on_leave()
    
    def teaching(self):
        return self.get_queryset().teaching()
    
    def research_active(self):
        return self.get_queryset().research_active()
    
    def by_department(self, department):
        return self.get_queryset().by_department(department)
    
    def hods(self):
        return self.get_queryset().hods()
    
    def available_for_teaching(self):
        return self.get_queryset().available_for_teaching()
    
    def by_designation(self, designation):
        return self.get_queryset().by_designation(designation)
    
    def full_time(self):
        return self.get_queryset().full_time()
    
    def part_time(self):
        return self.get_queryset().part_time()


class FacultyQualificationQuerySet(models.QuerySet):
    """Custom queryset for FacultyQualification"""
    
    def verified(self):
        """Get verified qualifications"""
        return self.filter(is_verified=True)
    
    def phd(self):
        """Get PhD qualifications"""
        return self.filter(degree='phd')
    
    def masters(self):
        """Get Masters qualifications"""
        return self.filter(degree='masters')
    
    def by_faculty(self, faculty):
        """Get qualifications by faculty"""
        return self.filter(faculty=faculty)


class FacultyQualificationManager(models.Manager):
    """Custom manager for FacultyQualification"""
    
    def get_queryset(self):
        return FacultyQualificationQuerySet(self.model, using=self._db)
    
    def verified(self):
        return self.get_queryset().verified()
    
    def phd(self):
        return self.get_queryset().phd()
    
    def masters(self):
        return self.get_queryset().masters()
    
    def by_faculty(self, faculty):
        return self.get_queryset().by_faculty(faculty)


class FacultyExperienceQuerySet(models.QuerySet):
    """Custom queryset for FacultyExperience"""
    
    def current(self):
        """Get current experiences"""
        return self.filter(is_current=True)
    
    def teaching(self):
        """Get teaching experiences"""
        return self.filter(experience_type='teaching')
    
    def research(self):
        """Get research experiences"""
        return self.filter(experience_type='research')
    
    def industry(self):
        """Get industry experiences"""
        return self.filter(experience_type='industry')


class FacultyExperienceManager(models.Manager):
    """Custom manager for FacultyExperience"""
    
    def get_queryset(self):
        return FacultyExperienceQuerySet(self.model, using=self._db)
    
    def current(self):
        return self.get_queryset().current()
    
    def teaching(self):
        return self.get_queryset().teaching()
    
    def research(self):
        return self.get_queryset().research()
    
    def industry(self):
        return self.get_queryset().industry()
