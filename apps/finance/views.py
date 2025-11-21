"""Finance Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.utils import timezone
import csv

from .models import (
    FeeStructure, Invoice, Payment, ExpenseCategory, Expense,
    Budget, BudgetAllocation, Scholarship, ScholarshipApplication
)
from .forms import (
    FeeStructureForm, InvoiceForm, PaymentForm, ExpenseForm,
    BudgetForm, ScholarshipForm, ScholarshipApplicationForm
)


@login_required
def dashboard(request):
    """Finance dashboard"""
    stats = {
        'total_revenue': Invoice.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0,
        'pending_amount': Invoice.objects.filter(status='pending').aggregate(Sum('amount_due'))['amount_due__sum'] or 0,
        'total_expenses': Expense.objects.filter(status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'scholarships_awarded': ScholarshipApplication.objects.filter(status='awarded').count(),
    }
    
    recent_invoices = Invoice.objects.all()[:10]
    recent_payments = Payment.objects.all()[:10]
    pending_expenses = Expense.objects.filter(status='pending')[:10]
    
    context = {
        'stats': stats,
        'recent_invoices': recent_invoices,
        'recent_payments': recent_payments,
        'pending_expenses': pending_expenses,
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
def invoice_list(request):
    """List all invoices"""
    invoices = Invoice.objects.all()
    
    # Filter
    status_filter = request.GET.get('status')
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    
    search = request.GET.get('search')
    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search) |
            Q(student__user__email__icontains=search)
        )
    
    paginator = Paginator(invoices, 20)
    page = request.GET.get('page')
    invoices_page = paginator.get_page(page)
    
    context = {'invoices': invoices_page}
    return render(request, 'finance/invoice_list.html', context)


@login_required
def invoice_create(request):
    """Create new invoice"""
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
            return redirect('finance:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'finance/invoice_form.html', context)


@login_required
def invoice_detail(request, pk):
    """Invoice detail view"""
    invoice = get_object_or_404(Invoice, pk=pk)
    payments = invoice.payments.all()
    
    context = {
        'invoice': invoice,
        'payments': payments,
    }
    return render(request, 'finance/invoice_detail.html', context)


@login_required
def payment_create(request):
    """Record new payment"""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.processed_by = request.user
            payment.save()
            messages.success(request, f'Payment {payment.receipt_number} recorded successfully!')
            return redirect('finance:invoice_detail', pk=payment.invoice.pk)
    else:
        form = PaymentForm()
    
    context = {'form': form}
    return render(request, 'finance/payment_form.html', context)


@login_required
def expense_list(request):
    """List all expenses"""
    expenses = Expense.objects.all()
    
    status_filter = request.GET.get('status')
    if status_filter:
        expenses = expenses.filter(status=status_filter)
    
    paginator = Paginator(expenses, 20)
    page = request.GET.get('page')
    expenses_page = paginator.get_page(page)
    
    context = {'expenses': expenses_page}
    return render(request, 'finance/expense_list.html', context)


@login_required
def expense_create(request):
    """Create new expense"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.requested_by = request.user
            expense.save()
            messages.success(request, f'Expense {expense.expense_number} created successfully!')
            return redirect('finance:expense_list')
    else:
        form = ExpenseForm()
    
    context = {'form': form}
    return render(request, 'finance/expense_form.html', context)


@login_required
def scholarship_list(request):
    """List all scholarships"""
    scholarships = Scholarship.objects.filter(status='active')
    
    context = {'scholarships': scholarships}
    return render(request, 'finance/scholarship_list.html', context)


@login_required
def export_invoices_csv(request):
    """Export invoices to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="invoices_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Invoice Number', 'Student', 'Amount Due', 'Amount Paid', 'Balance', 'Status', 'Due Date'])
    
    invoices = Invoice.objects.all()
    for inv in invoices:
        writer.writerow([
            inv.invoice_number,
            inv.student.user.email,
            inv.amount_due,
            inv.amount_paid,
            inv.balance,
            inv.get_status_display(),
            inv.due_date
        ])
    
    return response
