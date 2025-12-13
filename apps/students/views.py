"""
Students Views - Complete CRUD Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Student
from .forms import StudentForm
from .filters import StudentFilter
from .utils import generate_students_report, export_students_to_csv


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """
    Students dashboard with statistics and overview
    """
    # Get statistics
    total_students = Student.objects.count()
    active_students = Student.objects.filter(student_status='active').count()
    on_leave = Student.objects.filter(student_status='on_leave').count()
    graduated = Student.objects.filter(student_status='graduated').count()
    
    # Recent students
    recent_students = Student.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_students': total_students,
        'active_students': active_students,
        'on_leave': on_leave,
        'graduated': graduated,
        'recent_students': recent_students,
    }
    
    return render(request, students/dashboard.htmlstudents/'students/dashboard.html, context)


# ============================================================================
# List View (Read - All)
# ============================================================================

@login_required
def item_list(request):
    """
    List all students with filtering, search, and pagination
    """
    # Get all students
    students = Student.objects.all()
    
    # Apply filters using django-filter
    filter_instance = StudentFilter(request.GET, queryset=students)
    students = filter_instance.qs
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(student_id__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    students = students.order_by(sort_by)
    
    # Statistics
    stats = {
        'total': students.count(),
        'active': students.filter(student_status='active').count(),
        'on_leave': students.filter(student_status='on_leave').count(),
        'graduated': students.filter(student_status='graduated').count(),
        'applicants': 0,  # Students don't have applicant status
    }
    
    # Pagination
    paginator = Paginator(students, 20)  # Show 20 students per page
    page = request.GET.get('page')
    
    try:
        students_page = paginator.page(page)
    except PageNotAnInteger:
        students_page = paginator.page(1)
    except EmptyPage:
        students_page = paginator.page(paginator.num_pages)
    
    context = {
        'students': students_page,
        'page_obj': students_page,  # For template compatibility
        'filter': filter_instance,
        'search_query': search_query,
        'sort_by': sort_by,
        'stats': stats,
        'title': 'Students List',
    }
    
    return render(request, students/student_list.htmlstudents/'students/student_list.html, context)


# ============================================================================
# Detail View (Read - Single)
# ============================================================================

@login_required
def item_detail(request, pk):
    """
    View single student details
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Get enrollments and attendance
    enrollments = student.enrollments.all()
    attendance_records = student.student_attendance_records.all()[:20]
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'attendance_records': attendance_records,
        'title': f'Student: {student.get_full_name()}',
    }
    
    return render(request, students/student_detail.htmlstudents/'students/student_detail.html, context)


# ============================================================================
# Create View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def item_create(request):
    """
    Create new student
    """
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    student = form.save(commit=False)
                    student.role = 'student'
                    student.save()
                    
                    messages.success(request, f'Student {student.get_full_name()} created successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_add'):
                        return redirect('students:create')
                    elif request.POST.get('save_and_continue'):
                        return redirect('students:update', pk=student.pk)
                    else:
                        return redirect('students:detail', pk=student.pk)
                        
            except Exception as e:
                messages.error(request, f'Error creating student: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create New Student',
    }
    
    return render(request, students/student_form.htmlstudents/'students/student_form.html, context)


# ============================================================================
# Update View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def item_update(request, pk):
    """
    Update existing student
    """
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_student = form.save()
                    
                    messages.success(request, f'Student {updated_student.get_full_name()} updated successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_continue'):
                        return redirect('students:update', pk=updated_student.pk)
                    else:
                        return redirect('students:detail', pk=updated_student.pk)
                        
            except Exception as e:
                messages.error(request, f'Error updating student: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'action': 'Update',
        'title': f'Update Student: {student.get_full_name()}',
    }
    
    return render(request, students/student_form.htmlstudents/'students/student_form.html, context)


# ============================================================================
# Delete View
# ============================================================================

@login_required
@require_http_methods(["POST"])
def item_delete(request, pk):
    """
    Delete student (soft or hard delete)
    """
    student = get_object_or_404(Student, pk=pk)
    
    try:
        student_name = student.get_full_name()
        student.delete()
        messages.success(request, f'Student {student_name} deleted successfully!')
        return redirect('students:list')
    except Exception as e:
        messages.error(request, f'Error deleting student: {str(e)}')
        return redirect('students:detail', pk=pk)


# ============================================================================
# Bulk Operations
# ============================================================================

@login_required
@require_http_methods(["POST"])
def bulk_delete(request):
    """
    Delete multiple items at once
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    item_ids = request.POST.getlist('item_ids[]')
    
    try:
        deleted_count = Student.objects.filter(id__in=item_ids).delete()[0]
        return JsonResponse({
            'success': True,
            'message': f'{deleted_count} items deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def bulk_update_status(request):
    """
    Update status for multiple students
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    item_ids = request.POST.getlist('item_ids[]')
    status = request.POST.get('status')
    
    try:
        updated_count = Student.objects.filter(id__in=item_ids).update(student_status=status)
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} students updated successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_csv(request):
    """
    Export students to CSV
    """
    students = Student.objects.all()
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="students_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Program', 'Batch', 'Status', 'Admission Year'])
    
    for student in students:
        writer.writerow([
            student.student_id,
            student.first_name,
            student.last_name,
            student.email,
            student.phone,
            student.program,
            student.batch,
            student.student_status,
            student.admission_year,
        ])
    
    return response


@login_required
def export_pdf(request):
    """
    Export students to PDF
    """
    students = Student.objects.all()
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, 'Students Report')
    
    # Date
    p.setFont("Helvetica", 10)
    p.drawString(100, 730, f'Generated: {timezone.now().strftime("%Y-%m-%d %H:%M")}')
    
    # Students
    y = 700
    p.setFont("Helvetica", 10)
    
    for student in students[:50]:  # Limit to 50 students for simple PDF
        p.drawString(100, y, f'{student.student_id} - {student.get_full_name()} - {student.student_status}')
        y -= 20
        
        if y < 100:
            p.showPage()
            y = 750
            p.setFont("Helvetica", 10)
    
    p.save()
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="students_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    return response


# ============================================================================
# AJAX/API Operations
# ============================================================================

@login_required
def get_item_data(request, pk):
    """
    Get student data as JSON (for AJAX requests)
    """
    student = get_object_or_404(Student, pk=pk)
    
    data = {
        'id': student.id,
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'email': student.email,
        'phone': student.phone,
        'program': student.program,
        'batch': student.batch,
        'student_status': student.student_status,
        'created_at': student.created_at.isoformat(),
        'updated_at': student.updated_at.isoformat(),
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def toggle_status(request, pk):
    """
    Toggle student status (active/inactive)
    """
    student = get_object_or_404(Student, pk=pk)
    
    try:
        if student.student_status == 'active':
            student.student_status = 'on_leave'
        else:
            student.student_status = 'active'
        
        student.save()
        
        return JsonResponse({
            'success': True,
            'status': student.student_status,
            'message': f'Status changed to {student.student_status}'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Statistics and Reports
# ============================================================================

@login_required
def statistics(request):
    """
    View statistics and reports
    """
    students = Student.objects.all()
    
    # Statistics by status
    stats = {
        'total': students.count(),
        'by_status': {
            'active': students.filter(student_status='active').count(),
            'on_leave': students.filter(student_status='on_leave').count(),
            'graduated': students.filter(student_status='graduated').count(),
            'withdrawn': students.filter(student_status='withdrawn').count(),
        },
        'by_program': {},
        'recent_activity': students.order_by('-updated_at')[:10],
    }
    
    # Statistics by program
    programs = students.values_list('program', flat=True).distinct()
    for program in programs:
        if program:
            stats['by_program'][program] = students.filter(program=program).count()
    
    context = {
        'stats': stats,
        'title': 'Student Statistics',
    }
    
    return render(request, students/statistics.htmlstudents/'students/statistics.html, context)


# ============================================================================
# Search and Filter
# ============================================================================

@login_required
def search(request):
    """
    Advanced search functionality
    """
    query = request.GET.get('q', '')
    
    students = Student.objects.all()
    
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(student_id__icontains=query) |
            Q(program__icontains=query)
        )
    
    # Apply additional filters from request
    status_filter = request.GET.get('status')
    if status_filter:
        students = students.filter(student_status=status_filter)
    
    program_filter = request.GET.get('program')
    if program_filter:
        students = students.filter(program=program_filter)
    
    year_filter = request.GET.get('admission_year')
    if year_filter:
        students = students.filter(admission_year=year_filter)
    
    context = {
        'students': students,
        'query': query,
        'title': 'Search Students',
    }
    
    return render(request, students/search_results.htmlstudents/'students/search_results.html, context)
