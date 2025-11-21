"""
Faculty Views - Django Template Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction
import csv

from .models import (
    Department, Faculty, FacultyQualification, FacultyExperience,
    FacultyAttendance, FacultyLeave, FacultyPublication, FacultyAward
)
from .forms import (
    DepartmentForm, FacultyForm, FacultyQualificationForm, FacultyExperienceForm,
    FacultyAttendanceForm, FacultyLeaveForm, FacultyPublicationForm, FacultyAwardForm
)


@login_required
def dashboard(request):
    """Faculty dashboard"""
    stats = {
        'total_faculty': Faculty.objects.count(),
        'active_faculty': Faculty.objects.active().count(),
        'on_leave': Faculty.objects.on_leave().count(),
        'departments': Department.objects.filter(is_active=True).count(),
    }
    
    recent_faculty = Faculty.objects.all()[:5]
    pending_leaves = FacultyLeave.objects.filter(status='pending')[:10]
    
    context = {
        'stats': stats,
        'recent_faculty': recent_faculty,
        'pending_leaves': pending_leaves,
    }
    
    return render(request, 'faculty/dashboard.html', context)


@login_required
def faculty_list(request):
    """List all faculty members"""
    faculty = Faculty.objects.all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        faculty = faculty.filter(
            Q(employee_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(official_email__icontains=search_query)
        )
    
    # Filter by department
    department_id = request.GET.get('department')
    if department_id:
        faculty = faculty.filter(department_id=department_id)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        faculty = faculty.filter(status=status)
    
    # Pagination
    paginator = Paginator(faculty, 20)
    page = request.GET.get('page')
    faculty_page = paginator.get_page(page)
    
    context = {
        'faculty_list': faculty_page,
        'departments': Department.objects.filter(is_active=True),
        'search_query': search_query,
    }
    
    return render(request, 'faculty/faculty_list.html', context)


@login_required
def faculty_detail(request, pk):
    """Faculty detail view"""
    faculty = get_object_or_404(Faculty, pk=pk)
    
    context = {
        'faculty': faculty,
        'qualifications': faculty.qualifications.all(),
        'experiences': faculty.experiences.all(),
        'publications': faculty.publications.all()[:10],
        'awards': faculty.awards.all(),
    }
    
    return render(request, 'faculty/faculty_detail.html', context)


@login_required
def faculty_create(request):
    """Create new faculty"""
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES)
        if form.is_valid():
            faculty = form.save(commit=False)
            faculty.created_by = request.user
            faculty.save()
            messages.success(request, f'Faculty {faculty.get_full_name()} created successfully!')
            return redirect('faculty:detail', pk=faculty.pk)
    else:
        form = FacultyForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'faculty/add_faculty.html', context)


@login_required
def faculty_update(request, pk):
    """Update faculty"""
    faculty = get_object_or_404(Faculty, pk=pk)
    
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, f'Faculty {faculty.get_full_name()} updated successfully!')
            return redirect('faculty:detail', pk=faculty.pk)
    else:
        form = FacultyForm(instance=faculty)
    
    context = {'form': form, 'faculty': faculty, 'action': 'Update'}
    return render(request, 'faculty/add_faculty.html', context)


@login_required
def faculty_delete(request, pk):
    """Delete faculty"""
    if request.method == 'POST':
        faculty = get_object_or_404(Faculty, pk=pk)
        name = faculty.get_full_name()
        faculty.delete()
        messages.success(request, f'Faculty {name} deleted successfully!')
        return redirect('faculty:list')
    return redirect('faculty:list')


@login_required
def attendance_list(request):
    """Faculty attendance list"""
    attendance = FacultyAttendance.objects.all()
    
    # Filter by date
    date = request.GET.get('date')
    if date:
        attendance = attendance.filter(date=date)
    
    # Pagination
    paginator = Paginator(attendance, 30)
    page = request.GET.get('page')
    attendance_page = paginator.get_page(page)
    
    context = {'attendance_list': attendance_page}
    return render(request, 'faculty/attendance.html', context)


@login_required
def leave_list(request):
    """Faculty leave list"""
    leaves = FacultyLeave.objects.all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        leaves = leaves.filter(status=status)
    
    # Pagination
    paginator = Paginator(leaves, 20)
    page = request.GET.get('page')
    leaves_page = paginator.get_page(page)
    
    context = {'leaves': leaves_page}
    return render(request, 'faculty/leaves.html', context)


@login_required
def export_csv(request):
    """Export faculty to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="faculty_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Department', 'Designation', 'Email', 'Phone', 'Status'])
    
    faculty = Faculty.objects.all()
    for f in faculty:
        writer.writerow([
            f.employee_id,
            f.get_full_name(),
            f.department.name,
            f.get_designation_display(),
            f.official_email,
            f.phone,
            f.get_status_display()
        ])
    
    return response
