from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from ..managers import BookManager

class Book(TimeStampedModel):
    """
    Book model with comprehensive fields
    """
    class Category(models.TextChoices):
        FICTION = 'fiction', 'Fiction'
        NON_FICTION = 'non_fiction', 'Non-Fiction'
        REFERENCE = 'reference', 'Reference'
        TEXTBOOK = 'textbook', 'Textbook'
        JOURNAL = 'journal', 'Journal'
        MAGAZINE = 'magazine', 'Magazine'
        RESEARCH = 'research', 'Research Paper'

    class BookStatus(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        ISSUED = 'issued', 'Issued'
        MAINTENANCE = 'maintenance', 'Under Maintenance'
        LOST = 'lost', 'Lost'
        DAMAGED = 'damaged', 'Damaged'

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
        choices=Category.choices
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
        choices=BookStatus.choices,
        default=BookStatus.AVAILABLE
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
