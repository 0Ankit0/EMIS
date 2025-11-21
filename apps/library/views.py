"""
Library Views - Complete Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import csv
from datetime import timedelta

from .models import Book, BookIssue, LibraryMember
from .forms import BookForm, BookIssueForm, BookReturnForm, LibraryMemberForm, BookSearchForm


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """Library dashboard with statistics"""
    total_books = Book.objects.count()
    available_books = Book.objects.available().count()
    issued_books = BookIssue.objects.issued().count()
    overdue_books = BookIssue.objects.overdue().count()
    total_members = LibraryMember.objects.filter(status='active').count()
    
    recent_issues = BookIssue.objects.select_related('book').order_by('-created_at')[:5]
    popular_books = Book.objects.annotate(issue_count=Count('issues')).order_by('-issue_count')[:5]
    
    context = {
        'total_books': total_books,
        'available_books': available_books,
        'issued_books': issued_books,
        'overdue_books': overdue_books,
        'total_members': total_members,
        'recent_issues': recent_issues,
        'popular_books': popular_books,
    }
    
    return render(request, 'library/dashboard.html', context)


# ============================================================================
# Book Views
# ============================================================================

@login_required
def books_catalog(request):
    """List all books with search and filters"""
    books = Book.objects.all()
    form = BookSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(isbn__icontains=query)
            )
        if category:
            books = books.filter(category=category)
        if status:
            books = books.filter(status=status)
    
    paginator = Paginator(books, 20)
    page = request.GET.get('page')
    books_page = paginator.get_page(page)
    
    context = {
        'books': books_page,
        'form': form,
    }
    
    return render(request, 'library/books_catalog.html', context)


@login_required
def book_detail(request, pk):
    """View single book details"""
    book = get_object_or_404(Book, pk=pk)
    recent_issues = book.issues.order_by('-issue_date')[:10]
    
    context = {
        'book': book,
        'recent_issues': recent_issues,
    }
    
    return render(request, 'library/book_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def add_book(request):
    """Add new book"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                book = form.save()
                messages.success(request, f'Book "{book.title}" added successfully!')
                return redirect('library:book_detail', pk=book.pk)
            except Exception as e:
                messages.error(request, f'Error adding book: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'action': 'Add',
    }
    
    return render(request, 'library/add_book.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_book(request, pk):
    """Edit existing book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            try:
                book = form.save()
                messages.success(request, f'Book "{book.title}" updated successfully!')
                return redirect('library:book_detail', pk=book.pk)
            except Exception as e:
                messages.error(request, f'Error updating book: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'action': 'Edit',
    }
    
    return render(request, 'library/add_book.html', context)


@login_required
@require_http_methods(["POST"])
def delete_book(request, pk):
    """Delete book"""
    book = get_object_or_404(Book, pk=pk)
    
    try:
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('library:books_catalog')
    except Exception as e:
        messages.error(request, f'Error deleting book: {str(e)}')
        return redirect('library:book_detail', pk=pk)


# ============================================================================
# Issue/Return Views
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def issue_book(request):
    """Issue book to student or faculty"""
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    issue = form.save(commit=False)
                    issue.issued_by = request.user
                    issue.save()
                    
                    issue.book.issue_book()
                    
                    messages.success(request, f'Book "{issue.book.title}" issued successfully to {issue.borrower_name}!')
                    return redirect('library:issued_books')
            except Exception as e:
                messages.error(request, f'Error issuing book: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookIssueForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'library/issue_book.html', context)


@login_required
def issued_books(request):
    """List all currently issued books"""
    issues = BookIssue.objects.issued().select_related('book', 'student', 'faculty').order_by('-issue_date')
    
    search = request.GET.get('search')
    if search:
        issues = issues.filter(
            Q(book__title__icontains=search) |
            Q(book__isbn__icontains=search) |
            Q(student__user__first_name__icontains=search) |
            Q(faculty__user__first_name__icontains=search)
        )
    
    paginator = Paginator(issues, 20)
    page = request.GET.get('page')
    issues_page = paginator.get_page(page)
    
    context = {
        'issues': issues_page,
        'search': search,
    }
    
    return render(request, 'library/issued_books.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def return_book(request, pk=None):
    """Return issued book"""
    if pk:
        issue = get_object_or_404(BookIssue, pk=pk, status='issued')
        
        if request.method == 'POST':
            form = BookReturnForm(request.POST, instance=issue)
            
            if form.is_valid():
                try:
                    with transaction.atomic():
                        issue = form.save(commit=False)
                        issue.status = 'returned'
                        issue.save()
                        
                        issue.book.return_book()
                        
                        messages.success(request, f'Book "{issue.book.title}" returned successfully!')
                        return redirect('library:issued_books')
                except Exception as e:
                    messages.error(request, f'Error returning book: {str(e)}')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = BookReturnForm(instance=issue)
        
        context = {
            'form': form,
            'issue': issue,
        }
        
        return render(request, 'library/return_book.html', context)
    else:
        issues = BookIssue.objects.issued().select_related('book')
        
        context = {
            'issues': issues,
        }
        
        return render(request, 'library/return_book_select.html', context)


@login_required
def overdue(request):
    """List all overdue books"""
    overdue_issues = BookIssue.objects.overdue().select_related('book', 'student', 'faculty').order_by('due_date')
    
    for issue in overdue_issues:
        issue.calculate_fine()
    
    context = {
        'overdue_issues': overdue_issues,
    }
    
    return render(request, 'library/overdue.html', context)


# ============================================================================
# Reports Views
# ============================================================================

@login_required
def reports(request):
    """Library reports"""
    today = timezone.now().date()
    
    stats = {
        'total_books': Book.objects.count(),
        'available_books': Book.objects.available().count(),
        'issued_books': BookIssue.objects.issued().count(),
        'overdue_books': BookIssue.objects.overdue().count(),
        'total_members': LibraryMember.objects.filter(status='active').count(),
        'books_by_category': Book.objects.values('category').annotate(count=Count('id')),
        'books_by_status': Book.objects.values('status').annotate(count=Count('id')),
        'issues_this_month': BookIssue.objects.filter(
            issue_date__year=today.year,
            issue_date__month=today.month
        ).count(),
    }
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'library/reports.html', context)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_books_csv(request):
    """Export books to CSV"""
    books = Book.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="books_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ISBN', 'Title', 'Author', 'Publisher', 'Year', 'Category', 'Total Copies', 'Available', 'Status'])
    
    for book in books:
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
    
    return response


@login_required
def export_issues_csv(request):
    """Export issues to CSV"""
    issues = BookIssue.objects.all().select_related('book', 'student', 'faculty')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="issues_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Book Title', 'ISBN', 'Borrower', 'Issue Date', 'Due Date', 'Return Date', 'Status', 'Fine'])
    
    for issue in issues:
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
    
    return response


# ============================================================================
# AJAX Operations
# ============================================================================

@login_required
def book_availability(request, pk):
    """Check book availability (AJAX)"""
    book = get_object_or_404(Book, pk=pk)
    
    data = {
        'is_available': book.is_available,
        'available_copies': book.available_copies,
        'total_copies': book.total_copies,
        'status': book.status,
    }
    
    return JsonResponse(data)


@login_required
def calculate_fine_ajax(request, pk):
    """Calculate fine for overdue book (AJAX)"""
    issue = get_object_or_404(BookIssue, pk=pk)
    fine = issue.calculate_fine()
    
    data = {
        'fine_amount': str(fine),
        'days_overdue': issue.days_overdue,
        'is_overdue': issue.is_overdue,
    }
    
    return JsonResponse(data)
