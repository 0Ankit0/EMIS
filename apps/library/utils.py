"""
Library Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Count, Q
import csv
from io import StringIO


def validate_isbn(isbn):
    """
    Validate ISBN number
    
    Args:
        isbn: ISBN string
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    isbn = isbn.strip().replace('-', '')
    if not (len(isbn) == 10 or len(isbn) == 13):
        raise ValidationError("ISBN must be 10 or 13 characters long")
    
    if not isbn.isdigit():
        raise ValidationError("ISBN must contain only digits")
    
    return True


def generate_member_id(prefix='LM'):
    """
    Generate unique library member ID
    
    Args:
        prefix: Prefix for member ID
    
    Returns:
        str: Unique member ID
    """
    from .models import LibraryMember
    
    current_year = timezone.now().year
    count = LibraryMember.objects.filter(
        member_id__startswith=f'{prefix}{current_year}'
    ).count() + 1
    
    return f'{prefix}{current_year}{count:04d}'


def calculate_fine_amount(issue, rate_per_day=5):
    """
    Calculate fine for overdue book
    
    Args:
        issue: BookIssue instance
        rate_per_day: Fine rate per day
    
    Returns:
        Decimal: Fine amount
    """
    if issue.is_overdue:
        return issue.days_overdue * rate_per_day
    return 0


def get_library_statistics():
    """
    Get comprehensive library statistics
    
    Returns:
        dict: Statistics data
    """
    from .models import Book, BookIssue, LibraryMember
    
    today = timezone.now().date()
    
    return {
        'total_books': Book.objects.count(),
        'available_books': Book.objects.available().count(),
        'issued_books': BookIssue.objects.issued().count(),
        'overdue_books': BookIssue.objects.overdue().count(),
        'total_members': LibraryMember.objects.filter(status='active').count(),
        'books_by_category': dict(Book.objects.values_list('category').annotate(count=Count('id'))),
        'books_by_status': dict(Book.objects.values_list('status').annotate(count=Count('id'))),
        'issues_this_month': BookIssue.objects.filter(
            issue_date__year=today.year,
            issue_date__month=today.month
        ).count(),
        'returns_this_month': BookIssue.objects.filter(
            return_date__year=today.year,
            return_date__month=today.month,
            status='returned'
        ).count(),
    }


def export_books_to_csv(queryset):
    """
    Export books to CSV
    
    Args:
        queryset: QuerySet of books to export
    
    Returns:
        str: CSV data
    """
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ISBN', 'Title', 'Author', 'Publisher', 'Publication Year',
        'Category', 'Total Copies', 'Available Copies', 'Status'
    ])
    
    # Write data
    for book in queryset:
        writer.writerow([
            book.isbn,
            book.title,
            book.author,
            book.publisher,
            book.publication_year,
            book.get_category_display(),
            book.total_copies,
            book.available_copies,
            book.get_status_display(),
        ])
    
    return output.getvalue()


def export_issues_to_csv(queryset):
    """
    Export book issues to CSV
    
    Args:
        queryset: QuerySet of issues to export
    
    Returns:
        str: CSV data
    """
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Book Title', 'ISBN', 'Borrower', 'Issue Date', 'Due Date',
        'Return Date', 'Status', 'Fine Amount'
    ])
    
    # Write data
    for issue in queryset:
        writer.writerow([
            issue.book.title,
            issue.book.isbn,
            issue.borrower_name,
            issue.issue_date,
            issue.due_date,
            issue.return_date or '',
            issue.get_status_display(),
            issue.fine_amount,
        ])
    
    return output.getvalue()


def check_member_eligibility(member):
    """
    Check if member is eligible to issue more books
    
    Args:
        member: LibraryMember instance
    
    Returns:
        tuple: (bool, str) - (is_eligible, message)
    """
    if not member.is_active:
        return False, "Membership is not active"
    
    if member.current_issues_count >= member.max_books_allowed:
        return False, f"Maximum book limit ({member.max_books_allowed}) reached"
    
    # Check for overdue books
    from .models import BookIssue
    overdue_count = BookIssue.objects.filter(
        Q(student=member.student) | Q(faculty=member.faculty),
        status='issued',
        due_date__lt=timezone.now().date()
    ).count()
    
    if overdue_count > 0:
        return False, f"Cannot issue books. You have {overdue_count} overdue book(s)"
    
    return True, "Eligible"


def send_overdue_reminders():
    """
    Send reminders for overdue books
    This can be called from a periodic task
    """
    from .models import BookIssue
    
    overdue_issues = BookIssue.objects.overdue()
    
    # Here you would implement email/SMS sending logic
    # For now, just return the count
    return overdue_issues.count()
