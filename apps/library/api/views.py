"""
Library API Views
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction

from .models import Book, BookIssue, LibraryMember
from .serializers import (
    BookSerializer, BookListSerializer, BookIssueSerializer, 
    LibraryMemberSerializer
)
from .filters import BookFilter, BookIssueFilter, LibraryMemberFilter
from .permissions import IsLibraryStaff, CanIssueBook


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint for books
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'isbn', 'publisher']
    ordering_fields = ['title', 'author', 'publication_year', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibraryStaff()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check book availability"""
        book = self.get_object()
        return Response({
            'is_available': book.is_available,
            'available_copies': book.available_copies,
            'total_copies': book.total_copies,
            'status': book.status,
        })
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available books"""
        books = self.queryset.available()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get books by category"""
        category = request.query_params.get('category')
        if category:
            books = self.queryset.by_category(category)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class BookIssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint for book issues
    """
    queryset = BookIssue.objects.all().select_related('book', 'student', 'faculty')
    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated, CanIssueBook]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookIssueFilter
    ordering_fields = ['issue_date', 'due_date', 'return_date']
    ordering = ['-issue_date']
    
    def perform_create(self, serializer):
        """Issue a book"""
        with transaction.atomic():
            issue = serializer.save(issued_by=self.request.user)
            issue.book.issue_book()
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Return a book"""
        issue = self.get_object()
        
        if issue.status == 'returned':
            return Response(
                {'error': 'Book already returned'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            issue.return_date = timezone.now().date()
            issue.status = 'returned'
            issue.calculate_fine()
            issue.save()
            
            issue.book.return_book()
        
        serializer = self.get_serializer(issue)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def calculate_fine(self, request, pk=None):
        """Calculate fine for overdue book"""
        issue = self.get_object()
        fine = issue.calculate_fine()
        
        return Response({
            'fine_amount': fine,
            'days_overdue': issue.days_overdue,
            'is_overdue': issue.is_overdue,
        })
    
    @action(detail=False, methods=['get'])
    def issued(self, request):
        """Get all currently issued books"""
        issues = self.queryset.issued()
        serializer = self.get_serializer(issues, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue books"""
        issues = self.queryset.overdue()
        
        # Calculate fines
        for issue in issues:
            issue.calculate_fine()
        
        serializer = self.get_serializer(issues, many=True)
        return Response(serializer.data)


class LibraryMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint for library members
    """
    queryset = LibraryMember.objects.all()
    serializer_class = LibraryMemberSerializer
    permission_classes = [IsAuthenticated, IsLibraryStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LibraryMemberFilter
    search_fields = ['member_id', 'student__user__first_name', 'faculty__user__first_name']
    ordering_fields = ['membership_date', 'expiry_date']
    ordering = ['-membership_date']
    
    @action(detail=True, methods=['get'])
    def current_issues(self, request, pk=None):
        """Get current issues for a member"""
        member = self.get_object()
        
        if member.student:
            issues = BookIssue.objects.filter(student=member.student, status='issued')
        elif member.faculty:
            issues = BookIssue.objects.filter(faculty=member.faculty, status='issued')
        else:
            issues = BookIssue.objects.none()
        
        serializer = BookIssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def can_issue(self, request, pk=None):
        """Check if member can issue more books"""
        member = self.get_object()
        
        return Response({
            'can_issue': member.can_issue_book(),
            'current_issues': member.current_issues_count,
            'max_allowed': member.max_books_allowed,
            'is_active': member.is_active,
        })
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active members"""
        members = self.queryset.filter(status='active')
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)
