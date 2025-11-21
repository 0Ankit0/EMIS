"""
Courses Views - Complete CRUD Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models.course import Course
from .models.module import Module
from .models.assignment import Assignment
from .forms import CourseForm, ModuleForm, AssignmentForm


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """
    Courses dashboard with statistics and overview
    """
    # Get statistics
    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(status='active').count()
    draft_courses = Course.objects.filter(status='draft').count()
    archived_courses = Course.objects.filter(status='archived').count()
    
    # Module and Assignment stats
    total_modules = Module.objects.count()
    total_assignments = Assignment.objects.count()
    
    # Recent items
    recent_courses = Course.objects.all().order_by('-created_at')[:5]
    recent_modules = Module.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_courses': total_courses,
        'active_courses': active_courses,
        'draft_courses': draft_courses,
        'archived_courses': archived_courses,
        'total_modules': total_modules,
        'total_assignments': total_assignments,
        'recent_courses': recent_courses,
        'recent_modules': recent_modules,
    }
    
    return render(request, 'courses/dashboard.html', context)


# ============================================================================
# List View (Read - All)
# ============================================================================

@login_required
def item_list(request):
    """
    List all courses with filtering, search, and pagination
    """
    # Get all courses
    courses = Course.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        courses = courses.filter(status=status_filter)
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        courses = courses.filter(department=department_filter)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    courses = courses.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(courses, 20)
    page = request.GET.get('page')
    
    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        courses_page = paginator.page(1)
    except EmptyPage:
        courses_page = paginator.page(paginator.num_pages)
    
    # Get unique departments for filter
    departments = Course.objects.values_list('department', flat=True).distinct()
    
    context = {
        'courses': courses_page,
        'search_query': search_query,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'departments': departments,
        'sort_by': sort_by,
    }
    
    return render(request, 'courses/course_list.html', context)


# ============================================================================
# Detail View (Read - Single)
# ============================================================================

@login_required
def item_detail(request, pk):
    """
    View single course details
    """
    course = get_object_or_404(Course, pk=pk)
    
    # Get related data
    modules = Module.objects.filter(course=course).order_by('sequence_order')
    assignments = Assignment.objects.filter(course=course).order_by('-due_date')
    
    context = {
        'course': course,
        'item': course,  # For template compatibility
        'modules': modules,
        'assignments': assignments,
    }
    
    return render(request, 'courses/course_detail.html', context)


# ============================================================================
# Create View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def item_create(request):
    """
    Create new course
    """
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    course = form.save(commit=False)
                    course.created_by = request.user
                    course.save()
                    
                    messages.success(request, f'Course "{course.title}" created successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_add'):
                        return redirect('courses:create')
                    elif request.POST.get('save_and_continue'):
                        return redirect('courses:update', pk=course.pk)
                    else:
                        return redirect('courses:detail', pk=course.pk)
                        
            except Exception as e:
                messages.error(request, f'Error creating course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create New Course',
    }
    
    return render(request, 'courses/course_form.html', context)


# ============================================================================
# Update View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def item_update(request, pk):
    """
    Update existing item
    """
    item = get_object_or_404(Course, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('courses:detail', pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_item = form.save()
                    
                    messages.success(request, f'{updated_item.name} updated successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_continue'):
                        return redirect('courses:update', pk=updated_item.pk)
                    else:
                        return redirect('courses:detail', pk=updated_item.pk)
                        
            except Exception as e:
                messages.error(request, f'Error updating item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'action': 'Update',
    }
    
    return render(request, 'courses/item_form.html', context)


# ============================================================================
# Delete View
# ============================================================================

@login_required
@require_http_methods(["POST"])
def item_delete(request, pk):
    """
    Delete item (soft or hard delete)
    """
    item = get_object_or_404(Course, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('courses:detail', pk=pk)
    
    try:
        item_name = item.name
        item.delete()
        messages.success(request, f'{item_name} deleted successfully!')
        return redirect('courses:list')
    except Exception as e:
        messages.error(request, f'Error deleting item: {str(e)}')
        return redirect('courses:detail', pk=pk)


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
        deleted_count = Course.objects.filter(id__in=item_ids).delete()[0]
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
    Update status for multiple items
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    item_ids = request.POST.getlist('item_ids[]')
    status = request.POST.get('status')
    
    try:
        updated_count = Course.objects.filter(id__in=item_ids).update(status=status)
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} items updated successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_csv(request):
    """
    Export items to CSV
    """
    items = Course.objects.all()
    
    # Apply user filter if not admin
    if not request.user.is_staff:
        items = items.filter(created_by=request.user)
    
    # Generate CSV
    csv_data = export_courses_to_csv(items)
    
    # Create response
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="courses_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    return response


@login_required
def export_pdf(request):
    """
    Export items to PDF
    """
    items = Course.objects.all()
    
    # Apply user filter if not admin
    if not request.user.is_staff:
        items = items.filter(created_by=request.user)
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f'Courses Report')
    
    # Date
    p.setFont("Helvetica", 10)
    p.drawString(100, 730, f'Generated: {timezone.now().strftime("%Y-%m-%d %H:%M")}')
    
    # Items
    y = 700
    p.setFont("Helvetica", 12)
    
    for item in items[:50]:  # Limit to 50 items for simple PDF
        p.drawString(100, y, f'{item.name} - {item.status}')
        y -= 20
        
        if y < 100:
            p.showPage()
            y = 750
    
    p.save()
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="courses_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    return response


# ============================================================================
# AJAX/API Operations
# ============================================================================

@login_required
def get_item_data(request, pk):
    """
    Get item data as JSON (for AJAX requests)
    """
    item = get_object_or_404(Course, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    data = {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'status': item.status,
        'created_at': item.created_at.isoformat(),
        'updated_at': item.updated_at.isoformat(),
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def toggle_status(request, pk):
    """
    Toggle item status (active/inactive)
    """
    item = get_object_or_404(Course, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        if item.status == 'active':
            item.status = 'inactive'
        else:
            item.status = 'active'
        
        item.save()
        
        return JsonResponse({
            'success': True,
            'status': item.status,
            'message': f'Status changed to {item.status}'
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
    items = Course.objects.all()
    
    # Apply user filter if not admin
    if not request.user.is_staff:
        items = items.filter(created_by=request.user)
    
    # Generate report
    report_data = generate_courses_report(items)
    
    # Additional statistics
    stats = {
        'total': items.count(),
        'by_status': {
            'active': items.filter(status='active').count(),
            'inactive': items.filter(status='inactive').count(),
            'pending': items.filter(status='pending').count(),
        },
        'by_month': {
            # Add monthly statistics
        },
        'recent_activity': items.order_by('-updated_at')[:10],
    }
    
    context = {
        'report_data': report_data,
        'stats': stats,
    }
    
    return render(request, 'courses/statistics.html', context)


# ============================================================================
# Search and Filter
# ============================================================================

@login_required
def search(request):
    """
    Advanced search functionality
    """
    query = request.GET.get('q', '')
    
    courses = Course.objects.all()
    
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(code__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Apply additional filters from request
    status_filter = request.GET.get('status')
    if status_filter:
        courses = courses.filter(status=status_filter)
    
    date_from = request.GET.get('date_from')
    if date_from:
        courses = courses.filter(created_at__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        courses = courses.filter(created_at__lte=date_to)
    
    context = {
        'courses': courses,
        'query': query,
    }
    
    return render(request, 'courses/search_results.html', context)


# ============================================================================
# Module Management
# ============================================================================

@login_required
def module_list(request, course_pk):
    """List all modules for a course"""
    course = get_object_or_404(Course, pk=course_pk)
    modules = Module.objects.filter(course=course).order_by('sequence_order')
    
    context = {
        'course': course,
        'modules': modules,
    }
    return render(request, 'courses/module_list.html', context)


@login_required
def module_create(request, course_pk):
    """Create new module"""
    course = get_object_or_404(Course, pk=course_pk)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, f'Module "{module.title}" created successfully!')
            return redirect('courses:module_list', course_pk=course.pk)
    else:
        form = ModuleForm(initial={'course': course})
    
    context = {
        'form': form,
        'course': course,
        'action': 'Create',
    }
    return render(request, 'courses/module_form.html', context)


@login_required
def module_detail(request, pk):
    """View module details"""
    module = get_object_or_404(Module, pk=pk)
    
    context = {
        'module': module,
        'course': module.course,
    }
    return render(request, 'courses/module_detail.html', context)


@login_required
def module_update(request, pk):
    """Update module"""
    module = get_object_or_404(Module, pk=pk)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, f'Module "{module.title}" updated successfully!')
            return redirect('courses:module_detail', pk=module.pk)
    else:
        form = ModuleForm(instance=module)
    
    context = {
        'form': form,
        'module': module,
        'course': module.course,
        'action': 'Update',
    }
    return render(request, 'courses/module_form.html', context)


@login_required
@require_http_methods(["POST"])
def module_delete(request, pk):
    """Delete module"""
    module = get_object_or_404(Module, pk=pk)
    course_pk = module.course.pk
    module_title = module.title
    module.delete()
    messages.success(request, f'Module "{module_title}" deleted successfully!')
    return redirect('courses:module_list', course_pk=course_pk)


# ============================================================================
# Assignment Management
# ============================================================================

@login_required
def assignment_list(request, course_pk):
    """List all assignments for a course"""
    course = get_object_or_404(Course, pk=course_pk)
    assignments = Assignment.objects.filter(course=course).order_by('-due_date')
    
    context = {
        'course': course,
        'assignments': assignments,
    }
    return render(request, 'courses/assignment_list.html', context)


@login_required
def assignment_create(request, course_pk):
    """Create new assignment"""
    course = get_object_or_404(Course, pk=course_pk)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, f'Assignment "{assignment.title}" created successfully!')
            return redirect('courses:assignment_list', course_pk=course.pk)
    else:
        form = AssignmentForm(initial={'course': course})
    
    context = {
        'form': form,
        'course': course,
        'action': 'Create',
    }
    return render(request, 'courses/assignment_form.html', context)


@login_required
def assignment_detail(request, pk):
    """View assignment details"""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    context = {
        'assignment': assignment,
        'course': assignment.course,
    }
    return render(request, 'courses/assignment_detail.html', context)


@login_required
def assignment_update(request, pk):
    """Update assignment"""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Assignment "{assignment.title}" updated successfully!')
            return redirect('courses:assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment)
    
    context = {
        'form': form,
        'assignment': assignment,
        'course': assignment.course,
        'action': 'Update',
    }
    return render(request, 'courses/assignment_form.html', context)


@login_required
@require_http_methods(["POST"])
def assignment_delete(request, pk):
    """Delete assignment"""
    assignment = get_object_or_404(Assignment, pk=pk)
    course_pk = assignment.course.pk
    assignment_title = assignment.title
    assignment.delete()
    messages.success(request, f'Assignment "{assignment_title}" deleted successfully!')
    return redirect('courses:assignment_list', course_pk=course_pk)


# ============================================================================
# Additional Pages
# ============================================================================

@login_required
def programs(request):
    """View all programs/courses organized by department"""
    departments = Course.objects.values('department').annotate(
        course_count=Count('id')
    ).order_by('department')
    
    context = {
        'departments': departments,
    }
    return render(request, 'courses/programs.html', context)


@login_required
def syllabus_view(request):
    """View and manage course syllabi"""
    courses = Course.objects.all().order_by('code')
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/syllabus.html', context)


@login_required
def enrollments(request):
    """Manage course enrollments"""
    courses = Course.objects.filter(status='active').order_by('code')
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/enrollments.html', context)


@login_required
def course_materials(request):
    """Manage course materials"""
    courses = Course.objects.all().order_by('code')
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/course_materials.html', context)


@login_required
def prerequisites(request):
    """Manage course prerequisites"""
    courses = Course.objects.all().order_by('code')
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/prerequisites.html', context)


@login_required
def curriculum(request):
    """View curriculum structure"""
    courses = Course.objects.all().order_by('department', 'semester', 'code')
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/curriculum.html', context)
