"""
Library Admin Configuration
"""
from django.contrib import admin
from .models import Book, BookIssue, LibraryMember


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book
    """
    list_display = ['isbn', 'title', 'author', 'category', 'total_copies', 'available_copies', 'status']
    list_filter = ['status', 'category', 'publication_year']
    search_fields = ['isbn', 'title', 'author', 'publisher']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 50
    
    fieldsets = (
        ('Book Information', {
            'fields': ('isbn', 'title', 'author', 'publisher', 'publication_year', 'edition', 'language', 'pages', 'description', 'cover_image')
        }),
        ('Category', {
            'fields': ('category',)
        }),
        ('Availability', {
            'fields': ('total_copies', 'available_copies', 'price', 'status')
        }),
        ('Location', {
            'fields': ('rack_number', 'shelf_number', 'floor')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_available', 'mark_as_maintenance']
    
    def mark_as_available(self, request, queryset):
        queryset.update(status='available')
    mark_as_available.short_description = "Mark selected books as available"
    
    def mark_as_maintenance(self, request, queryset):
        queryset.update(status='maintenance')
    mark_as_maintenance.short_description = "Mark selected books as under maintenance"


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    """
    Admin interface for BookIssue
    """
    list_display = ['book', 'borrower_name', 'issue_date', 'due_date', 'return_date', 'status', 'fine_amount']
    list_filter = ['status', 'issue_date', 'due_date', 'fine_paid']
    search_fields = ['book__title', 'book__isbn', 'student__user__first_name', 'faculty__user__first_name']
    readonly_fields = ['created_at', 'updated_at', 'is_overdue', 'days_overdue']
    date_hierarchy = 'issue_date'
    ordering = ['-issue_date']
    list_per_page = 50
    
    fieldsets = (
        ('Book & Borrower', {
            'fields': ('book', 'student', 'faculty')
        }),
        ('Issue Details', {
            'fields': ('issue_date', 'due_date', 'return_date', 'status')
        }),
        ('Fine Details', {
            'fields': ('fine_amount', 'fine_paid')
        }),
        ('Additional Info', {
            'fields': ('notes', 'issued_by')
        }),
        ('Status Info', {
            'fields': ('is_overdue', 'days_overdue'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_returned', 'calculate_fines']
    
    def mark_as_returned(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='returned', return_date=timezone.now().date())
    mark_as_returned.short_description = "Mark selected issues as returned"
    
    def calculate_fines(self, request, queryset):
        for issue in queryset:
            issue.calculate_fine()
    calculate_fines.short_description = "Calculate fines for selected issues"


@admin.register(LibraryMember)
class LibraryMemberAdmin(admin.ModelAdmin):
    """
    Admin interface for LibraryMember
    """
    list_display = ['member_id', 'member_name', 'membership_date', 'expiry_date', 'status', 'max_books_allowed']
    list_filter = ['status', 'membership_date', 'expiry_date']
    search_fields = ['member_id', 'student__user__first_name', 'faculty__user__first_name']
    readonly_fields = ['created_at', 'updated_at', 'is_active', 'current_issues_count']
    date_hierarchy = 'membership_date'
    ordering = ['-membership_date']
    
    fieldsets = (
        ('Member Info', {
            'fields': ('student', 'faculty', 'member_id')
        }),
        ('Membership Details', {
            'fields': ('membership_date', 'expiry_date', 'status', 'max_books_allowed')
        }),
        ('Status', {
            'fields': ('is_active', 'current_issues_count'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

