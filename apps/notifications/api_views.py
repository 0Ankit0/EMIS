"""
Notifications API Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone

from .models import (
    Notification, NotificationTemplate, NotificationPreference,
    ScheduledNotification, NotificationLog
)
from .serializers import (
    NotificationSerializer, NotificationListSerializer, NotificationCreateSerializer,
    NotificationTemplateSerializer, NotificationPreferenceSerializer,
    ScheduledNotificationSerializer, NotificationLogSerializer,
    BulkNotificationSerializer
)
from .permissions import IsNotificationsOwner, CanNotificationsManage
from .utils import send_notification, send_bulk_notifications


class NotificationViewSet(viewsets.ModelViewSet):
    """API ViewSet for Notifications"""
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get notifications for current user"""
        return Notification.objects.for_user(self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer"""
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        """Set sender to current user"""
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        notifications = self.get_queryset().unread()
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notifications count"""
        count = self.get_queryset().unread().count()
        return Response({'count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'status': 'marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_unread(self, request, pk=None):
        """Mark notification as unread"""
        notification = self.get_object()
        notification.mark_as_unread()
        return Response({'status': 'marked as unread'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().unread().mark_all_as_read()
        return Response({'status': 'all marked as read'})
    
    @action(detail=False, methods=['post'])
    def send_bulk(self, request):
        """Send bulk notifications (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = BulkNotificationSerializer(data=request.data)
        if serializer.is_valid():
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            recipients = User.objects.filter(id__in=serializer.validated_data['recipients'])
            
            count = send_bulk_notifications(
                recipients=recipients,
                title=serializer.validated_data['title'],
                message=serializer.validated_data['message'],
                notification_type=serializer.validated_data['notification_type'],
                channels=serializer.validated_data['channels'],
                action_url=serializer.validated_data.get('action_url', ''),
                sender=request.user
            )
            
            return Response({
                'status': 'success',
                'count': count
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """API ViewSet for Notification Templates"""
    
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated, CanNotificationsManage]
    
    def get_queryset(self):
        """Filter active templates for non-staff users"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.active()
        return queryset
    
    @action(detail=True, methods=['post'])
    def render(self, request, pk=None):
        """Render template with context"""
        template = self.get_object()
        context = request.data.get('context', {})
        
        try:
            rendered = template.render(context)
            return Response(rendered)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """API ViewSet for Notification Preferences"""
    
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get preference for current user"""
        return NotificationPreference.objects.filter(user=self.request.user)
    
    def get_object(self):
        """Get or create preference for current user"""
        preference, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference
    
    @action(detail=False, methods=['get'])
    def my_preferences(self, request):
        """Get current user's preferences"""
        preference = self.get_object()
        serializer = self.get_serializer(preference)
        return Response(serializer.data)


class ScheduledNotificationViewSet(viewsets.ModelViewSet):
    """API ViewSet for Scheduled Notifications"""
    
    queryset = ScheduledNotification.objects.all()
    serializer_class = ScheduledNotificationSerializer
    permission_classes = [IsAuthenticated, CanNotificationsManage]
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending scheduled notifications"""
        notifications = self.get_queryset().filter(is_sent=False, is_active=True)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def send_now(self, request, pk=None):
        """Send scheduled notification immediately"""
        notification = self.get_object()
        
        if notification.is_sent:
            return Response(
                {'error': 'Notification already sent'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.save()
        
        return Response({'status': 'sent'})


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Notification Logs (read-only)"""
    
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAuthenticated, CanNotificationsManage]
    
    def get_queryset(self):
        """Filter logs based on permissions"""
        queryset = super().get_queryset()
        
        notification_id = self.request.query_params.get('notification')
        if notification_id:
            queryset = queryset.filter(notification_id=notification_id)
        
        channel = self.request.query_params.get('channel')
        if channel:
            queryset = queryset.filter(channel=channel)
        
        is_successful = self.request.query_params.get('is_successful')
        if is_successful is not None:
            queryset = queryset.filter(is_successful=is_successful.lower() == 'true')
        
        return queryset
