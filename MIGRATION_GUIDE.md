# EMIS - Django Migration Guide

## Overview

EMIS (Educational Management Information System) is a comprehensive full-stack web application built with **Django 4.2+**. This guide covers the project structure, setup, and development workflow.

## What Changed (FastAPI → Django)

The project was migrated from FastAPI to Django to provide:
- ✅ Full-stack web application (Frontend + Backend)
- ✅ Built-in admin panel
- ✅ Django ORM (no more SQLAlchemy)
- ✅ Django migrations (no more Alembic)
- ✅ Server-side rendering with templates
- ✅ Mature, production-ready framework

**All FastAPI code has been removed.** The project is now 100% Django.

## Project Structure

```
EMIS/
├── config/                 # Django settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI server
│   ├── asgi.py            # ASGI server
│   └── celery.py          # Celery configuration
│
├── apps/                   # Django applications (18 apps)
│   ├── authentication/    # User auth and RBAC
│   ├── students/         # Student portal
│   ├── faculty/          # Faculty portal
│   ├── hr/               # HR management
│   ├── finance/          # Finance & accounting
│   ├── library/          # Library management
│   ├── admissions/       # Admissions
│   ├── exams/            # Exam management
│   ├── attendance/       # Attendance tracking
│   ├── timetable/        # Scheduling
│   ├── hostel/           # Hostel management
│   ├── transport/        # Transport
│   ├── inventory/        # Inventory
│   ├── lms/              # Learning Management
│   ├── analytics/        # Analytics
│   ├── notifications/    # Messaging
│   ├── reports/          # Reports
│   └── core/             # Base models & utilities
│
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── includes/         # Header, footer, sidebar
│   ├── authentication/   # Auth pages
│   └── ...               # App-specific templates
│
├── static/               # Static files
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript
│   └── images/          # Images
│
├── tests/                # Test suite
├── manage.py             # Django CLI
└── requirements.txt      # Dependencies
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Django 4.2+ |
| **API** | Django REST Framework |
| **Database** | PostgreSQL 15+ |
| **ORM** | Django ORM |
| **Frontend** | Bootstrap 5, HTMX, Chart.js |
| **Task Queue** | Celery + Redis |
| **Auth** | JWT + Session-based |
| **Server** | Gunicorn |
| **Testing** | pytest-django |

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone and setup**
```bash
cd EMIS
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.development .env
# Edit .env with your settings
```

Required `.env` variables:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/emis
REDIS_URL=redis://localhost:6379/0
```

4. **Setup database**
```bash
# Start PostgreSQL and Redis (or use Docker)
docker-compose up -d postgres redis

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data.json
```

5. **Collect static files**
```bash
python manage.py collectstatic
```

6. **Start development server**
```bash
./start-dev.sh
# or
python manage.py runserver
```

7. **Access the application**
- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API: http://localhost:8000/api/v1/

## Development

### Common Commands

```bash
# Database
python manage.py makemigrations          # Create migrations
python manage.py migrate                 # Apply migrations
python manage.py showmigrations          # Show migration status
python manage.py dbshell                 # Database shell

# Users
python manage.py createsuperuser         # Create admin user
python manage.py changepassword <user>   # Change password

# Development
python manage.py runserver               # Start dev server
python manage.py shell                   # Django shell
python manage.py check                   # Check for issues

# Static files
python manage.py collectstatic           # Collect static files
python manage.py findstatic <file>       # Find static file

# Testing
python manage.py test                    # Run tests
pytest                                   # Run with pytest
pytest --cov=apps                        # With coverage

# Celery
celery -A config worker -l info          # Start worker
celery -A config beat -l info            # Start scheduler
```

### Creating a New App

```bash
# Create the app
python manage.py startapp myapp apps/myapp

# Add to INSTALLED_APPS in config/settings.py
INSTALLED_APPS = [
    ...
    'apps.myapp',
]

# Create models in apps/myapp/models.py
from django.db import models
from apps.core.models import TimeStampedModel

class MyModel(TimeStampedModel):
    name = models.CharField(max_length=100)

# Create migrations
python manage.py makemigrations
python manage.py migrate

# Register in admin
from django.contrib import admin
from .models import MyModel

admin.site.register(MyModel)
```

### API Development

```python
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
    permission_classes = [IsAuthenticated]

# api_urls.py
from rest_framework.routers import DefaultRouter
from .api_views import MyModelViewSet

router = DefaultRouter()
router.register('mymodel', MyModelViewSet)
urlpatterns = router.urls
```

### Frontend Development

```python
# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    return render(request, 'myapp/template.html', {
        'title': 'My Page',
        'data': 'Hello World'
    })

# urls.py
from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('page/', views.my_view, name='page'),
]
```

```html
<!-- templates/myapp/template.html -->
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ title }}</h1>
    <p>{{ data }}</p>
</div>
{% endblock %}
```

## Production Deployment

### Using Docker

```bash
# Start all services
./start-prod.sh

# Or manually
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --no-input

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure production settings
export DJANGO_SETTINGS_MODULE=config.settings
export DEBUG=False

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Start with Gunicorn
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/EMIS/staticfiles/;
    }

    location /media/ {
        alias /path/to/EMIS/uploads/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Testing

```bash
# Run all tests
python manage.py test

# Run with pytest
pytest

# Run specific app tests
pytest apps/authentication/

# With coverage
pytest --cov=apps --cov-report=html

# Open coverage report
open htmlcov/index.html
```

## Troubleshooting

### Database Connection Error
```bash
# Check DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/emis

# Test connection
python manage.py dbshell
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --clear
python manage.py collectstatic

# Check STATIC_ROOT and STATIC_URL in settings.py
```

### Migration Issues
```bash
# Show current state
python manage.py showmigrations

# Reset migrations (development only)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

### ImportError: No module named 'apps'
```bash
# Make sure you're in the project root
pwd  # Should be /path/to/EMIS

# Activate virtual environment
source venv/bin/activate
```

## API Documentation

### Authentication

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token
curl http://localhost:8000/api/v1/students/ \
  -H "Authorization: Bearer <access_token>"

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/auth/token/` | Get JWT token |
| `/api/v1/auth/token/refresh/` | Refresh token |
| `/api/v1/auth/register/` | Register user |
| `/api/v1/auth/me/` | Current user profile |
| `/api/v1/students/` | Students API |
| `/api/v1/faculty/` | Faculty API |
| `/api/v1/hr/` | HR API |
| `/api/v1/finance/` | Finance API |
| `/api/v1/library/` | Library API |

## Environment Variables

### Development (.env.development)
```env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://emis_user:emis_password@localhost:5432/emis_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
LOG_LEVEL=DEBUG
DEFAULT_PAGE_SIZE=20
```

### Production (.env.production)
```env
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@postgres:5432/emis_db
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=https://your-domain.com
LOG_LEVEL=INFO
DEFAULT_PAGE_SIZE=20
```

## Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Bootstrap 5**: https://getbootstrap.com/
- **HTMX**: https://htmx.org/
- **Celery**: https://docs.celeryq.dev/

## Support

For issues or questions:
1. Check this documentation
2. See `QUICK_REFERENCE.md` for common commands
3. Check Django documentation
4. Review the code in `apps/` for examples

## License

[Your License Here]
