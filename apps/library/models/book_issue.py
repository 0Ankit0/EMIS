from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.core.models import TimeStampedModel
from .book import Book
from ..managers import BookIssueManager
from django.contrib.auth import get_user_model

User = get_user_model()

class BookIssue(TimeStampedModel):
    """
    Book Issue/Borrowing model
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='book_issues', null=True, blank=True)
    faculty = models.ForeignKey('faculty.Faculty', on_delete=models.CASCADE, related_name='book_issues', null=True, blank=True)
    
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_paid = models.BooleanField(default=False)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('issued', 'Issued'),
            ('returned', 'Returned'),
            ('overdue', 'Overdue'),
            ('lost', 'Lost'),
        ],
        default='issued'
    )
    
    notes = models.TextField(blank=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_books')
    
    objects = BookIssueManager()
    
    @property
    def is_overdue(self):
        if self.status != 'returned' and self.due_date < timezone.now().date():
            return True
        return False
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (timezone.now().date() - self.due_date).days
        return 0
    
    def calculate_fine(self, rate_per_day=5):
        if self.is_overdue:
            self.fine_amount = self.days_overdue * rate_per_day
            self.save()
        return self.fine_amount
    
    @property
    def borrower_name(self):
        if self.student:
            return self.student.user.get_full_name()
        elif self.faculty:
            return self.faculty.user.get_full_name()
        return "Unknown"
    
    class Meta:
        db_table = 'library_book_issues'
        ordering = ['-issue_date']
        verbose_name = 'Book Issue'
        verbose_name_plural = 'Book Issues'
        indexes = [
            models.Index(fields=['issue_date']),
            models.Index(fields=['due_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.book.title} - {self.borrower_name}"
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=14)
        super().save(*args, **kwargs)
