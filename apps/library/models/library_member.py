from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.core.models import TimeStampedModel
from .book_issue import BookIssue

class LibraryMember(TimeStampedModel):
    """
    Library membership model
    """
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, null=True, blank=True, related_name='library_member')
    faculty = models.OneToOneField('faculty.Faculty', on_delete=models.CASCADE, null=True, blank=True, related_name='library_member')
    
    member_id = models.CharField(max_length=20, unique=True)
    membership_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('suspended', 'Suspended'),
            ('expired', 'Expired'),
        ],
        default='active'
    )
    
    max_books_allowed = models.IntegerField(default=3)
    notes = models.TextField(blank=True)
    
    @property
    def is_active(self):
        return self.status == 'active' and self.expiry_date >= timezone.now().date()
    
    @property
    def member_name(self):
        if self.student:
            return self.student.user.get_full_name()
        elif self.faculty:
            return self.faculty.user.get_full_name()
        return "Unknown"
    
    @property
    def current_issues_count(self):
        if self.student:
            return BookIssue.objects.filter(student=self.student, status='issued').count()
        elif self.faculty:
            return BookIssue.objects.filter(faculty=self.faculty, status='issued').count()
        return 0
    
    def can_issue_book(self):
        return self.is_active and self.current_issues_count < self.max_books_allowed
    
    class Meta:
        db_table = 'library_members'
        ordering = ['-membership_date']
        verbose_name = 'Library Member'
        verbose_name_plural = 'Library Members'
    
    def __str__(self):
        return f"{self.member_id} - {self.member_name}"
    
    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = self.membership_date + timedelta(days=365)
        super().save(*args, **kwargs)
