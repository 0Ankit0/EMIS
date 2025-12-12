"""
Library API Filters
"""
import django_filters
from ..models import Book, BookIssue, LibraryMember


class BookFilter(django_filters.FilterSet):
    """Filter for Book model"""
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    isbn = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    publisher = django_filters.CharFilter(lookup_expr='icontains')
    is_available = django_filters.BooleanFilter()
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'publisher', 'is_available']


class BookIssueFilter(django_filters.FilterSet):
    """Filter for BookIssue model"""
    book = django_filters.NumberFilter(field_name='book__id')
    member = django_filters.NumberFilter(field_name='member__id')
    status = django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = BookIssue
        fields = ['book', 'member', 'status']


class LibraryMemberFilter(django_filters.FilterSet):
    """Filter for LibraryMember model"""
    user = django_filters.NumberFilter(field_name='user__id')
    member_type = django_filters.CharFilter(lookup_expr='exact')
    is_active = django_filters.BooleanFilter()
    
    class Meta:
        model = LibraryMember
        fields = ['user', 'member_type', 'is_active']
