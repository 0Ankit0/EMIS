"""
Attendance Views - Complete Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from datetime import timedelta, date
import json

from .models import AttendanceRecord, AttendanceSession, AttendancePolicy, AttendanceReport
from .forms import AttendanceRecordForm, AttendanceSessionForm, AttendancePolicyForm, BulkAttendanceForm
from .filters import AttendanceRecordFilter, AttendanceSessionFilter


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """
    Attendance dashboard with statistics
    """
    today = timezone.now().date()
    
    # Get today's sessions
    today_sessions = AttendanceSession.objects.filter(date=today)
    
    # Get statistics
    total_sessions_today = today_sessions.count()
    completed_sessions = today_sessions.filter(status='completed').count()
    in_progress_sessions = today_sessions.filter(status='in_progress').count()
    
    # Recent records
    recent_records = AttendanceRecord.objects.select_related(
        'student', 'course'
    ).order_by('-created_at')[:10]
    
    # Attendance statistics
    week_ago = today - timedelta(days=7)
    week_records = AttendanceRecord.objects.filter(date__gte=week_ago)
    
    total_records = week_records.count()
    present_count = week_records.filter(status='present').count()
    absent_count = week_records.filter(status__in=['absent', 'sick_leave']).count()
    late_count = week_records.filter(status='late').count()
    
    attendance_rate = round((present_count / total_records * 100) if total_records > 0 else 0, 2)
    
    context = {
        'today_sessions': today_sessions,
        'total_sessions_today': total_sessions_today,
        'completed_sessions': completed_sessions,
        'in_progress_sessions': in_progress_sessions,
        'recent_records': recent_records,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'attendance_rate': attendance_rate,
    }
    
    return render(request, 'attendance/dashboard.html', context)


# ============================================================================
# Attendance Record Views
# ============================================================================

@login_required
def record_list(request):
    """List all attendance records with filtering"""
    records = AttendanceRecord.objects.select_related(
        'student', 'course', 'session'
    ).all()
    
    # Apply filters
    filter_instance = AttendanceRecordFilter(request.GET, queryset=records)
    records = filter_instance.qs
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        records = records.filter(
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query) |
            Q(course__name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(records, 20)
    page = request.GET.get('page')
    records_page = paginator.get_page(page)
    
    context = {
        'records': records_page,
        'filter': filter_instance,
        'search_query': search_query,
    }
    
    return render(request, 'attendance/record_list.html', context)


@login_required
def record_detail(request, pk):
    """View attendance record details"""
    record = get_object_or_404(
        AttendanceRecord.objects.select_related('student', 'course', 'session'),
        pk=pk
    )
    
    context = {
        'record': record,
    }
    
    return render(request, 'attendance/record_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def record_create(request):
    """Create new attendance record"""
    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    record = form.save(commit=False)
                    record.marked_by = request.user
                    record.save()
                    
                    # Update session counts if applicable
                    if record.session:
                        record.session.update_counts()
                    
                    messages.success(request, 'Attendance record created successfully!')
                    return redirect('attendance:record_detail', pk=record.pk)
                    
            except Exception as e:
                messages.error(request, f'Error creating record: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AttendanceRecordForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'attendance/record_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def record_update(request, pk):
    """Update attendance record"""
    record = get_object_or_404(AttendanceRecord, pk=pk)
    
    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, request.FILES, instance=record)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_record = form.save()
                    
                    # Update session counts
                    if updated_record.session:
                        updated_record.session.update_counts()
                    
                    messages.success(request, 'Attendance record updated successfully!')
                    return redirect('attendance:record_detail', pk=updated_record.pk)
                    
            except Exception as e:
                messages.error(request, f'Error updating record: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AttendanceRecordForm(instance=record)
    
    context = {
        'form': form,
        'record': record,
        'action': 'Update',
    }
    
    return render(request, 'attendance/record_form.html', context)


@login_required
@require_http_methods(["POST"])
def record_delete(request, pk):
    """Delete attendance record"""
    record = get_object_or_404(AttendanceRecord, pk=pk)
    
    try:
        session = record.session
        record.delete()
        
        # Update session counts
        if session:
            session.update_counts()
        
        messages.success(request, 'Attendance record deleted successfully!')
        return redirect('attendance:record_list')
    except Exception as e:
        messages.error(request, f'Error deleting record: {str(e)}')
        return redirect('attendance:record_detail', pk=pk)


# ============================================================================
# Attendance Session Views
# ============================================================================

@login_required
def session_list(request):
    """List all attendance sessions"""
    sessions = AttendanceSession.objects.select_related(
        'course', 'instructor'
    ).all()
    
    # Apply filters
    filter_instance = AttendanceSessionFilter(request.GET, queryset=sessions)
    sessions = filter_instance.qs
    
    # Pagination
    paginator = Paginator(sessions, 20)
    page = request.GET.get('page')
    sessions_page = paginator.get_page(page)
    
    context = {
        'sessions': sessions_page,
        'filter': filter_instance,
    }
    
    return render(request, 'attendance/session_list.html', context)


@login_required
def session_detail(request, pk):
    """View session details with attendance records"""
    session = get_object_or_404(
        AttendanceSession.objects.select_related('course', 'instructor'),
        pk=pk
    )
    
    # Get all records for this session
    records = session.records.select_related('student').all()
    
    context = {
        'session': session,
        'records': records,
        'attendance_rate': session.get_attendance_rate(),
    }
    
    return render(request, 'attendance/session_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def session_create(request):
    """Create new attendance session"""
    if request.method == 'POST':
        form = AttendanceSessionForm(request.POST)
        
        if form.is_valid():
            try:
                session = form.save()
                messages.success(request, 'Attendance session created successfully!')
                return redirect('attendance:session_detail', pk=session.pk)
            except Exception as e:
                messages.error(request, f'Error creating session: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AttendanceSessionForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'attendance/session_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def session_update(request, pk):
    """Update attendance session"""
    session = get_object_or_404(AttendanceSession, pk=pk)
    
    if request.method == 'POST':
        form = AttendanceSessionForm(request.POST, instance=session)
        
        if form.is_valid():
            try:
                updated_session = form.save()
                messages.success(request, 'Session updated successfully!')
                return redirect('attendance:session_detail', pk=updated_session.pk)
            except Exception as e:
                messages.error(request, f'Error updating session: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AttendanceSessionForm(instance=session)
    
    context = {
        'form': form,
        'session': session,
        'action': 'Update',
    }
    
    return render(request, 'attendance/session_form.html', context)


# ============================================================================
# Bulk Operations
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def bulk_mark_attendance(request, session_id):
    """Bulk mark attendance for a session"""
    session = get_object_or_404(AttendanceSession, pk=session_id)
    
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST, session=session)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Process bulk attendance
                    attendance_data = form.cleaned_data['attendance_data']
                    
                    for student_id, status in attendance_data.items():
                        AttendanceRecord.objects.update_or_create(
                            student_id=student_id,
                            course=session.course,
                            date=session.date,
                            defaults={
                                'status': status,
                                'session': session,
                                'marked_by': request.user,
                            }
                        )
                    
                    # Update session counts
                    session.update_counts()
                    session.status = 'completed'
                    session.save()
                    
                    messages.success(request, 'Attendance marked successfully!')
                    return redirect('attendance:session_detail', pk=session.pk)
                    
            except Exception as e:
                messages.error(request, f'Error marking attendance: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Get enrolled students for the course
        from apps.students.models import Student
        students = Student.objects.filter(
            enrollments__course=session.course,
            enrollments__status='active'
        ).distinct()
        
        form = BulkAttendanceForm(session=session, students=students)
    
    context = {
        'form': form,
        'session': session,
    }
    
    return render(request, 'attendance/bulk_mark.html', context)


# ============================================================================
# Reports
# ============================================================================

@login_required
def student_attendance_report(request, student_id):
    """Generate attendance report for a student"""
    from apps.students.models import Student
    student = get_object_or_404(Student, pk=student_id)
    
    # Get date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
    
    # Get records
    records = AttendanceRecord.objects.filter(
        student=student,
        date__gte=start_date,
        date__lte=end_date
    ).select_related('course')
    
    # Calculate statistics
    total = records.count()
    present = records.filter(status='present').count()
    absent = records.filter(status__in=['absent', 'sick_leave']).count()
    late = records.filter(status='late').count()
    
    attendance_rate = round((present / total * 100) if total > 0 else 0, 2)
    
    context = {
        'student': student,
        'records': records,
        'start_date': start_date,
        'end_date': end_date,
        'total': total,
        'present': present,
        'absent': absent,
        'late': late,
        'attendance_rate': attendance_rate,
    }
    
    return render(request, 'attendance/student_report.html', context)


@login_required
def course_attendance_report(request, course_id):
    """Generate attendance report for a course"""
    from apps.courses.models import Course
    course = get_object_or_404(Course, pk=course_id)
    
    # Get date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
    
    # Get sessions
    sessions = AttendanceSession.objects.filter(
        course=course,
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Calculate statistics
    total_sessions = sessions.count()
    avg_attendance = sessions.aggregate(
        avg_rate=Avg('present_count')
    )['avg_rate'] or 0
    
    context = {
        'course': course,
        'sessions': sessions,
        'start_date': start_date,
        'end_date': end_date,
        'total_sessions': total_sessions,
        'avg_attendance': round(avg_attendance, 2),
    }
    
    return render(request, 'attendance/course_report.html', context)


# ============================================================================
# API Endpoints
# ============================================================================

@login_required
def api_mark_attendance(request):
    """API endpoint to mark attendance"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            record, created = AttendanceRecord.objects.update_or_create(
                student_id=data['student_id'],
                course_id=data['course_id'],
                date=data['date'],
                defaults={
                    'status': data['status'],
                    'marked_by': request.user,
                }
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Attendance marked successfully',
                'record_id': str(record.id)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def api_session_stats(request, session_id):
    """Get real-time session statistics"""
    session = get_object_or_404(AttendanceSession, pk=session_id)
    
    data = {
        'total_students': session.total_students,
        'present': session.present_count,
        'absent': session.absent_count,
        'late': session.late_count,
        'attendance_rate': session.get_attendance_rate(),
    }
    
    return JsonResponse(data)
