"""
Notifications Views - Complete Implementation
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
from django.contrib.auth import get_user_model
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import (
    Notification, NotificationTemplate, NotificationPreference,
    ScheduledNotification, NotificationLog, NotificationType, NotificationChannel
)
from .utils import send_notification, send_bulk_notifications

User = get_user_model()


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """Notifications dashboard"""
    user_notifications = Notification.objects.for_user(request.user)
    
    total_notifications = user_notifications.count()
    unread_count = user_notifications.unread().count()
    read_count = user_notifications.read().count()
    recent_notifications = user_notifications[:10]
    notifications_by_type = user_notifications.values('notification_type').annotate(count=Count('id'))
    
    if request.user.is_staff:
        total_system_notifications = Notification.objects.count()
        total_templates = NotificationTemplate.objects.count()
        total_scheduled = ScheduledNotification.objects.filter(is_active=True).count()
    else:
        total_system_notifications = total_templates = total_scheduled = None
    
    context = {
        'total_notifications': total_notifications,
        'unread_count': unread_count,
        'read_count': read_count,
        'recent_notifications': recent_notifications,
        'notifications_by_type': notifications_by_type,
        'total_system_notifications': total_system_notifications,
        'total_templates': total_templates,
        'total_scheduled': total_scheduled,
    }
    
    return render(request, 'notifications/dashboard.html', context)


# ============================================================================
# Notification Views
# ============================================================================

@login_required
def notification_list(request):
    """List user's notifications"""
    notifications = Notification.objects.for_user(request.user)
    
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'unread':
        notifications = notifications.unread()
    elif filter_type == 'read':
        notifications = notifications.read()
    
    notification_type = request.GET.get('type')
    if notification_type:
        notifications = notifications.by_type(notification_type)
    
    search_query = request.GET.get('search', '')
    if search_query:
        notifications = notifications.filter(
            Q(title__icontains=search_query) | Q(message__icontains=search_query)
        )
    
    sort_by = request.GET.get('sort', '-created_at')
    notifications = notifications.order_by(sort_by)
    
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    
    try:
        notifications_page = paginator.page(page)
    except PageNotAnInteger:
        notifications_page = paginator.page(1)
    except EmptyPage:
        notifications_page = paginator.page(paginator.num_pages)
    
    context = {
        'notifications': notifications_page,
        'filter_type': filter_type,
        'notification_type': notification_type,
        'search_query': search_query,
        'sort_by': sort_by,
        'notification_types': NotificationType.choices,
    }
    
    return render(request, 'notifications/notification_list.html', context)


@login_required
def notification_detail(request, pk):
    """View notification detail and mark as read"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()
    
    context = {'notification': notification}
    return render(request, 'notifications/notification_detail.html', context)


@login_required
@require_http_methods(["POST"])
def mark_as_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()
    
    return JsonResponse({'success': True, 'message': 'Notification marked as read'})


@login_required
@require_http_methods(["POST"])
def mark_as_unread(request, pk):
    """Mark notification as unread"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_unread()
    
    return JsonResponse({'success': True, 'message': 'Notification marked as unread'})


@login_required
@require_http_methods(["POST"])
def mark_all_as_read(request):
    """Mark all user's notifications as read"""
    Notification.objects.for_user(request.user).unread().mark_all_as_read()
    
    return JsonResponse({'success': True, 'message': 'All notifications marked as read'})


