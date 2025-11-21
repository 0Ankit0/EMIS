"""
LMS Custom Managers and QuerySets
"""
from django.db import models
from django.utils import timezone


class CourseQuerySet(models.QuerySet):
    """Custom queryset for Course"""
    
    def published(self):
        """Get published courses"""
        return self.filter(status='published', publish_date__lte=timezone.now())
    
    def draft(self):
        """Get draft courses"""
        return self.filter(status='draft')
    
    def archived(self):
        """Get archived courses"""
        return self.filter(status='archived')
    
    def free(self):
        """Get free courses"""
        return self.filter(is_free=True)
    
    def paid(self):
        """Get paid courses"""
        return self.filter(is_free=False)
    
    def by_instructor(self, faculty):
        """Get courses by instructor"""
        return self.filter(instructor=faculty)


class CourseManager(models.Manager):
    """Custom manager for Course"""
    
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def draft(self):
        return self.get_queryset().draft()
    
    def archived(self):
        return self.get_queryset().archived()
    
    def free(self):
        return self.get_queryset().free()
    
    def paid(self):
        return self.get_queryset().paid()
    
    def by_instructor(self, faculty):
        return self.get_queryset().by_instructor(faculty)


class EnrollmentQuerySet(models.QuerySet):
    """Custom queryset for Enrollment"""
    
    def active(self):
        """Get active enrollments"""
        return self.filter(status='active')
    
    def completed(self):
        """Get completed enrollments"""
        return self.filter(status='completed')
    
    def by_student(self, student):
        """Get enrollments by student"""
        return self.filter(student=student)
    
    def by_course(self, course):
        """Get enrollments by course"""
        return self.filter(course=course)


class EnrollmentManager(models.Manager):
    """Custom manager for Enrollment"""
    
    def get_queryset(self):
        return EnrollmentQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def completed(self):
        return self.get_queryset().completed()
    
    def by_student(self, student):
        return self.get_queryset().by_student(student)
    
    def by_course(self, course):
        return self.get_queryset().by_course(course)
