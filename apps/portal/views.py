from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import (
    Dashboard, Widget, QuickLink, Announcement, AnnouncementView,
    StudentPortalProfile, FacultyPortalProfile, PortalActivity
)
from .forms import (
    DashboardForm, AnnouncementForm, StudentPortalProfileForm,
    FacultyPortalProfileForm, ProfilePictureUploadForm
)
from apps.students.models import Student
from apps.faculty.models import Faculty


@login_required
def portal_home(request):
    """Main portal home page"""
    user = request.user
    
    # Get or create dashboard
    dashboard, created = Dashboard.objects.get_or_create(
        user=user,
        defaults={'role': get_user_role(user)}
    )
    
    # Get active widgets for user role
    widgets = Widget.objects.filter(is_active=True, roles__contains=dashboard.role)
    
    # Get quick links
    quick_links = QuickLink.objects.filter(is_active=True, roles__contains=dashboard.role)
    
    # Get active announcements
    now = timezone.now()
    announcements = Announcement.objects.filter(
        Q(is_published=True) &
        Q(Q(publish_date__lte=now) | Q(publish_date__isnull=True)) &
        Q(Q(expiry_date__gte=now) | Q(expiry_date__isnull=True)) &
        Q(target_roles__contains=dashboard.role)
    ).order_by('-priority', '-created_at')[:5]
    
    # Log activity
    log_activity(request, 'view_page', 'Visited portal home')
    
    context = {
        'dashboard': dashboard,
        'widgets': widgets,
        'quick_links': quick_links,
        'announcements': announcements,
    }
    
    return render(request, 'portal/home.html', context)


@login_required
def student_dashboard(request):
    """Student dashboard"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('portal:home')
    
    # Get or create portal profile
    profile, created = StudentPortalProfile.objects.get_or_create(student=student)
    
    # Update last login
    profile.last_login = timezone.now()
    profile.login_count += 1
    profile.save()
    
    # Get dashboard data
    dashboard = Dashboard.objects.filter(user=request.user).first()
    widgets = Widget.objects.filter(is_active=True, roles__contains='student')
    quick_links = QuickLink.objects.filter(is_active=True, roles__contains='student')
    
    context = {
        'student': student,
        'profile': profile,
        'dashboard': dashboard,
        'widgets': widgets,
        'quick_links': quick_links,
    }
    
    return render(request, 'portal/student/dashboard.html', context)


@login_required
def faculty_dashboard(request):
    """Faculty dashboard"""
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, "Faculty profile not found.")
        return redirect('portal:home')
    
    # Get or create portal profile
    profile, created = FacultyPortalProfile.objects.get_or_create(faculty=faculty)
    
    # Update last login
    profile.last_login = timezone.now()
    profile.login_count += 1
    profile.save()
    
    # Get dashboard data
    dashboard = Dashboard.objects.filter(user=request.user).first()
    widgets = Widget.objects.filter(is_active=True, roles__contains='faculty')
    quick_links = QuickLink.objects.filter(is_active=True, roles__contains='faculty')
    
    context = {
        'faculty': faculty,
        'profile': profile,
        'dashboard': dashboard,
        'widgets': widgets,
        'quick_links': quick_links,
    }
    
    return render(request, 'portal/faculty/dashboard.html', context)


@login_required
def announcements_list(request):
    """List all announcements"""
    user = request.user
    role = get_user_role(user)
    
    now = timezone.now()
    announcements = Announcement.objects.filter(
        Q(is_published=True) &
        Q(Q(publish_date__lte=now) | Q(publish_date__isnull=True)) &
        Q(Q(expiry_date__gte=now) | Q(expiry_date__isnull=True)) &
        Q(target_roles__contains=role)
    ).order_by('-priority', '-created_at')
    
    context = {
        'announcements': announcements,
    }
    
    return render(request, 'portal/announcements/list.html', context)


@login_required
def announcement_detail(request, pk):
    """View announcement details"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    # Create view record
    view, created = AnnouncementView.objects.get_or_create(
        announcement=announcement,
        user=request.user
    )
    
    # Update view count
    if created:
        announcement.views_count += 1
        announcement.save()
    
    context = {
        'announcement': announcement,
    }
    
    return render(request, 'portal/announcements/detail.html', context)


@login_required
def profile_settings(request):
    """User profile settings"""
    user = request.user
    role = get_user_role(user)
    
    if role == 'student':
        student = Student.objects.get(user=user)
        profile, created = StudentPortalProfile.objects.get_or_create(student=student)
        
        if request.method == 'POST':
            form = StudentPortalProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('portal:profile_settings')
        else:
            form = StudentPortalProfileForm(instance=profile)
            
    elif role == 'faculty':
        faculty = Faculty.objects.get(user=user)
        profile, created = FacultyPortalProfile.objects.get_or_create(faculty=faculty)
        
        if request.method == 'POST':
            form = FacultyPortalProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('portal:profile_settings')
        else:
            form = FacultyPortalProfileForm(instance=profile)
    else:
        messages.error(request, "Profile type not supported.")
        return redirect('portal:home')
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'portal/settings/profile.html', context)


@login_required
def dashboard_settings(request):
    """Dashboard configuration settings"""
    dashboard, created = Dashboard.objects.get_or_create(
        user=request.user,
        defaults={'role': get_user_role(request.user)}
    )
    
    if request.method == 'POST':
        form = DashboardForm(request.POST, instance=dashboard)
        if form.is_valid():
            form.save()
            messages.success(request, "Dashboard settings updated successfully.")
            return redirect('portal:dashboard_settings')
    else:
        form = DashboardForm(instance=dashboard)
    
    context = {
        'form': form,
        'dashboard': dashboard,
    }
    
    return render(request, 'portal/settings/dashboard.html', context)


@login_required
def activity_log(request):
    """View user activity log"""
    activities = PortalActivity.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    context = {
        'activities': activities,
    }
    
    return render(request, 'portal/activity_log.html', context)


# Helper functions

def get_user_role(user):
    """Determine user role"""
    if hasattr(user, 'student_profile'):
        return 'student'
    elif hasattr(user, 'faculty_profile'):
        return 'faculty'
    elif user.is_staff or user.is_superuser:
        return 'admin'
    return 'student'


def log_activity(request, activity_type, description, metadata=None):
    """Log user activity"""
    if request.user.is_authenticated:
        PortalActivity.objects.create(
            user=request.user,
            activity_type=activity_type,
            description=description,
            metadata=metadata or {},
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
