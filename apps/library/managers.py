"""
Library Custom Managers and QuerySets
"""
from django.db import models
from django.utils import timezone


class BookQuerySet(models.QuerySet):
    """Custom queryset for Book"""
    
    def available(self):
        """Get only available books"""
        return self.filter(status='available', available_copies__gt=0)
    
    def issued(self):
        """Get only issued books"""
        return self.filter(status='issued')
    
    def maintenance(self):
        """Get books under maintenance"""
        return self.filter(status='maintenance')
    
    def by_category(self, category):
        """Get books by category"""
        return self.filter(category=category)
    
    def search(self, query):
        """Search books by title, author, isbn"""
        return self.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(isbn__icontains=query)
        )


class BookManager(models.Manager):
    """Custom manager for Book"""
    
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)
    
    def available(self):
        return self.get_queryset().available()
    
    def issued(self):
        return self.get_queryset().issued()
    
    def maintenance(self):
        return self.get_queryset().maintenance()
    
    def by_category(self, category):
        return self.get_queryset().by_category(category)
    
    def search(self, query):
        return self.get_queryset().search(query)


class BookIssueQuerySet(models.QuerySet):
    """Custom queryset for BookIssue"""
    
    def issued(self):
        """Get currently issued books"""
        return self.filter(status='issued')
    
    def returned(self):
        """Get returned books"""
        return self.filter(status='returned')
    
    def overdue(self):
        """Get overdue books"""
        return self.filter(
            status='issued',
            due_date__lt=timezone.now().date()
        )
    
    def by_student(self, student):
        """Get issues by student"""
        return self.filter(student=student)
    
    def by_faculty(self, faculty):
        """Get issues by faculty"""
        return self.filter(faculty=faculty)


class BookIssueManager(models.Manager):
    """Custom manager for BookIssue"""
    
    def get_queryset(self):
        return BookIssueQuerySet(self.model, using=self._db)
    
    def issued(self):
        return self.get_queryset().issued()
    
    def returned(self):
        return self.get_queryset().returned()
    
    def overdue(self):
        return self.get_queryset().overdue()
    
    def by_student(self, student):
        return self.get_queryset().by_student(student)
    
    def by_faculty(self, faculty):
        return self.get_queryset().by_faculty(faculty)
