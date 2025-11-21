# Portal App

The Portal app provides a centralized dashboard and interface for students, faculty, and administrators to access various features and services of the EMIS system.

## Features

### Dashboard Management
- **User Dashboards**: Customizable dashboards for different user roles
- **Widgets**: Modular widgets for displaying different types of information
- **Quick Links**: Fast access to frequently used features
- **Themes**: Customizable theme settings for personalization

### Announcements
- **Multi-role Targeting**: Target announcements to specific roles or users
- **Priority Levels**: Low, Medium, High, and Urgent priorities
- **Scheduling**: Set publish and expiry dates
- **View Tracking**: Track who has viewed announcements
- **Attachments**: Support for file attachments

### User Profiles
- **Student Portal Profiles**: Extended profiles with bio, emergency contacts
- **Faculty Portal Profiles**: Profiles with office hours and consultation settings
- **Profile Pictures**: Upload and manage profile pictures
- **Preferences**: User-specific preferences and settings

### Activity Tracking
- **Activity Logs**: Track all user activities in the portal
- **Login Tracking**: Monitor login history and frequency
- **IP Tracking**: Record IP addresses for security
- **User Agent Tracking**: Track browser and device information

## Models

### Dashboard
- User-specific dashboard configuration
- Role-based layout and widget preferences
- Theme settings

### Widget
- Reusable dashboard widgets
- Role-based widget availability
- Configurable widget order

### QuickLink
- Category-based quick links
- Role-based link visibility
- External/internal link support

### Announcement
- Multi-priority announcements
- Role and user targeting
- Publication scheduling
- View tracking

### StudentPortalProfile
- Extended student profile information
- Emergency contact management
- Login statistics

### FacultyPortalProfile
- Extended faculty profile information
- Office hours management
- Consultation settings

### PortalActivity
- Comprehensive activity logging
- IP and user agent tracking
- Activity type categorization

### PortalSettings
- Global portal configuration
- Key-value based settings

## API Endpoints

### Dashboards
- `GET /api/portal/dashboards/` - List all dashboards
- `GET /api/portal/dashboards/{id}/` - Get specific dashboard
- `GET /api/portal/dashboards/my_dashboard/` - Get current user's dashboard
- `POST /api/portal/dashboards/{id}/update_layout/` - Update dashboard layout
- `POST /api/portal/dashboards/{id}/update_theme/` - Update theme settings

### Widgets
- `GET /api/portal/widgets/` - List all widgets
- `GET /api/portal/widgets/{id}/` - Get specific widget
- `GET /api/portal/widgets/?role=student` - Filter widgets by role

### Quick Links
- `GET /api/portal/quick-links/` - List all quick links
- `GET /api/portal/quick-links/{id}/` - Get specific quick link
- `GET /api/portal/quick-links/?role=student&category=academic` - Filter links

### Announcements
- `GET /api/portal/announcements/` - List announcements
- `GET /api/portal/announcements/{id}/` - Get specific announcement
- `POST /api/portal/announcements/{id}/mark_as_read/` - Mark as read
- `GET /api/portal/announcements/unread/` - Get unread announcements

### Student Profiles
- `GET /api/portal/student-profiles/` - List student profiles
- `GET /api/portal/student-profiles/{id}/` - Get specific profile
- `GET /api/portal/student-profiles/my_profile/` - Get current student's profile

### Faculty Profiles
- `GET /api/portal/faculty-profiles/` - List faculty profiles
- `GET /api/portal/faculty-profiles/{id}/` - Get specific profile
- `GET /api/portal/faculty-profiles/my_profile/` - Get current faculty's profile

### Activities
- `GET /api/portal/activities/` - List activities
- `GET /api/portal/activities/my_activity/` - Get current user's activities

### Settings
- `GET /api/portal/settings/` - List all settings
- `GET /api/portal/settings/get_by_key/?key=setting_name` - Get setting by key

## Views

### Web Views
- `portal/` - Portal home page
- `portal/student/` - Student dashboard
- `portal/faculty/` - Faculty dashboard
- `portal/announcements/` - Announcements list
- `portal/announcements/<id>/` - Announcement detail
- `portal/settings/profile/` - Profile settings
- `portal/settings/dashboard/` - Dashboard settings
- `portal/activity/` - Activity log

## Management Commands

### Initialize Widgets
```bash
python manage.py init_widgets
```
Creates default portal widgets for all user roles.

