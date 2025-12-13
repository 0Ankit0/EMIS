"""
Timetable Views - Complete Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape

from .models import (
    AcademicYear, Semester, TimeSlot, Room,
    TimetableEntry, TimetableException
)
from .forms import (
    AcademicYearForm, SemesterForm, TimeSlotForm,
    RoomForm, TimetableEntryForm, TimetableExceptionForm
)


# ============================================================================
# Dashboard
# ============================================================================

@login_required
def dashboard(request):
    """Timetable dashboard"""
    active_semester = Semester.objects.filter(is_active=True).first()
    
    stats = {
        'total_entries': TimetableEntry.objects.filter(is_active=True).count(),
        'total_rooms': Room.objects.filter(is_active=True).count(),
        'total_time_slots': TimeSlot.objects.filter(is_active=True).count(),
        'active_semester': active_semester,
    }
    
    if active_semester:
        stats['semester_entries'] = TimetableEntry.objects.filter(
            semester=active_semester,
            is_active=True
        ).count()
    
    recent_entries = TimetableEntry.objects.select_related(
        'course', 'room', 'instructor', 'time_slot'
    ).filter(is_active=True)[:10]
    
    context = {
        'stats': stats,
        'recent_entries': recent_entries,
        'title': 'Timetable Dashboard',
    }
    
    return render(request, timetable/dashboard.htmltimetable/'timetable/dashboard.html, context)


# ============================================================================
# Timetable Entry Views
# ============================================================================

@login_required
def timetable_list(request):
    """List all timetable entries"""
    entries = TimetableEntry.objects.select_related(
        'semester', 'course', 'time_slot', 'room', 'instructor'
    ).filter(is_active=True)
    
    # Filter by semester
    semester_id = request.GET.get('semester')
    if semester_id:
        entries = entries.filter(semester_id=semester_id)
    else:
        active_semester = Semester.objects.filter(is_active=True).first()
        if active_semester:
            entries = entries.filter(semester=active_semester)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        entries = entries.filter(
            Q(course__code__icontains=search_query) |
            Q(course__title__icontains=search_query) |
            Q(section__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(entries, 50)
    page = request.GET.get('page')
    entries_page = paginator.get_page(page)
    
    semesters = Semester.objects.all().order_by('-start_date')
    
    context = {
        'entries': entries_page,
        'semesters': semesters,
        'search_query': search_query,
        'title': 'Timetable Entries',
    }
    
    return render(request, timetable/view_timetable.htmltimetable/'timetable/view_timetable.html, context)


@login_required
def timetable_create(request):
    """Create timetable entry"""
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    entry = form.save(commit=False)
                    entry.created_by = request.user
                    entry.full_clean()  # Validate conflicts
                    entry.save()
                    
                    messages.success(request, 'Timetable entry created successfully!')
                    return redirect('timetable:list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TimetableEntryForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Timetable Entry',
    }
    
    return render(request, timetable/create_timetable.htmltimetable/'timetable/create_timetable.html, context)


@login_required
def timetable_update(request, pk):
    """Update timetable entry"""
    entry = get_object_or_404(TimetableEntry, pk=pk)
    
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST, instance=entry)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Timetable entry updated successfully!')
                return redirect('timetable:list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = TimetableEntryForm(instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'action': 'Update',
        'title': 'Update Timetable Entry',
    }
    
    return render(request, timetable/create_timetable.htmltimetable/'timetable/create_timetable.html, context)


@login_required
@require_http_methods(["POST"])
def timetable_delete(request, pk):
    """Delete timetable entry"""
    entry = get_object_or_404(TimetableEntry, pk=pk)
    entry.delete()
    messages.success(request, 'Timetable entry deleted successfully!')
    return redirect('timetable:list')


# ============================================================================
# View Schedules
# ============================================================================

@login_required
def class_schedule(request):
    """View schedule for a specific class/section"""
    semester_id = request.GET.get('semester')
    section = request.GET.get('section', '')
    batch = request.GET.get('batch', '')
    
    entries = TimetableEntry.objects.select_related(
        'course', 'time_slot', 'room', 'instructor'
    ).filter(is_active=True)
    
    if semester_id:
        entries = entries.filter(semester_id=semester_id)
    
    if section:
        entries = entries.filter(section=section)
    
    if batch:
        entries = entries.filter(batch=batch)
    
    # Organize by day and time
    schedule = {}
    for day in range(7):
        schedule[day] = entries.filter(time_slot__day_of_week=day).order_by('time_slot__start_time')
    
    semesters = Semester.objects.all().order_by('-start_date')
    
    context = {
        'schedule': schedule,
        'semesters': semesters,
        'section': section,
        'batch': batch,
        'title': 'Class Schedule',
    }
    
    return render(request, timetable/class_schedule.htmltimetable/'timetable/class_schedule.html, context)


@login_required
def teacher_schedule(request):
    """View schedule for a specific teacher"""
    instructor_id = request.GET.get('instructor')
    semester_id = request.GET.get('semester')
    
    entries = TimetableEntry.objects.select_related(
        'course', 'time_slot', 'room'
    ).filter(is_active=True)
    
    if instructor_id:
        entries = entries.filter(instructor_id=instructor_id)
    
    if semester_id:
        entries = entries.filter(semester_id=semester_id)
    
    # Organize by day and time
    schedule = {}
    for day in range(7):
        schedule[day] = entries.filter(time_slot__day_of_week=day).order_by('time_slot__start_time')
    
    context = {
        'schedule': schedule,
        'title': 'Teacher Schedule',
    }
    
    return render(request, timetable/teacher_schedule.htmltimetable/'timetable/teacher_schedule.html, context)


@login_required
def room_allocation(request):
    """View room allocation/utilization"""
    semester_id = request.GET.get('semester')
    room_id = request.GET.get('room')
    
    entries = TimetableEntry.objects.select_related(
        'course', 'time_slot', 'instructor'
    ).filter(is_active=True)
    
    if semester_id:
        entries = entries.filter(semester_id=semester_id)
    
    if room_id:
        entries = entries.filter(room_id=room_id)
    
    # Group by room
    rooms = Room.objects.filter(is_active=True).prefetch_related(
        Prefetch('timetable_entries', queryset=entries)
    )
    
    context = {
        'rooms': rooms,
        'entries': entries,
        'title': 'Room Allocation',
    }
    
    return render(request, timetable/room_allocation.htmltimetable/'timetable/room_allocation.html, context)


# ============================================================================
# Supporting Model Views
# ============================================================================

@login_required
def room_list(request):
    """List all rooms"""
    rooms = Room.objects.filter(is_active=True)
    
    context = {
        'rooms': rooms,
        'title': 'Rooms',
    }
    
    return render(request, timetable/room_list.htmltimetable/'timetable/room_list.html, context)


@login_required
def room_create(request):
    """Create room"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully!')
            return redirect('timetable:room_list')
    else:
        form = RoomForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Room',
    }
    
    return render(request, timetable/room_form.htmltimetable/'timetable/room_form.html, context)


@login_required
def timeslot_list(request):
    """List all time slots"""
    slots = TimeSlot.objects.filter(is_active=True).order_by('day_of_week', 'start_time')
    
    context = {
        'slots': slots,
        'title': 'Time Slots',
    }
    
    return render(request, timetable/timeslot_list.htmltimetable/'timetable/timeslot_list.html, context)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_csv(request):
    """Export timetable to CSV"""
    semester_id = request.GET.get('semester')
    
    entries = TimetableEntry.objects.select_related(
        'semester', 'course', 'time_slot', 'room', 'instructor'
    ).filter(is_active=True)
    
    if semester_id:
        entries = entries.filter(semester_id=semester_id)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="timetable_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Course', 'Day', 'Time', 'Room', 'Instructor', 'Section', 'Type'])
    
    for entry in entries:
        writer.writerow([
            entry.course.code,
            entry.time_slot.get_day_of_week_display(),
            f"{entry.time_slot.start_time} - {entry.time_slot.end_time}",
            entry.room.name if entry.room else 'N/A',
            entry.instructor.get_full_name() if entry.instructor else 'N/A',
            entry.section or 'N/A',
            entry.session_type,
        ])
    
    return response


@login_required
def export_pdf(request):
    """Export timetable to PDF"""
    semester_id = request.GET.get('semester')
    
    entries = TimetableEntry.objects.select_related(
        'semester', 'course', 'time_slot', 'room', 'instructor'
    ).filter(is_active=True)
    
    if semester_id:
        entries = entries.filter(semester_id=semester_id)
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 550, 'Timetable')
    
    p.setFont("Helvetica", 10)
    y = 520
    
    for entry in entries[:30]:
        text = f"{entry.course.code} - {entry.time_slot} - {entry.room}"
        p.drawString(50, y, text)
        y -= 15
        
        if y < 50:
            p.showPage()
            y = 550
    
    p.save()
    
    pdf_data = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="timetable_{timezone.now().strftime("%Y%m%d")}.pdf"'
    
    return response


# ============================================================================
# AJAX Operations
# ============================================================================

@login_required
def check_conflict(request):
    """Check for timetable conflicts"""
    semester_id = request.GET.get('semester')
    time_slot_id = request.GET.get('time_slot')
    room_id = request.GET.get('room')
    instructor_id = request.GET.get('instructor')
    
    conflicts = []
    
    if room_id and time_slot_id and semester_id:
        room_conflict = TimetableEntry.objects.filter(
            semester_id=semester_id,
            time_slot_id=time_slot_id,
            room_id=room_id,
            is_active=True
        ).exists()
        
        if room_conflict:
            conflicts.append('Room is already booked for this time slot')
    
    if instructor_id and time_slot_id and semester_id:
        instructor_conflict = TimetableEntry.objects.filter(
            semester_id=semester_id,
            time_slot_id=time_slot_id,
            instructor_id=instructor_id,
            is_active=True
        ).exists()
        
        if instructor_conflict:
            conflicts.append('Instructor already has a class at this time')
    
    return JsonResponse({
        'has_conflict': len(conflicts) > 0,
        'conflicts': conflicts
    })
