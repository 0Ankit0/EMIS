from django.db import models
from apps.core.models import TimeStampedModel
from .faculty import Faculty

class FacultyPublication(TimeStampedModel):
    """Research Publications by Faculty"""
    class PublicationType(models.TextChoices):
        JOURNAL = 'journal', 'Journal Article'
        CONFERENCE = 'conference', 'Conference Paper'
        BOOK = 'book', 'Book'
        CHAPTER = 'chapter', 'Book Chapter'
        PATENT = 'patent', 'Patent'
        OTHER = 'other', 'Other'
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=500)
    publication_type = models.CharField(max_length=20, choices=PublicationType.choices)
    authors = models.TextField(help_text="Comma separated list of authors")
    journal_or_conference = models.CharField(max_length=300)
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    year = models.IntegerField()
    doi = models.CharField(max_length=200, blank=True, verbose_name='DOI')
    isbn_issn = models.CharField(max_length=50, blank=True, verbose_name='ISBN/ISSN')
    url = models.URLField(blank=True)
    abstract = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    citation_count = models.IntegerField(default=0)
    impact_factor = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    is_indexed = models.BooleanField(default=False, help_text="Indexed in Scopus/Web of Science")
    document = models.FileField(upload_to='faculty/publications/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'faculty_publications'
        ordering = ['-year', '-created_at']
        verbose_name = 'Faculty Publication'
        verbose_name_plural = 'Faculty Publications'
    
    def __str__(self):
        return f"{self.title[:50]} - {self.year}"

