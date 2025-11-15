# EMIS Django - Quick Reference

## Common Commands

### Development
```bash
# Start development server
python manage.py runserver
# or
./start-dev.sh

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run shell
python manage.py shell

# Run tests
python manage.py test
```

### Database
```bash
# Reset database
python manage.py flush

# Show migrations
python manage.py showmigrations

# SQL for migration
python manage.py sqlmigrate app_name migration_number
```

### Production
```bash
# Start with Docker
./start-prod.sh

# Manual start
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Project Structure

```
apps/
├── authentication/     # User auth and management
├── students/          # Student portal
├── faculty/           # Faculty portal
├── hr/               # HR management
├── finance/          # Finance module
├── library/          # Library management
├── admissions/       # Admissions
├── exams/            # Exam management
├── attendance/       # Attendance tracking
├── timetable/        # Scheduling
├── hostel/           # Hostel management
├── transport/        # Transport
├── inventory/        # Inventory
├── lms/              # Learning Management
├── analytics/        # Analytics
├── notifications/    # Notifications
└── reports/          # Reports
```

## URLs

### Frontend
- `/` - Home
- `/auth/login/` - Login
- `/auth/logout/` - Logout
- `/auth/register/` - Register
- `/dashboard/` - Dashboard
- `/student/` - Student portal
- `/faculty/` - Faculty portal
- `/admin-portal/` - Admin portal
- `/admin/` - Django admin

### API
- `/api/v1/auth/token/` - Get JWT token
- `/api/v1/auth/token/refresh/` - Refresh token
- `/api/v1/auth/register/` - Register user
- `/api/v1/auth/me/` - User profile
- `/api/v1/students/` - Students API
- `/api/v1/faculty/` - Faculty API
- `/api/v1/hr/` - HR API
- `/api/v1/finance/` - Finance API

## Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/emis

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## File Locations

### Settings
- Main settings: `config/settings.py`
- URLs: `config/urls.py`
- WSGI: `config/wsgi.py`
- ASGI: `config/asgi.py`

### Templates
- Base: `templates/base.html`
- Login: `templates/authentication/login.html`
- Header: `templates/includes/header.html`
- Sidebar: `templates/includes/sidebar.html`
- Footer: `templates/includes/footer.html`

### Static
- CSS: `static/css/`
- JS: `static/js/`
- Images: `static/images/`

## Creating a New App

```bash
# Create app
python manage.py startapp app_name apps/app_name

# Add to INSTALLED_APPS in config/settings.py
INSTALLED_APPS = [
    ...
    'apps.app_name',
]

# Create URLs
# apps/app_name/urls.py
from django.urls import path
from . import views

app_name = 'app_name'
urlpatterns = [
    path('', views.index, name='index'),
]

# Add to main URLs in config/urls.py
urlpatterns = [
    ...
    path('app_name/', include('apps.app_name.urls')),
]
```

## API Development

```python
# models.py
from apps.core.models import TimeStampedModel

class MyModel(TimeStampedModel):
    name = models.CharField(max_length=100)

# serializers.py
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

# api_views.py
from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

# api_urls.py
from rest_framework.routers import DefaultRouter
from .api_views import MyModelViewSet

router = DefaultRouter()
router.register('mymodel', MyModelViewSet)

urlpatterns = router.urls
```

## Frontend Development

```python
# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    context = {'data': 'value'}
    return render(request, 'app_name/template.html', context)

# urls.py
from django.urls import path
from . import views

app_name = 'app_name'
urlpatterns = [
    path('page/', views.my_view, name='page'),
]
```

```html
<!-- template.html -->
{% extends 'base.html' %}

{% block title %}My Page{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>My Page</h1>
    <p>{{ data }}</p>
</div>
{% endblock %}
```

## Troubleshooting

### Migration Issues
```bash
# Reset migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Database Connection Error
Check `.env` file for correct DATABASE_URL

### Import Errors
Make sure all apps are in INSTALLED_APPS

## Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Bootstrap: https://getbootstrap.com/
- CONVERSION_SUMMARY.md - Full conversion details
- DJANGO_MIGRATION.md - Migration guide
