from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import (
    Dashboard, Widget, QuickLink, Announcement, AnnouncementView,
    StudentPortalProfile, FacultyPortalProfile, PortalActivity, PortalSettings
)
from .serializers import (
    DashboardSerializer, WidgetSerializer, QuickLinkSerializer,
    AnnouncementSerializer, AnnouncementViewSerializer,
    StudentPortalProfileSerializer, FacultyPortalProfileSerializer,
    PortalActivitySerializer, PortalSettingsSerializer
)


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Dashboard.objects.all()
        return Dashboard.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_dashboard(self, request):
        dashboard, created = Dashboard.objects.get_or_create(
            user=request.user,
            defaults={'role': self.get_user_role(request.user)}
        )
        serializer = self.get_serializer(dashboard)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_layout(self, request, pk=None):
        dashboard = self.get_object()
        layout_config = request.data.get('layout_config', {})
        dashboard.layout_config = layout_config
        dashboard.save()
        return Response({'status': 'layout updated'})
    
    @action(detail=True, methods=['post'])
    def update_theme(self, request, pk=None):
        dashboard = self.get_object()
        theme_settings = request.data.get('theme_settings', {})
        dashboard.theme_settings = theme_settings
        dashboard.save()
        return Response({'status': 'theme updated'})
    
    def get_user_role(self, user):
        if hasattr(user, 'student_profile'):
            return 'student'
        elif hasattr(user, 'faculty_profile'):
            return 'faculty'
        elif user.is_staff:
            return 'admin'
        return 'student'


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        queryset = Widget.objects.filter(is_active=True)
        if role:
            queryset = queryset.filter(roles__contains=role)
        return queryset.order_by('order', 'name')


class QuickLinkViewSet(viewsets.ModelViewSet):
    queryset = QuickLink.objects.all()
    serializer_class = QuickLinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        category = self.request.query_params.get('category', None)
        
        queryset = QuickLink.objects.filter(is_active=True)
        
        if role:
            queryset = queryset.filter(roles__contains=role)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('order', 'title')


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Announcement.objects.all()
        
        # Get user role
        role = self.get_user_role(self.request.user)
        
        # Filter active announcements for user role
        now = timezone.now()
        queryset = Announcement.objects.filter(
            Q(is_published=True) &
            Q(Q(publish_date__lte=now) | Q(publish_date__isnull=True)) &
            Q(Q(expiry_date__gte=now) | Q(expiry_date__isnull=True)) &
            Q(target_roles__contains=role)
        )
        
        return queryset.order_by('-priority', '-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        announcement = self.get_object()
        view, created = AnnouncementView.objects.get_or_create(
            announcement=announcement,
            user=request.user
        )
        
        if created:
            announcement.views_count += 1
            announcement.save()
        
        return Response({'status': 'marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        read_announcements = AnnouncementView.objects.filter(
            user=request.user
        ).values_list('announcement_id', flat=True)
        
        queryset = self.get_queryset().exclude(id__in=read_announcements)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_user_role(self, user):
        if hasattr(user, 'student_profile'):
            return 'student'
        elif hasattr(user, 'faculty_profile'):
            return 'faculty'
        elif user.is_staff:
            return 'admin'
        return 'student'


class StudentPortalProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentPortalProfile.objects.all()
    serializer_class = StudentPortalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return StudentPortalProfile.objects.all()
        return StudentPortalProfile.objects.filter(student__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            from apps.students.models import Student
            student = Student.objects.get(user=request.user)
            profile, created = StudentPortalProfile.objects.get_or_create(student=student)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class FacultyPortalProfileViewSet(viewsets.ModelViewSet):
    queryset = FacultyPortalProfile.objects.all()
    serializer_class = FacultyPortalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return FacultyPortalProfile.objects.all()
        return FacultyPortalProfile.objects.filter(faculty__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            from apps.faculty.models import Faculty
            faculty = Faculty.objects.get(user=request.user)
            profile, created = FacultyPortalProfile.objects.get_or_create(faculty=faculty)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Faculty.DoesNotExist:
            return Response(
                {'error': 'Faculty profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PortalActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PortalActivity.objects.all()
    serializer_class = PortalActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return PortalActivity.objects.all()
        return PortalActivity.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_activity(self, request):
        activities = PortalActivity.objects.filter(
            user=request.user
        ).order_by('-created_at')[:50]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class PortalSettingsViewSet(viewsets.ModelViewSet):
    queryset = PortalSettings.objects.all()
    serializer_class = PortalSettingsSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def get_by_key(self, request):
        key = request.query_params.get('key', None)
        if not key:
            return Response(
                {'error': 'Key parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            setting = PortalSettings.objects.get(key=key, is_active=True)
            serializer = self.get_serializer(setting)
            return Response(serializer.data)
        except PortalSettings.DoesNotExist:
            return Response(
                {'error': 'Setting not found'},
                status=status.HTTP_404_NOT_FOUND
            )
