"""
Library Models
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.core.models import TimeStampedModel
from .managers import BookManager, BookIssueManager

User = get_user_model()


class Book(TimeStampedModel):
    """
    Book model with comprehensive fields
    """

    # Book Information
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True)
    publication_year = models.IntegerField()
    edition = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=50, default='English')
    pages = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    # Category
    category = models.CharField(
        max_length=50,
        choices=[
            ('fiction', 'Fiction'),
            ('non_fiction', 'Non-Fiction'),
            ('reference', 'Reference'),
            ('textbook', 'Textbook'),
            ('journal', 'Journal'),
            ('magazine', 'Magazine'),
            ('research', 'Research Paper'),
        ]
    )
    
    # Availability
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Location
    rack_number = models.CharField(max_length=20, blank=True)
    shelf_number = models.CharField(max_length=20, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('issued', 'Issued'),
            ('maintenance', 'Under Maintenance'),
            ('lost', 'Lost'),
            ('damaged', 'Damaged'),
        ],
        default='available'
    )
    
    # Cover image
    cover_image = models.ImageField(upload_to='library/covers/', blank=True, null=True)
    
    objects = BookManager()
    
    @property
    def is_available(self):
        return self.available_copies > 0 and self.status == 'available'
    
    def issue_book(self):
        if self.is_available:
            self.available_copies -= 1
            if self.available_copies == 0:
                self.status = 'issued'
            self.save()
            return True
        return False
    
    def return_book(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            if self.available_copies > 0:
                self.status = 'available'
            self.save()
    
    class Meta:
        db_table = 'library_books'
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.isbn} - {self.title}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('library:book_detail', kwargs={'pk': self.pk})


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
