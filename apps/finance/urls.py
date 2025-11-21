"""Finance URL Configuration"""
from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Invoices
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<uuid:pk>/', views.invoice_detail, name='invoice_detail'),
    
    # Payments
    path('payments/create/', views.payment_create, name='payment_create'),
    
    # Expenses
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    
    # Scholarships
    path('scholarships/', views.scholarship_list, name='scholarship_list'),
    
    # Export
    path('export/invoices/csv/', views.export_invoices_csv, name='export_invoices_csv'),
]
