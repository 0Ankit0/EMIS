from .models import Dashboard, Announcement, QuickLink


def portal_context(request):
    """Add portal-specific context to all templates"""
    context = {}
    
    if request.user.is_authenticated:
        # Get user dashboard
        try:
            dashboard = Dashboard.objects.get(user=request.user)
            context['user_dashboard'] = dashboard
        except Dashboard.DoesNotExist:
            context['user_dashboard'] = None
        
        # Get unread announcements count
        from django.utils import timezone
        from django.db.models import Q
        from .models import AnnouncementView
        
        now = timezone.now()
        role = get_user_role(request.user)
        
        all_announcements = Announcement.objects.filter(
            Q(is_published=True) &
            Q(Q(publish_date__lte=now) | Q(publish_date__isnull=True)) &
            Q(Q(expiry_date__gte=now) | Q(expiry_date__isnull=True)) &
            Q(target_roles__contains=role)
        )
        
        read_announcements = AnnouncementView.objects.filter(
            user=request.user
        ).values_list('announcement_id', flat=True)
        
        unread_count = all_announcements.exclude(id__in=read_announcements).count()
        context['unread_announcements_count'] = unread_count
        
        # Get quick links for user role
        quick_links = QuickLink.objects.filter(
            is_active=True,
            roles__contains=role
        ).order_by('order')[:5]
        context['portal_quick_links'] = quick_links
    
    return context


def get_user_role(user):
    """Determine user role"""
    if hasattr(user, 'student_profile'):
        return 'student'
    elif hasattr(user, 'faculty_profile'):
        return 'faculty'
    elif user.is_staff or user.is_superuser:
        return 'admin'
    return 'student'
