"""HR Utility Functions"""
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import csv
from io import StringIO


def calculate_leave_balance(employee, leave_type, year=None):
    """Calculate leave balance for an employee"""
    from .models import Leave
    
    if year is None:
        year = timezone.now().year
    
    # Default entitlements (can be customized per organization)
    entitlements = {
        'casual': 12,
        'sick': 12,
        'earned': 30,
        'maternity': 180,
        'paternity': 15,
        'unpaid': 0,
        'compensatory': 0,
    }
    
    # Get approved leaves for the year
    approved_leaves = Leave.objects.filter(
        employee=employee,
        leave_type=leave_type,
        status='approved',
        start_date__year=year
    )
    
    total_taken = sum(leave.number_of_days for leave in approved_leaves)
    entitled = entitlements.get(leave_type, 0)
    balance = entitled - total_taken
    
    return {
        'entitled': entitled,
        'taken': total_taken,
        'balance': max(0, balance),
        'year': year
    }


def calculate_attendance_summary(employee, start_date=None, end_date=None):
    """Calculate attendance summary for an employee"""
    from .models import Attendance
    
    if start_date is None:
        start_date = date.today().replace(day=1)
    if end_date is None:
        end_date = date.today()
    
    attendance = Attendance.objects.filter(
        employee=employee,
        date__gte=start_date,
        date__lte=end_date
    )
    
    total_days = attendance.count()
    
    return {
        'total_days': total_days,
        'present': attendance.filter(status='present').count(),
        'absent': attendance.filter(status='absent').count(),
        'half_day': attendance.filter(status='half_day').count(),
        'late': attendance.filter(status='late').count(),
        'on_leave': attendance.filter(status='on_leave').count(),
        'work_from_home': attendance.filter(status='work_from_home').count(),
        'attendance_percentage': (
            attendance.filter(status__in=['present', 'half_day', 'work_from_home']).count() / total_days * 100
            if total_days > 0 else 0
        )
    }


def generate_payroll_for_employee(employee, month, year):
    """Generate payroll for an employee for a specific month"""
    from .models import Payroll, Attendance
    import calendar
    
    # Check if payroll already exists
    existing = Payroll.objects.filter(employee=employee, month=month, year=year).first()
    if existing:
        return existing
    
    # Calculate working days
    num_days = calendar.monthrange(year, month)[1]
    working_days = num_days - 8  # Assuming 8 Sundays/holidays
    
    # Get attendance
    attendance = Attendance.objects.filter(
        employee=employee,
        date__year=year,
        date__month=month
    )
    
    present_days = attendance.filter(status__in=['present', 'work_from_home']).count()
    half_days = attendance.filter(status='half_day').count()
    leave_days = attendance.filter(status='on_leave').count()
    
    # Adjust for half days
    effective_present = present_days + (half_days * 0.5)
    
    # Calculate pro-rated salary
    salary_per_day = employee.basic_salary / working_days
    basic_salary = salary_per_day * effective_present
    
    # Calculate allowances (pro-rated)
    hra = (employee.hra / working_days) * effective_present
    da = (employee.da / working_days) * effective_present
    other_allowances = (employee.other_allowances / working_days) * effective_present
    
    # Calculate deductions (12% PF, 0.75% ESI as example)
    pf = basic_salary * Decimal('0.12')
    esi = basic_salary * Decimal('0.0075') if basic_salary <= 21000 else 0
    
    # Create payroll
    payroll = Payroll.objects.create(
        employee=employee,
        month=month,
        year=year,
        basic_salary=basic_salary,
        hra=hra,
        da=da,
        other_allowances=other_allowances,
        pf=pf,
        esi=esi,
        working_days=working_days,
        present_days=int(effective_present),
        leave_days=leave_days,
        status='draft'
    )
    
    return payroll


def generate_payroll_for_all_employees(month, year):
    """Generate payroll for all active employees"""
    from .models import Employee
    
    employees = Employee.objects.active()
    count = 0
    
    for employee in employees:
        try:
            generate_payroll_for_employee(employee, month, year)
            count += 1
        except Exception as e:
            print(f"Error generating payroll for {employee.employee_id}: {e}")
            continue
    
    return count


