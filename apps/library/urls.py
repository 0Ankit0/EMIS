"""
Library URL Configuration
"""
from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Books
    path('books/', views.books_catalog, name='books_catalog'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # Issue/Return
    path('issue/', views.issue_book, name='issue_book'),
    path('issued/', views.issued_books, name='issued_books'),
    path('return/', views.return_book, name='return_book'),
    path('return/<int:pk>/', views.return_book, name='return_book_detail'),
    path('overdue/', views.overdue, name='overdue'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # Export
    path('export/books/', views.export_books_csv, name='export_books'),
    path('export/issues/', views.export_issues_csv, name='export_issues'),
    
    # AJAX
    path('ajax/book/<int:pk>/availability/', views.book_availability, name='book_availability'),
    path('ajax/issue/<int:pk>/fine/', views.calculate_fine_ajax, name='calculate_fine'),
]
