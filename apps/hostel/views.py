"""Hostel Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import csv

from .models import (
    Hostel, Floor, Room, RoomAllocation, HostelFee, MessMenu,
    VisitorLog, Complaint, OutingRequest, Attendance
)
from .forms import (
    HostelForm, RoomForm, RoomAllocationForm, ComplaintForm,
    OutingRequestForm, AttendanceForm
)


@login_required
def dashboard(request):
    """Hostel dashboard"""
    stats = {
        'total_hostels': Hostel.objects.active().count(),
        'total_rooms': Room.objects.count(),
        'occupied_rooms': Room.objects.filter(status='occupied').count(),
        'total_capacity': Hostel.objects.aggregate(Sum('total_capacity'))['total_capacity__sum'] or 0,
        'occupied_capacity': Hostel.objects.aggregate(Sum('occupied_capacity'))['occupied_capacity__sum'] or 0,
        'active_allocations': RoomAllocation.objects.active().count(),
        'pending_complaints': Complaint.objects.pending().count(),
        'pending_outings': OutingRequest.objects.pending().count(),
    }
    
    recent_allocations = RoomAllocation.objects.all()[:10]
    recent_complaints = Complaint.objects.all()[:10]
    
    context = {
        'stats': stats,
        'recent_allocations': recent_allocations,
        'recent_complaints': recent_complaints,
    }
    return render(request, 'hostel/dashboard.html', context)


@login_required
def hostel_list(request):
    """List all hostels"""
    hostels = Hostel.objects.all()
    
    # Filter
    hostel_type = request.GET.get('type')
    if hostel_type:
        hostels = hostels.filter(hostel_type=hostel_type)
    
    search = request.GET.get('search')
    if search:
        hostels = hostels.filter(
            Q(name__icontains=search) | Q(code__icontains=search)
        )
    
    context = {'hostels': hostels}
    return render(request, 'hostel/hostel_list.html', context)


@login_required
def hostel_detail(request, pk):
    """Hostel detail view"""
    hostel = get_object_or_404(Hostel, pk=pk)
    
    rooms = hostel.rooms.all()
    allocations = RoomAllocation.objects.filter(room__hostel=hostel, status='active')
    
    context = {
        'hostel': hostel,
        'rooms': rooms,
        'allocations': allocations,
    }
    return render(request, 'hostel/hostel_detail.html', context)


@login_required
def room_list(request):
    """List all rooms"""
    rooms = Room.objects.all()
    
    # Filters
    hostel_id = request.GET.get('hostel')
    if hostel_id:
        rooms = rooms.filter(hostel_id=hostel_id)
    
    status_filter = request.GET.get('status')
    if status_filter:
        rooms = rooms.filter(status=status_filter)
    
    paginator = Paginator(rooms, 20)
    page = request.GET.get('page')
    rooms_page = paginator.get_page(page)
    
    context = {
        'rooms': rooms_page,
        'hostels': Hostel.objects.active(),
    }
    return render(request, 'hostel/room_list.html', context)


@login_required
def room_allocation_create(request):
    """Create room allocation"""
    if request.method == 'POST':
        form = RoomAllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.allocated_by = request.user
            allocation.save()
            
            # Update room occupancy
            room = allocation.room
            room.occupied_beds += 1
            if room.occupied_beds >= room.capacity:
                room.status = 'full'
            room.save()
            
            messages.success(request, 'Room allocated successfully!')
            return redirect('hostel:allocation_list')
    else:
        form = RoomAllocationForm()
    
    context = {'form': form}
    return render(request, 'hostel/allocation_form.html', context)


@login_required
def allocation_list(request):
    """List all allocations"""
    allocations = RoomAllocation.objects.all()
    
    # Filter
    status_filter = request.GET.get('status')
    if status_filter:
        allocations = allocations.filter(status=status_filter)
    
    paginator = Paginator(allocations, 20)
    page = request.GET.get('page')
    allocations_page = paginator.get_page(page)
    
    context = {'allocations': allocations_page}
    return render(request, 'hostel/allocation_list.html', context)


@login_required
def complaint_list(request):
    """List all complaints"""
    complaints = Complaint.objects.all()
    
    # Filter
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    paginator = Paginator(complaints, 20)
    page = request.GET.get('page')
    complaints_page = paginator.get_page(page)
    
    context = {'complaints': complaints_page}
    return render(request, 'hostel/complaint_list.html', context)


@login_required
def complaint_create(request):
    """Create new complaint"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            # Assume student is linked to user
            # complaint.student = request.user.student_profile
            complaint.save()
            messages.success(request, f'Complaint {complaint.complaint_number} submitted successfully!')
            return redirect('hostel:complaint_list')
    else:
        form = ComplaintForm()
    
    context = {'form': form}
    return render(request, 'hostel/complaint_form.html', context)


@login_required
def outing_request_list(request):
    """List all outing requests"""
    requests_qs = OutingRequest.objects.all()
    
    # Filter
    status_filter = request.GET.get('status')
    if status_filter:
        requests_qs = requests_qs.filter(status=status_filter)
    
    paginator = Paginator(requests_qs, 20)
    page = request.GET.get('page')
    requests_page = paginator.get_page(page)
    
    context = {'outing_requests': requests_page}
    return render(request, 'hostel/outing_request_list.html', context)


@login_required
def outing_request_create(request):
    """Create outing request"""
    if request.method == 'POST':
        form = OutingRequestForm(request.POST)
        if form.is_valid():
            outing = form.save(commit=False)
            # outing.student = request.user.student_profile
            outing.save()
            messages.success(request, 'Outing request submitted successfully!')
            return redirect('hostel:outing_request_list')
    else:
        form = OutingRequestForm()
    
    context = {'form': form}
    return render(request, 'hostel/outing_request_form.html', context)


@login_required
def mess_menu(request, hostel_id):
    """View mess menu for a hostel"""
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    menus = MessMenu.objects.filter(hostel=hostel, is_active=True).order_by('day_of_week', 'meal_type')
    
    # Organize by day and meal
    organized_menus = {}
    for menu in menus:
        day = menu.get_day_of_week_display()
        if day not in organized_menus:
            organized_menus[day] = {}
        organized_menus[day][menu.get_meal_type_display()] = menu
    
    context = {
        'hostel': hostel,
        'organized_menus': organized_menus,
    }
    return render(request, 'hostel/mess_menu.html', context)


@login_required
def visitor_logs(request, hostel_id):
    """View visitor logs for a hostel"""
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    logs = VisitorLog.objects.filter(hostel=hostel).order_by('-entry_time')[:50]
    
    context = {
        'hostel': hostel,
        'visitor_logs': logs,
    }
    return render(request, 'hostel/visitor_logs.html', context)


@login_required
def export_allocations_csv(request):
    """Export room allocations to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="room_allocations_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student', 'Room', 'Hostel', 'Allocation Date', 'Monthly Rent', 'Status'])
    
    allocations = RoomAllocation.objects.filter(status='active')
    for allocation in allocations:
        writer.writerow([
            allocation.student.user.email,
            allocation.room.room_number,
            allocation.room.hostel.name,
            allocation.allocation_date,
            allocation.monthly_rent,
            allocation.get_status_display()
        ])
    
    return response
