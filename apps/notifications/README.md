# Notifications App

A comprehensive notification system for the EMIS platform supporting multiple delivery channels (in-app, email, SMS, push notifications).

## Features

### Core Features
- **Multi-channel notifications**: In-app, Email, SMS, Push notifications
- **Notification templates**: Reusable templates with variable substitution
- **Scheduled notifications**: Send notifications at specific times
- **Recurring notifications**: Daily, weekly, monthly recurring patterns
- **User preferences**: Customizable notification settings per user
- **Quiet hours**: Suppress notifications during user-defined time periods
- **Notification logging**: Track delivery status for all channels
- **Bulk notifications**: Send to multiple users at once
- **Rich notifications**: Support for action URLs and metadata

### Models

1. **Notification**
   - Main notification model
   - Supports multiple delivery channels
   - Generic relation to any model
   - Read/unread status tracking
   - Expiry dates

2. **NotificationTemplate**
   - Reusable notification templates
   - Django template syntax support
   - Variable substitution
   - Default channel configuration

3. **NotificationPreference**
   - User-specific notification settings
   - Channel preferences (email, SMS, push, in-app)
   - Quiet hours configuration
   - Daily digest settings

4. **ScheduledNotification**
   - Schedule notifications for future delivery
   - Recurring notification support
   - Template-based or direct content
   - Recipient groups

5. **NotificationLog**
   - Delivery tracking
   - Error logging
   - Channel-specific status

## Installation

The app is already installed in the EMIS project. To use it:

1. Run migrations:
```bash
python manage.py makemigrations notifications
python manage.py migrate notifications
```

2. Add to settings if not already present:
```python
INSTALLED_APPS = [
    # ...
    'apps.notifications',
]
```

## Usage

### Sending Notifications

#### Simple notification:
```python
from apps.notifications.utils import send_notification

notification = send_notification(
    recipient=user,
    title="Welcome!",
    message="Welcome to EMIS platform",
    notification_type='info',
    channels=['in_app', 'email']
)
```

#### Bulk notifications:
```python
from apps.notifications.utils import send_bulk_notifications

count = send_bulk_notifications(
    recipients=[user1, user2, user3],
    title="System Maintenance",
    message="System will be down for maintenance",
    notification_type='warning',
    channels=['in_app', 'email']
)
```

#### Template-based notifications:
```python
from apps.notifications.utils import send_notification_from_template

notification = send_notification_from_template(
    template_code='welcome-email',
    recipient=user,
    context={'name': user.first_name, 'school': 'ABC School'}
)
```

### Management Commands

Process scheduled notifications (run via cron):
```bash
python manage.py process_scheduled_notifications
```

Clean up old notifications:
```bash
python manage.py cleanup_notifications --days 30
```

### API Endpoints

#### Notifications
- `GET /api/notifications/` - List user's notifications
- `GET /api/notifications/{id}/` - Get notification detail
- `POST /api/notifications/{id}/mark_read/` - Mark as read
- `POST /api/notifications/{id}/mark_unread/` - Mark as unread
- `GET /api/notifications/unread/` - Get unread notifications
- `GET /api/notifications/unread_count/` - Get unread count
- `POST /api/notifications/mark_all_read/` - Mark all as read
- `POST /api/notifications/send_bulk/` - Send bulk notifications (admin)

#### Templates (Admin)
- `GET /api/notifications/templates/` - List templates
- `POST /api/notifications/templates/` - Create template
- `GET /api/notifications/templates/{id}/` - Get template
- `PUT /api/notifications/templates/{id}/` - Update template
- `DELETE /api/notifications/templates/{id}/` - Delete template
- `POST /api/notifications/templates/{id}/render/` - Render template

#### Preferences
- `GET /api/notifications/preferences/my_preferences/` - Get user preferences
- `PUT /api/notifications/preferences/{id}/` - Update preferences

#### Scheduled (Admin)
- `GET /api/notifications/scheduled/` - List scheduled notifications
- `POST /api/notifications/scheduled/` - Create scheduled notification
- `GET /api/notifications/scheduled/pending/` - Get pending notifications
- `POST /api/notifications/scheduled/{id}/send_now/` - Send immediately

### Web Views

- `/notifications/` - Dashboard
- `/notifications/list/` - List notifications
- `/notifications/<id>/` - Notification detail
- `/notifications/send/` - Send notification (admin)
- `/notifications/templates/` - Template management (admin)
- `/notifications/scheduled/` - Scheduled notifications (admin)
- `/notifications/preferences/` - User preferences
- `/notifications/statistics/` - Statistics (admin)

### Template Context

The app provides context processors to add notification data to all templates:

```django
{{ unread_notification_count }}  <!-- Number of unread notifications -->
{{ recent_notifications }}  <!-- List of 5 recent notifications -->
```

### Middleware

The notification middleware attaches unread count to the request:

```python
request.unread_notifications_count  # Available in views
```

## Configuration

### Email Settings
Configure email backend in settings.py:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```

### SMS Configuration
Implement SMS provider in `utils.py`:
```python
def send_sms_notification(notification):
    # Integrate with Twilio, AWS SNS, etc.
    pass
```

### Push Notifications
Implement push notification in `utils.py`:
```python
def send_push_notification(notification):
    # Integrate with FCM, APNS, etc.
    pass
```

## Notification Types

- `info` - Informational
- `success` - Success messages
- `warning` - Warnings
- `error` - Error messages
- `announcement` - Announcements
- `reminder` - Reminders

## Channels

- `in_app` - In-application notifications
- `email` - Email notifications
- `sms` - SMS notifications
- `push` - Push notifications

## Signals

The app provides signals for integration:

```python
from django.dispatch import receiver
from apps.notifications.signals import notification_post_save

@receiver(notification_post_save)
def my_handler(sender, instance, created, **kwargs):
    # Custom logic
    pass
```

## Admin Interface

Full admin interface available at `/admin/notifications/` with:
- Notification management
- Template editor
- Preference management
- Scheduled notification management
- Delivery logs

## Testing

Run tests:
```bash
python manage.py test apps.notifications
```

## Best Practices

1. **Use templates**: Create reusable templates for common notifications
2. **Check preferences**: Always respect user notification preferences
3. **Batch operations**: Use bulk operations for sending to multiple users
4. **Clean up**: Regularly clean up old notifications
5. **Error handling**: Monitor NotificationLog for delivery failures
6. **Quiet hours**: Respect user quiet hours settings

## Examples

### Welcome notification on user registration:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.notifications.utils import send_notification

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance, created, **kwargs):
    if created:
        send_notification(
            recipient=instance,
            title=f"Welcome {instance.first_name}!",
            message="Thank you for joining our platform.",
            notification_type='info',
            channels=['in_app', 'email']
        )
```

### Fee reminder:
```python
from apps.notifications.models import ScheduledNotification

ScheduledNotification.objects.create(
    title="Fee Payment Reminder",
    message="Your fees are due in 3 days",
    notification_type='reminder',
    scheduled_for=timezone.now() + timedelta(days=3),
    channels=['in_app', 'email', 'sms'],
    is_recurring=True,
    recurrence_pattern='monthly',
    created_by=admin_user
)
```

## License

Part of the EMIS system.
