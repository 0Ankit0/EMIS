"""HR Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, Avg
from django.http import HttpResponse
from django.utils import timezone
import csv

from .models import (
    Department, Designation, Employee, Attendance, Leave, Payroll,
    JobPosting, JobApplication, PerformanceReview, Training, TrainingParticipant
)
from .forms import EmployeeForm, LeaveForm, PayrollForm, JobPostingForm


@login_required
def dashboard(request):
    """HR dashboard"""
    stats = {
        'total_employees': Employee.objects.active().count(),
        'on_leave': Employee.objects.on_leave().count(),
        'pending_leaves': Leave.objects.pending().count(),
        'open_positions': JobPosting.objects.open().count(),
        'pending_applications': JobApplication.objects.submitted().count(),
    }
    
    recent_employees = Employee.objects.all()[:10]
    pending_leaves = Leave.objects.pending()[:10]
    
    context = {
        'stats': stats,
        'recent_employees': recent_employees,
        'pending_leaves': pending_leaves,
    }
    return render(request, 'hr/dashboard.html', context)


@login_required
def employee_list(request):
    """List all employees"""
    employees = Employee.objects.all()
    
    # Filters
    department_id = request.GET.get('department')
    if department_id:
        employees = employees.filter(department_id=department_id)
    
    status_filter = request.GET.get('status')
    if status_filter:
        employees = employees.filter(status=status_filter)
    
    search = request.GET.get('search')
    if search:
        employees = employees.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    paginator = Paginator(employees, 20)
    page = request.GET.get('page')
    employees_page = paginator.get_page(page)
    
    context = {
        'employees': employees_page,
        'departments': Department.objects.filter(is_active=True),
    }
    return render(request, 'hr/employee_list.html', context)


@login_required
def employee_detail(request, pk):
    """Employee detail view"""
    employee = get_object_or_404(Employee, pk=pk)
    
    attendance_records = employee.attendance_records.all()[:30]
    leave_applications = employee.leave_applications.all()[:10]
    payrolls = employee.payrolls.all()[:12]
    
    context = {
        'employee': employee,
        'attendance_records': attendance_records,
        'leave_applications': leave_applications,
        'payrolls': payrolls,
    }
    return render(request, 'hr/employee_detail.html', context)


@login_required
def attendance_list(request):
    """Attendance list"""
    attendance = Attendance.objects.all()
    
    # Filters
    date_filter = request.GET.get('date')
    if date_filter:
        attendance = attendance.filter(date=date_filter)
    
    employee_id = request.GET.get('employee')
    if employee_id:
        attendance = attendance.filter(employee_id=employee_id)
    
    paginator = Paginator(attendance, 30)
    page = request.GET.get('page')
    attendance_page = paginator.get_page(page)
    
    context = {'attendance_records': attendance_page}
    return render(request, 'hr/attendance_list.html', context)


@login_required
def leave_list(request):
    """Leave applications list"""
    leaves = Leave.objects.all()
    
    # Filter
    status_filter = request.GET.get('status')
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    
    paginator = Paginator(leaves, 20)
    page = request.GET.get('page')
    leaves_page = paginator.get_page(page)
    
    context = {'leaves': leaves_page}
    return render(request, 'hr/leave_list.html', context)


@login_required
def payroll_list(request):
    """Payroll list"""
    payrolls = Payroll.objects.all()
    
    # Filters
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if month:
        payrolls = payrolls.filter(month=month)
    if year:
        payrolls = payrolls.filter(year=year)
    
    paginator = Paginator(payrolls, 20)
    page = request.GET.get('page')
    payrolls_page = paginator.get_page(page)
    
    context = {'payrolls': payrolls_page}
    return render(request, 'hr/payroll_list.html', context)


@login_required
def job_list(request):
    """Job postings list"""
    jobs = JobPosting.objects.all()
    
    status_filter = request.GET.get('status')
    if status_filter:
        jobs = jobs.filter(status=status_filter)
    
    context = {'jobs': jobs}
    return render(request, 'hr/job_list.html', context)


@login_required
def application_list(request):
    """Job applications list"""
    applications = JobApplication.objects.all()
    
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    paginator = Paginator(applications, 20)
    page = request.GET.get('page')
    applications_page = paginator.get_page(page)
    
    context = {'applications': applications_page}
    return render(request, 'hr/application_list.html', context)


@login_required
def export_employees_csv(request):
    """Export employees to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="employees_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Email', 'Department', 'Designation', 'Status', 'Joining Date'])
    
    employees = Employee.objects.all()
    for emp in employees:
        writer.writerow([
            emp.employee_id,
            emp.get_full_name(),
            emp.email,
            emp.department.name,
            emp.designation.title,
            emp.get_status_display(),
            emp.date_of_joining
        ])
    
    return response


@login_required
def export_payroll_csv(request):
    """Export payroll to CSV"""
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="payroll_{month}_{year}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Basic', 'HRA', 'DA', 'Gross', 'Deductions', 'Net'])
    
    payrolls = Payroll.objects.filter(month=month, year=year) if month and year else Payroll.objects.all()
    
    for p in payrolls:
        writer.writerow([
            p.employee.employee_id,
            p.employee.get_full_name(),
            p.basic_salary,
            p.hra,
            p.da,
            p.gross_salary,
            p.total_deductions,
            p.net_salary
        ])
    
    return response