def get_department_statistics(department):
    """Get statistics for a department"""
    from .models import Employee
    
    employees = Employee.objects.filter(department=department)
    
    return {
        'total_employees': employees.count(),
        'active': employees.filter(status='active').count(),
        'by_employment_type': dict(
            employees.values('employment_type').annotate(count=Count('id')).values_list('employment_type', 'count')
        ),
        'average_salary': employees.aggregate(avg=Avg('basic_salary'))['avg'] or 0,
        'total_salary_cost': employees.aggregate(total=Sum('basic_salary'))['total'] or 0,
    }


def export_employees_to_csv(queryset):
    """Export employees to CSV"""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Employee ID', 'Name', 'Email', 'Phone', 'Department', 'Designation',
        'Employment Type', 'Status', 'Joining Date', 'Basic Salary'
    ])
    
    for emp in queryset:
        writer.writerow([
            emp.employee_id,
            emp.get_full_name(),
            emp.email,
            emp.phone,
            emp.department.name,
            emp.designation.title,
            emp.get_employment_type_display(),
            emp.get_status_display(),
            emp.date_of_joining,
            emp.basic_salary
        ])
    
    return output.getvalue()


def export_payroll_to_csv(queryset):
    """Export payroll to CSV"""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Employee ID', 'Name', 'Month', 'Year', 'Basic Salary', 'HRA', 'DA',
        'Gross Salary', 'PF', 'ESI', 'Total Deductions', 'Net Salary', 'Status'
    ])
    
    for payroll in queryset:
        writer.writerow([
            payroll.employee.employee_id,
            payroll.employee.get_full_name(),
            payroll.month,
            payroll.year,
            payroll.basic_salary,
            payroll.hra,
            payroll.da,
            payroll.gross_salary,
            payroll.pf,
            payroll.esi,
            payroll.total_deductions,
            payroll.net_salary,
            payroll.get_status_display()
        ])
    
    return output.getvalue()


def get_recruitment_statistics(start_date=None, end_date=None):
    """Get recruitment statistics"""
    from .models import JobPosting, JobApplication
    
    postings = JobPosting.objects.all()
    applications = JobApplication.objects.all()
    
    if start_date:
        postings = postings.filter(posted_date__gte=start_date)
        applications = applications.filter(application_date__gte=start_date)
    
    if end_date:
        postings = postings.filter(posted_date__lte=end_date)
        applications = applications.filter(application_date__lte=end_date)
    
    return {
        'total_postings': postings.count(),
        'open_postings': postings.filter(status='open').count(),
        'total_applications': applications.count(),
        'by_status': dict(
            applications.values('status').annotate(count=Count('id')).values_list('status', 'count')
        ),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'selected': applications.filter(status='selected').count(),
        'joined': applications.filter(status='joined').count(),
    }


def calculate_employee_age(date_of_birth):
    """Calculate employee age"""
    today = date.today()
    return today.year - date_of_birth.year - (
        (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    )


def validate_leave_application(leave):
    """Validate leave application"""
    from .models import Leave
    
    # Check for overlapping leaves
    overlapping = Leave.objects.filter(
        employee=leave.employee,
        status__in=['pending', 'approved'],
        start_date__lte=leave.end_date,
        end_date__gte=leave.start_date
    )
    
    if leave.pk:
        overlapping = overlapping.exclude(pk=leave.pk)
    
    if overlapping.exists():
        return False, "Overlapping leave exists"
    
    # Check leave balance
    balance = calculate_leave_balance(leave.employee, leave.leave_type, leave.start_date.year)
    
    if balance['balance'] < leave.number_of_days:
        return False, f"Insufficient leave balance. Available: {balance['balance']} days"
    
    return True, None


def send_leave_notification(leave):
    """Send leave notification"""
    # TODO: Implement email/SMS notification
    pass


def send_payroll_notification(payroll):
    """Send payroll notification"""
    # TODO: Implement email notification with payslip
    pass
