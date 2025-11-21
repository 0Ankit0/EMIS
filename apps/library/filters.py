"""
Library Filters
"""
import django_filters
from .models import Book, BookIssue, LibraryMember


class BookFilter(django_filters.FilterSet):
    """
    Filter for Book
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    isbn = django_filters.CharFilter(lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    publication_year_gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year_lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'status', 'publication_year']


class BookIssueFilter(django_filters.FilterSet):
    """
    Filter for BookIssue
    """
    issue_date = django_filters.DateFromToRangeFilter()
    due_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = BookIssue
        fields = ['status', 'issue_date', 'due_date', 'fine_paid']


class LibraryMemberFilter(django_filters.FilterSet):
    """
    Filter for LibraryMember
    """
    member_id = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = LibraryMember
        fields = ['member_id', 'status']
