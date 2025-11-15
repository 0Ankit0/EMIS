"""
Student frontend views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Student, StudentStatus
from .forms import StudentCreateForm, StudentUpdateForm


@login_required
def dashboard(request):
    """
    Student portal dashboard
    Shows overview for logged-in student
    """
    # Check if user has a student profile
    try:
        student = request.user.student_profile
    except:
        messages.error(request, "You don't have a student profile")
        return redirect('core:dashboard')
    
    context = {
        'student': student,
        'title': 'Student Dashboard',
    }
    return render(request, 'students/dashboard.html', context)


@login_required
def student_list(request):
    """
    List all students (for admin/staff)
    GET /students/
    """
    # Check permission
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view this page")
        return redirect('core:dashboard')
    
    # Get filters from request
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')
    
    # Base queryset
    students = Student.objects.select_related('user', 'created_by').all()
    
    # Apply filters
    if status_filter:
        students = students.filter(status=status_filter)
    
    if search_query:
        students = students.filter(
            Q(student_number__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Statistics
    stats = {
        'total': Student.objects.count(),
        'active': Student.objects.filter(status=StudentStatus.ACTIVE).count(),
        'applicants': Student.objects.filter(status=StudentStatus.APPLICANT).count(),
        'graduated': Student.objects.filter(status=StudentStatus.GRADUATED).count(),
    }
    
    # Pagination
    paginator = Paginator(students, 20)  # 20 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': StudentStatus.choices,
        'title': 'Students',
    }
    return render(request, 'students/student_list.html', context)


@login_required
def student_detail(request, pk):
    """
    Student detail view
    GET /students/<id>/
    """
    student = get_object_or_404(
        Student.objects.select_related('user', 'created_by', 'updated_by'),
        pk=pk
    )
    
    # Check permission: student can view own profile, staff can view all
    if not request.user.is_staff:
        if not hasattr(request.user, 'student_profile') or request.user.student_profile.pk != student.pk:
            messages.error(request, "You don't have permission to view this profile")
            return redirect('core:dashboard')
    
    context = {
        'student': student,
        'title': f'Student: {student.get_full_name()}',
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def student_create(request):
    """
    Create new student
    GET/POST /students/create/
    """
    # Check permission
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create students")
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.created_by = request.user
            student.save()
            
            messages.success(
                request,
                f"Student {student.get_full_name()} created successfully"
            )
            return redirect('students:detail', pk=student.pk)
    else:
        form = StudentCreateForm()
    
    context = {
        'form': form,
        'title': 'Create Student',
    }
    return render(request, 'students/student_form.html', context)


@login_required
def student_update(request, pk):
    """
    Update student information
    GET/POST /students/<id>/update/
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Check permission
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to update students")
        return redirect('students:detail', pk=pk)
    
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.updated_by = request.user
            student.save()
            
            messages.success(
                request,
                f"Student {student.get_full_name()} updated successfully"
            )
            return redirect('students:detail', pk=student.pk)
    else:
        form = StudentUpdateForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'title': f'Update Student: {student.get_full_name()}',
    }
    return render(request, 'students/student_form.html', context)


@login_required
@require_http_methods(["POST"])
def student_admit(request, pk):
    """
    Admit a student (applicant -> active)
    POST /students/<id>/admit/
    """
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to admit students")
        return redirect('students:detail', pk=pk)
    
    student = get_object_or_404(Student, pk=pk)
    
    try:
        student.admit()
        messages.success(
            request,
            f"Student {student.get_full_name()} admitted successfully"
        )
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('students:detail', pk=pk)


@login_required
@require_http_methods(["POST"])
def student_graduate(request, pk):
    """
    Graduate a student
    POST /students/<id>/graduate/
    """
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to graduate students")
        return redirect('students:detail', pk=pk)
    
    student = get_object_or_404(Student, pk=pk)
    
    degree = request.POST.get('degree_earned', '')
    honors = request.POST.get('honors', '')
    
    try:
        student.graduate(degree_earned=degree, honors=honors)
        messages.success(
            request,
            f"Student {student.get_full_name()} graduated successfully"
        )
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('students:detail', pk=pk)


@login_required
def statistics(request):
    """
    Student statistics page
    GET /students/statistics/
    """
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view statistics")
        return redirect('core:dashboard')
    
    stats = {
        'total': Student.objects.count(),
        'by_status': dict(
            Student.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')
        ),
        'active': Student.objects.filter(status=StudentStatus.ACTIVE).count(),
        'applicants': Student.objects.filter(status=StudentStatus.APPLICANT).count(),
        'graduated': Student.objects.filter(status=StudentStatus.GRADUATED).count(),
        'avg_gpa': Student.objects.filter(
            status=StudentStatus.ACTIVE,
            current_gpa__isnull=False
        ).aggregate(avg_gpa=Avg('current_gpa'))['avg_gpa'],
    }
    
    context = {
        'stats': stats,
        'title': 'Student Statistics',
    }
    return render(request, 'students/statistics.html', context)
