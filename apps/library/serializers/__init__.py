"""
Library Serializers
"""
from rest_framework import serializers
from ..models import Book, BookIssue, LibraryMember


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book
    """
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'isbn', 'title', 'author', 'publisher', 'publication_year',
            'edition', 'language', 'pages', 'description', 'category',
            'total_copies', 'available_copies', 'price', 'rack_number',
            'shelf_number', 'floor', 'status', 'cover_image', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_available']
    
    def validate_isbn(self, value):
        """Validate ISBN field"""
        value = value.strip().replace('-', '')
        if not (len(value) == 10 or len(value) == 13):
            raise serializers.ValidationError("ISBN must be 10 or 13 characters long")
        return value


class BookListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing books
    """
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'category', 'available_copies', 'status']


class BookIssueSerializer(serializers.ModelSerializer):
    """
    Serializer for BookIssue
    """
    book_title = serializers.CharField(source='book.title', read_only=True)
    borrower_name = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = BookIssue
        fields = [
            'id', 'book', 'book_title', 'student', 'faculty', 'borrower_name',
            'issue_date', 'due_date', 'return_date', 'fine_amount', 'fine_paid',
            'status', 'notes', 'issued_by', 'is_overdue', 'days_overdue',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_overdue', 'days_overdue']


class LibraryMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for LibraryMember
    """
    member_name = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    current_issues_count = serializers.ReadOnlyField()
    
    class Meta:
        model = LibraryMember
        fields = [
            'id', 'student', 'faculty', 'member_id', 'member_name',
            'membership_date', 'expiry_date', 'status', 'max_books_allowed',
            'notes', 'is_active', 'current_issues_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_active', 'current_issues_count']
