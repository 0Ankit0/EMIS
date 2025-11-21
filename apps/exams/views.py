"""
Exams Views - Complete Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Avg, Sum
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from datetime import datetime
import csv
from io import BytesIO, StringIO

from .models import Exam, ExamResult, ExamSchedule
from .forms import ExamForm, ExamResultForm, ExamScheduleForm, BulkResultUploadForm
from .filters import ExamFilter, ExamResultFilter, ExamScheduleFilter
from .utils import (
    generate_exam_report, export_exams_to_csv, export_results_to_csv,
    process_bulk_results_csv, generate_result_card_pdf
)


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """
    Exams dashboard with statistics and overview
    """
    # Get statistics
    total_exams = Exam.objects.count()
    scheduled_exams = Exam.objects.scheduled().count()
    ongoing_exams = Exam.objects.ongoing().count()
    completed_exams = Exam.objects.completed().count()
    upcoming_exams = Exam.objects.upcoming().count()
    
    # Recent exams
    recent_exams = Exam.objects.all()[:5]
    
    # Upcoming exams
    upcoming_exams_list = Exam.objects.upcoming()[:5]
    
    # Results statistics
    total_results = ExamResult.objects.count()
    passed_results = ExamResult.objects.passed().count()
    failed_results = ExamResult.objects.failed().count()
    
    context = {
        'total_exams': total_exams,
        'scheduled_exams': scheduled_exams,
        'ongoing_exams': ongoing_exams,
        'completed_exams': completed_exams,
        'upcoming_exams_count': upcoming_exams,
        'recent_exams': recent_exams,
        'upcoming_exams_list': upcoming_exams_list,
        'total_results': total_results,
        'passed_results': passed_results,
        'failed_results': failed_results,
    }
    
    return render(request, 'exams/dashboard.html', context)


# ============================================================================
# Exam CRUD Views
# ============================================================================

@login_required
def exam_list(request):
    """
    List all exams with filtering, search, and pagination
    """
    exams = Exam.objects.select_related('course', 'invigilator').all()
    
    # Apply filters
    filter_instance = ExamFilter(request.GET, queryset=exams)
    exams = filter_instance.qs
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        exams = exams.filter(
            Q(exam_code__icontains=search_query) |
            Q(exam_name__icontains=search_query) |
            Q(course__course_name__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-exam_date')
    exams = exams.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(exams, 20)
    page = request.GET.get('page')
    
    try:
        exams_page = paginator.page(page)
    except PageNotAnInteger:
        exams_page = paginator.page(1)
    except EmptyPage:
        exams_page = paginator.page(paginator.num_pages)
    
    context = {
        'exams': exams_page,
        'filter': filter_instance,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'exams/exam_list.html', context)


@login_required
def exam_detail(request, pk):
    """
    View single exam details
    """
    exam = get_object_or_404(
        Exam.objects.select_related('course', 'invigilator'),
        pk=pk
    )
    
    # Get results for this exam
    results = exam.results.select_related('student').all()
    
    # Statistics
    total_students = results.count()
    passed_count = results.filter(is_passed=True).count()
    failed_count = results.filter(is_passed=False, is_absent=False).count()
    absent_count = results.filter(is_absent=True).count()
    
    # Grade distribution
    grade_distribution = results.values('grade').annotate(count=Count('grade')).order_by('grade')
    
    # Average marks
    avg_marks = results.filter(is_absent=False).aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    
    context = {
        'exam': exam,
        'results': results[:10],  # Show first 10 results
        'total_students': total_students,
        'passed_count': passed_count,
        'failed_count': failed_count,
        'absent_count': absent_count,
        'pass_percentage': exam.get_pass_percentage(),
        'grade_distribution': grade_distribution,
        'avg_marks': avg_marks,
    }
    
    return render(request, 'exams/exam_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def exam_create(request):
    """
    Create new exam
    """
    if request.method == 'POST':
        form = ExamForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    exam = form.save(commit=False)
                    exam.created_by = request.user
                    exam.save()
                    
                    messages.success(request, f'Exam "{exam.exam_name}" created successfully!')
                    
                    if request.POST.get('save_and_add'):
                        return redirect('exams:exam_create')
                    elif request.POST.get('save_and_continue'):
                        return redirect('exams:exam_update', pk=exam.pk)
                    else:
                        return redirect('exams:exam_detail', pk=exam.pk)
                        
            except Exception as e:
                messages.error(request, f'Error creating exam: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExamForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'exams/exam_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def exam_update(request, pk):
    """
    Update existing exam
    """
    exam = get_object_or_404(Exam, pk=pk)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_exam = form.save()
                    
                    messages.success(request, f'Exam "{updated_exam.exam_name}" updated successfully!')
                    
                    if request.POST.get('save_and_continue'):
                        return redirect('exams:exam_update', pk=updated_exam.pk)
                    else:
                        return redirect('exams:exam_detail', pk=updated_exam.pk)
                        
            except Exception as e:
                messages.error(request, f'Error updating exam: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExamForm(instance=exam)
    
    context = {
        'form': form,
        'exam': exam,
        'action': 'Update',
    }
    
    return render(request, 'exams/exam_form.html', context)


@login_required
@require_http_methods(["POST"])
def exam_delete(request, pk):
    """
    Delete exam
    """
    exam = get_object_or_404(Exam, pk=pk)
    
    try:
        exam_name = exam.exam_name
        exam.delete()
        messages.success(request, f'Exam "{exam_name}" deleted successfully!')
        return redirect('exams:exam_list')
    except Exception as e:
        messages.error(request, f'Error deleting exam: {str(e)}')
        return redirect('exams:exam_detail', pk=pk)


# ============================================================================
# Exam Result Views
# ============================================================================

@login_required
def result_list(request):
    """
    List all exam results with filtering
    """
    results = ExamResult.objects.select_related('exam', 'student').all()
    
    # Apply filters
    filter_instance = ExamResultFilter(request.GET, queryset=results)
    results = filter_instance.qs
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        results = results.filter(
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query) |
            Q(student__roll_number__icontains=search_query) |
            Q(exam__exam_code__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(results, 50)
    page = request.GET.get('page')
    
    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        results_page = paginator.page(1)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)
    
    context = {
        'results': results_page,
        'filter': filter_instance,
        'search_query': search_query,
    }
    
    return render(request, 'exams/result_list.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def result_create(request):
    """
    Create new exam result
    """
    if request.method == 'POST':
        form = ExamResultForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    result = form.save(commit=False)
                    if hasattr(request.user, 'faculty'):
                        result.evaluated_by = request.user.faculty
                    result.evaluated_at = timezone.now()
                    result.save()
                    
                    messages.success(request, 'Result added successfully!')
                    
                    if request.POST.get('save_and_add'):
                        return redirect('exams:result_create')
                    else:
                        return redirect('exams:result_list')
                        
            except Exception as e:
                messages.error(request, f'Error creating result: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExamResultForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'exams/result_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def result_update(request, pk):
    """
    Update exam result
    """
    result = get_object_or_404(ExamResult, pk=pk)
    
    if request.method == 'POST':
        form = ExamResultForm(request.POST, instance=result)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_result = form.save(commit=False)
                    if hasattr(request.user, 'faculty'):
                        updated_result.evaluated_by = request.user.faculty
                    updated_result.evaluated_at = timezone.now()
                    updated_result.save()
                    
                    messages.success(request, 'Result updated successfully!')
                    return redirect('exams:result_list')
                        
            except Exception as e:
                messages.error(request, f'Error updating result: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExamResultForm(instance=result)
    
    context = {
        'form': form,
        'result': result,
        'action': 'Update',
    }
    
    return render(request, 'exams/result_form.html', context)


@login_required
def grade_entry(request, exam_id):
    """
    Bulk grade entry for an exam
    """
    exam = get_object_or_404(Exam, pk=exam_id)
    
    # Get all enrolled students for this course
    from apps.students.models import Enrollment
    enrolled_students = Enrollment.objects.filter(
        course=exam.course,
        status='active'
    ).select_related('student')
    
    # Get existing results
    existing_results = {result.student_id: result for result in exam.results.all()}
    
    if request.method == 'POST':
        # Process bulk grade entry
        errors = []
        success_count = 0
        
        with transaction.atomic():
            for enrollment in enrolled_students:
                student = enrollment.student
                student_id = str(student.id)
                
                marks_key = f'marks_{student_id}'
                absent_key = f'absent_{student_id}'
                
                is_absent = request.POST.get(absent_key) == 'on'
                marks = request.POST.get(marks_key)
                
                if marks or is_absent:
                    try:
                        result, created = ExamResult.objects.update_or_create(
                            exam=exam,
                            student=student,
                            defaults={
                                'marks_obtained': float(marks) if marks and not is_absent else 0,
                                'is_absent': is_absent,
                                'evaluated_by': request.user.faculty if hasattr(request.user, 'faculty') else None,
                                'evaluated_at': timezone.now()
                            }
                        )
                        success_count += 1
                    except Exception as e:
                        errors.append(f"Error for {student.get_full_name()}: {str(e)}")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        
        messages.success(request, f'{success_count} results saved successfully!')
        return redirect('exams:exam_detail', pk=exam.pk)
    
    # Prepare data for template
    students_data = []
    for enrollment in enrolled_students:
        student = enrollment.student
        result = existing_results.get(student.id)
        students_data.append({
            'student': student,
            'result': result,
        })
    
    context = {
        'exam': exam,
        'students_data': students_data,
    }
    
    return render(request, 'exams/grade_entry.html', context)


# ============================================================================
# Exam Schedule Views
# ============================================================================

@login_required
def schedule_list(request):
    """
    List all exam schedules
    """
    schedules = ExamSchedule.objects.all()
    
    # Apply filters
    filter_instance = ExamScheduleFilter(request.GET, queryset=schedules)
    schedules = filter_instance.qs
    
    # Pagination
    paginator = Paginator(schedules, 20)
    page = request.GET.get('page')
    
    try:
        schedules_page = paginator.page(page)
    except PageNotAnInteger:
        schedules_page = paginator.page(1)
    except EmptyPage:
        schedules_page = paginator.page(paginator.num_pages)
    
    context = {
        'schedules': schedules_page,
        'filter': filter_instance,
    }
    
    return render(request, 'exams/schedule_list.html', context)


@login_required
def schedule_detail(request, pk):
    """
    View exam schedule details
    """
    schedule = get_object_or_404(ExamSchedule, pk=pk)
    
    # Get exams in this schedule period
    exams = Exam.objects.filter(
        exam_date__gte=schedule.start_date,
        exam_date__lte=schedule.end_date,
        academic_year=schedule.academic_year,
        semester=schedule.semester
    ).order_by('exam_date', 'start_time')
    
    context = {
        'schedule': schedule,
        'exams': exams,
    }
    
    return render(request, 'exams/schedule_detail.html', context)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_exams_csv(request):
    """
    Export exams to CSV
    """
    exams = Exam.objects.select_related('course').all()
    csv_data = export_exams_to_csv(exams)
    
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="exams_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    return response


@login_required
def export_results_csv_view(request):
    """
    Export exam results to CSV
    """
    results = ExamResult.objects.select_related('exam', 'student').all()
    
    # Filter by exam if specified
    exam_id = request.GET.get('exam_id')
    if exam_id:
        results = results.filter(exam_id=exam_id)
    
    csv_data = export_results_to_csv(results)
    
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="exam_results_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    return response


@login_required
def result_card_pdf(request, student_id, exam_id):
    """
    Generate result card PDF for a student
    """
    from apps.students.models import Student
    student = get_object_or_404(Student, pk=student_id)
    exam = get_object_or_404(Exam, pk=exam_id)
    result = get_object_or_404(ExamResult, exam=exam, student=student)
    
    pdf_data = generate_result_card_pdf(result)
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="result_card_{student.roll_number}_{exam.exam_code}.pdf"'
    
    return response


# ============================================================================
# AJAX/API Operations
# ============================================================================

@login_required
def get_exam_data(request, pk):
    """
    Get exam data as JSON
    """
    exam = get_object_or_404(Exam, pk=pk)
    
    data = {
        'id': exam.id,
        'exam_code': exam.exam_code,
        'exam_name': exam.exam_name,
        'course_name': exam.course.course_name,
        'exam_date': exam.exam_date.isoformat(),
        'status': exam.status,
        'total_marks': exam.total_marks,
        'passing_marks': exam.passing_marks,
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def update_exam_status(request, pk):
    """
    Update exam status
    """
    exam = get_object_or_404(Exam, pk=pk)
    new_status = request.POST.get('status')
    
    if new_status in ['scheduled', 'ongoing', 'completed', 'cancelled']:
        try:
            exam.status = new_status
            exam.save()
            
            return JsonResponse({
                'success': True,
                'status': exam.status,
                'message': f'Status changed to {exam.get_status_display()}'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid status'}, status=400)


# ============================================================================
# Statistics and Analysis
# ============================================================================

@login_required
def analysis(request):
    """
    Exam analysis and statistics
    """
    # Overall statistics
    total_exams = Exam.objects.count()
    total_results = ExamResult.objects.count()
    
    # Pass/Fail statistics
    passed = ExamResult.objects.passed().count()
    failed = ExamResult.objects.failed().count()
    absent = ExamResult.objects.absent().count()
    
    # Grade distribution
    grade_distribution = ExamResult.objects.values('grade').annotate(
        count=Count('grade')
    ).order_by('grade')
    
    # Average marks by exam type
    avg_by_type = Exam.objects.values('exam_type').annotate(
        avg_marks=Avg('results__marks_obtained')
    )
    
    # Recent exam statistics
    recent_exams = Exam.objects.completed()[:10]
    
    context = {
        'total_exams': total_exams,
        'total_results': total_results,
        'passed': passed,
        'failed': failed,
        'absent': absent,
        'grade_distribution': grade_distribution,
        'avg_by_type': avg_by_type,
        'recent_exams': recent_exams,
    }
    
    return render(request, 'exams/analysis.html', context)


# ============================================================================
# Bulk Operations
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def bulk_result_upload(request):
    """
    Bulk upload exam results via CSV
    """
    if request.method == 'POST':
        form = BulkResultUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            exam = form.cleaned_data['exam']
            csv_file = request.FILES['csv_file']
            
            try:
                success_count, errors = process_bulk_results_csv(exam, csv_file, request.user)
                
                if errors:
                    for error in errors:
                        messages.warning(request, error)
                
                messages.success(request, f'{success_count} results uploaded successfully!')
                return redirect('exams:exam_detail', pk=exam.pk)
                
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BulkResultUploadForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'exams/bulk_upload.html', context)