@login_required
@require_http_methods(["POST"])
def delete_notification(request, pk):
    """Delete a notification"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.delete()
    
    return JsonResponse({'success': True, 'message': 'Notification deleted'})


# ============================================================================
# Send Notifications (Admin)
# ============================================================================

@login_required
def send_notification_view(request):
    """Send notification to users (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('notifications:dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type', 'info')
        channels = request.POST.getlist('channels')
        recipient_ids = request.POST.getlist('recipients')
        
        if not channels:
            channels = ['in_app']
        
        try:
            recipients = User.objects.filter(id__in=recipient_ids)
            
            notifications_created = send_bulk_notifications(
                recipients=recipients,
                title=title,
                message=message,
                notification_type=notification_type,
                channels=channels,
                sender=request.user
            )
            
            messages.success(request, f'{notifications_created} notifications sent successfully!')
            return redirect('notifications:dashboard')
        except Exception as e:
            messages.error(request, f'Error sending notifications: {str(e)}')
    
    users = User.objects.filter(is_active=True)
    context = {
        'users': users,
        'notification_types': NotificationType.choices,
        'channels': NotificationChannel.choices,
    }
    
    return render(request, 'notifications/send_notification.html', context)


# ============================================================================
# Templates Views (Admin)
# ============================================================================

@login_required
def template_list(request):
    """List notification templates"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('notifications:dashboard')
    
    templates = NotificationTemplate.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        templates = templates.filter(
            Q(name__icontains=search_query) | Q(code__icontains=search_query)
        )
    
    context = {'templates': templates, 'search_query': search_query}
    return render(request, 'notifications/templates.html', context)


@login_required
def template_detail(request, pk):
    """View template detail"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('notifications:dashboard')
    
    template = get_object_or_404(NotificationTemplate, pk=pk)
    context = {'template': template}
    return render(request, 'notifications/template_detail.html', context)


# ============================================================================
# Scheduled Notifications (Admin)
# ============================================================================

@login_required
def scheduled_list(request):
    """List scheduled notifications"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('notifications:dashboard')
    
    scheduled = ScheduledNotification.objects.all()
    
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'pending':
        scheduled = scheduled.filter(is_sent=False, is_active=True)
    elif filter_type == 'sent':
        scheduled = scheduled.filter(is_sent=True)
    
    context = {'scheduled': scheduled, 'filter_type': filter_type}
    return render(request, 'notifications/scheduled.html', context)


# ============================================================================
# Preferences
# ============================================================================

@login_required
def preferences(request):
    """User notification preferences"""
    preference, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preference.enable_email = request.POST.get('enable_email') == 'on'
        preference.enable_sms = request.POST.get('enable_sms') == 'on'
        preference.enable_push = request.POST.get('enable_push') == 'on'
        preference.enable_in_app = request.POST.get('enable_in_app') == 'on'
        preference.quiet_hours_enabled = request.POST.get('quiet_hours_enabled') == 'on'
        preference.enable_daily_digest = request.POST.get('enable_daily_digest') == 'on'
        
        preference.save()
        messages.success(request, 'Preferences updated successfully!')
        return redirect('notifications:preferences')
    
    context = {'preference': preference}
    return render(request, 'notifications/settings.html', context)


# ============================================================================
# Recipients Management (Admin)
# ============================================================================

@login_required
def recipients(request):
    """Manage recipients"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('notifications:dashboard')
    
    users = User.objects.filter(is_active=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    paginator = Paginator(users, 50)
    page = request.GET.get('page')
    
    try:
        users_page = paginator.page(page)
    except PageNotAnInteger:
        users_page = paginator.page(1)
    except EmptyPage:
        users_page = paginator.page(paginator.num_pages)
    
    context = {'users': users_page, 'search_query': search_query}
    return render(request, 'notifications/recipients.html', context)


# ============================================================================
# Statistics
# ============================================================================

@login_required
def statistics(request):
    """Notification statistics"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('notifications:dashboard')
    
    total_notifications = Notification.objects.count()
    total_users = User.objects.filter(is_active=True).count()
    total_templates = NotificationTemplate.objects.count()
    total_scheduled = ScheduledNotification.objects.count()
    
    notifications_by_type = Notification.objects.values('notification_type').annotate(count=Count('id'))
    notifications_by_channel = NotificationLog.objects.values('channel').annotate(count=Count('id'))
    
    recent_logs = NotificationLog.objects.order_by('-created_at')[:20]
    
    context = {
        'total_notifications': total_notifications,
        'total_users': total_users,
        'total_templates': total_templates,
        'total_scheduled': total_scheduled,
        'notifications_by_type': notifications_by_type,
        'notifications_by_channel': notifications_by_channel,
        'recent_logs': recent_logs,
    }
    
    return render(request, 'notifications/statistics.html', context)


# ============================================================================
# Export
# ============================================================================

@login_required
def export_csv(request):
    """Export notifications to CSV"""
    notifications = Notification.objects.for_user(request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="notifications_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Message', 'Type', 'Read', 'Created At'])
    
    for notification in notifications:
        writer.writerow([
            notification.title,
            notification.message,
            notification.notification_type,
            'Yes' if notification.is_read else 'No',
            notification.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response


# ============================================================================
# AJAX API
# ============================================================================

@login_required
def get_unread_count(request):
    """Get unread notifications count"""
    count = Notification.objects.for_user(request.user).unread().count()
    return JsonResponse({'count': count})


@login_required
def get_recent_notifications(request):
    """Get recent notifications"""
    limit = int(request.GET.get('limit', 5))
    notifications = Notification.objects.for_user(request.user)[:limit]
    
    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.notification_type,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat(),
        'action_url': n.action_url,
    } for n in notifications]
    
    return JsonResponse({'notifications': data})
