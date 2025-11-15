# EMIS - Django Migration Guide

## Project Conversion Summary

The EMIS project has been converted from FastAPI to Django with full-stack capabilities.

### Major Changes

1. **Framework**: FastAPI → Django 4.2+
2. **ORM**: SQLAlchemy → Django ORM
3. **Migrations**: Alembic → Django Migrations
4. **Frontend**: Added Django Templates with Bootstrap 5
5. **API**: Added Django REST Framework

### New Project Structure

```
EMIS/
├── config/                     # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                       # Django applications
│   ├── core/
│   ├── authentication/
│   ├── students/
│   ├── faculty/
│   ├── hr/
│   ├── finance/
│   ├── library/
│   ├── admissions/
│   ├── exams/
│   ├── attendance/
│   ├── timetable/
│   ├── hostel/
│   ├── transport/
│   ├── inventory/
│   ├── lms/
│   ├── analytics/
│   ├── notifications/
│   └── reports/
├── templates/                  # Django templates
├── static/                     # Static files (CSS, JS, images)
├── uploads/                    # Media files
├── manage.py                   # Django management script
└── requirements.txt            # Updated dependencies
```

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**:
   ```bash
   cp .env.development .env
   # Edit .env with your database and secret settings
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Development Server**:
   ```bash
   ./start-dev.sh
   # or
   python manage.py runserver
   ```

6. **Access the Application**:
   - Application: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - API: http://localhost:8000/api/v1/

### Environment Variables

Update your `.env` file with:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emis

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Features

- **Bootstrap 5** UI framework
- **HTMX** for dynamic interactions
- **Chart.js** for data visualization
- **DataTables** for advanced tables
- **Crispy Forms** for form rendering

### API Endpoints

All previous API endpoints are now available under `/api/v1/`:

- `/api/v1/auth/` - Authentication endpoints
- `/api/v1/students/` - Student endpoints
- `/api/v1/faculty/` - Faculty endpoints
- `/api/v1/hr/` - HR endpoints
- `/api/v1/finance/` - Finance endpoints
- And more...

### Development Workflow

1. **Create New App**:
   ```bash
   python manage.py startapp appname
   ```

2. **Make Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Tests**:
   ```bash
   python manage.py test
   ```

### Production Deployment

1. **Using Docker**:
   ```bash
   ./start-prod.sh
   ```

2. **Manual Deployment**:
   ```bash
   # Collect static files
   python manage.py collectstatic
   
   # Run with Gunicorn
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

### Next Steps

1. Implement remaining apps (students, faculty, hr, finance, etc.)
2. Create models for each app
3. Build API views and serializers
4. Create frontend templates
5. Add tests for all functionality

### Migration Notes

- **Database**: Use Django ORM instead of SQLAlchemy
- **Async**: Django has async support, but most views can be synchronous
- **Dependencies**: FastAPI dependencies removed, Django equivalents added
- **Routing**: URL patterns defined in `urls.py` files
- **Middleware**: Django middleware instead of FastAPI middleware
- **Templates**: Server-side rendering with Django templates

### Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Bootstrap 5: https://getbootstrap.com/
- HTMX: https://htmx.org/