### Initialize Quick Links
```bash
python manage.py init_quicklinks
```
Creates default quick access links.

### Cleanup Activities
```bash
python manage.py cleanup_activities --days=90
```
Removes activity logs older than specified days (default: 90).

## Forms

- **DashboardForm**: Dashboard configuration
- **WidgetForm**: Widget creation and editing
- **QuickLinkForm**: Quick link management
- **AnnouncementForm**: Announcement creation
- **StudentPortalProfileForm**: Student profile editing
- **FacultyPortalProfileForm**: Faculty profile editing
- **ProfilePictureUploadForm**: Profile picture upload
- **ThemeSettingsForm**: Theme customization

## Permissions

- **IsOwnerOrAdmin**: Access for owners and admins
- **IsStudentOrAdmin**: Student-specific access
- **IsFacultyOrAdmin**: Faculty-specific access

## Signals

- **create_student_portal_profile**: Auto-create profile when student is created
- **create_faculty_portal_profile**: Auto-create profile when faculty is created

## Middleware

- **PortalActivityMiddleware**: Automatic activity logging for portal pages

## Context Processors

- **portal_context**: Adds portal-specific context to all templates
  - User dashboard
  - Unread announcements count
  - Quick links

## Filters

- **DashboardFilter**: Filter dashboards by role, status, date
- **AnnouncementFilter**: Filter announcements by priority, publication status
- **PortalActivityFilter**: Filter activities by type, date range

## Usage Examples

### Creating a Dashboard
```python
from apps.portal.models import Dashboard

dashboard = Dashboard.objects.create(
    user=user,
    role='student',
    theme_settings={'theme': 'light', 'primary_color': '#007bff'},
    is_active=True
)
```

### Creating an Announcement
```python
from apps.portal.models import Announcement
from django.utils import timezone

announcement = Announcement.objects.create(
    title='Important Notice',
    content='All students must attend...',
    author=admin_user,
    priority='high',
    target_roles=['student'],
    is_published=True,
    publish_date=timezone.now()
)
```

### Adding a Widget
```python
from apps.portal.models import Widget

widget = Widget.objects.create(
    name='Attendance Summary',
    widget_type='attendance',
    description='Shows attendance overview',
    roles=['student', 'faculty'],
    is_active=True,
    order=1
)
```

### Logging Activity
```python
from apps.portal.models import PortalActivity

PortalActivity.objects.create(
    user=request.user,
    activity_type='download',
    description='Downloaded grade report',
    metadata={'file': 'grades.pdf'},
    ip_address='127.0.0.1'
)
```

## Integration

The Portal app integrates with:
- **Authentication**: User authentication and authorization
- **Students**: Student profiles and data
- **Faculty**: Faculty profiles and data
- **Courses**: Course enrollments and schedules
- **Exams**: Grade information
- **Finance**: Fee status
- **Library**: Library resources
- **Notifications**: System notifications

## Security Features

- Activity logging and monitoring
- IP address tracking
- User agent tracking
- Role-based access control
- View tracking for announcements

## Configuration

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'apps.portal',
]
```

Add to URL configuration:
```python
urlpatterns = [
    ...
    path('portal/', include('apps.portal.urls')),
    path('api/portal/', include('apps.portal.api_urls')),
]
```

Add middleware (optional):
```python
MIDDLEWARE = [
    ...
    'apps.portal.middleware.PortalActivityMiddleware',
]
```

Add context processor:
```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'apps.portal.context_processors.portal_context',
            ],
        },
    },
]
```

## Testing

Run tests:
```bash
python manage.py test apps.portal
```

## Admin Interface

All models are registered in the admin interface with:
- List displays with relevant fields
- Search functionality
- Filters for common queries
- Readonly fields for timestamps
- Custom fieldsets for organization

## Best Practices

1. **Dashboard Customization**: Allow users to customize their dashboards
2. **Widget Management**: Keep widgets modular and reusable
3. **Announcement Targeting**: Use roles and specific users for targeted communication
4. **Activity Logging**: Log important user activities for security and analytics
5. **Profile Updates**: Encourage users to keep profiles updated
6. **Quick Links**: Organize links by category for better UX
7. **Theme Settings**: Provide theme options for accessibility

## Future Enhancements

- Real-time notifications using WebSockets
- Advanced analytics dashboard
- Mobile app support
- Widget marketplace
- Customizable widget layouts
- Multi-language support
- Dark mode support
- Advanced search functionality
- Integration with external services
- Calendar integration
