# EMIS Complete Setup Guide

## 🎯 Quick Start

This guide will help you set up and run the EMIS system.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Node.js 14+ (for Tailwind CSS)
- PostgreSQL 12+ (recommended) or SQLite for development

## 🚀 Installation Steps

### 1. Clone or Navigate to Project

```bash
cd /path/to/EMIS
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies (for Tailwind CSS)

```bash
npm install
```

### 5. Database Setup

```bash
# Create migrations for all apps
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Compile Tailwind CSS

```bash
# For development (with watch mode)
npm run dev

# For production (minified)
npm run build
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Access the application at: **http://localhost:8000**

## 📁 Project Structure

```
EMIS/
├── apps/                  # All Django applications
│   ├── admissions/       # Admissions management
│   ├── analytics/        # Analytics & reports
│   ├── attendance/       # Attendance tracking
│   ├── cms/             # Content management
│   ├── courses/         # Course management
│   ├── exams/           # Examination system
│   ├── faculty/         # Faculty management
│   ├── finance/         # Finance & fees
│   ├── hostel/          # Hostel management
│   ├── hr/              # Human resources
│   ├── inventory/       # Inventory control
│   ├── library/         # Library system
│   ├── lms/             # Learning management
│   ├── notifications/   # Notification system
│   ├── reports/         # Report generation
│   ├── students/        # Student management
│   ├── timetable/       # Timetable management
│   └── transport/       # Transport management
│
├── templates/            # HTML templates
├── static/              # Static files
├── config/              # Django configuration
└── docs/                # Documentation
```

## 🎨 Features Overview

### All 18 Modules Included:

1. **Students** - Student records management
2. **Admissions** - Application processing
3. **Attendance** - Attendance tracking
4. **Courses** - Course & curriculum management
5. **Exams** - Examination & grading
6. **Finance** - Fee management & payments
7. **Library** - Library resources
8. **LMS** - Learning management system
9. **Faculty** - Faculty records
10. **Timetable** - Class scheduling
11. **HR** - Employee management
12. **Analytics** - Analytics dashboard
13. **Hostel** - Accommodation management
14. **Transport** - Vehicle management
15. **Inventory** - Stock control
16. **Reports** - Report generation
17. **Notifications** - Multi-channel notifications
18. **CMS** - Content management

### Each Module Includes:

✅ **Complete MVC Structure**
- Models with custom managers
- Forms with validation
- Views with permissions
- URL routing

✅ **Admin Interface**
- Django admin integration
- Custom admin actions
- Filters and search

✅ **API Endpoints**
- RESTful API
- Serializers
- Permissions
- Filters

✅ **Testing**
- Unit tests
- Model tests
- View tests

✅ **Utilities**
- Helper functions
- Export functions
- Validators

## 🔐 Default Login Credentials

After creating superuser, use those credentials to login.

### Creating Test Users:

```bash
python manage.py shell
```

```python
from apps.authentication.models import User

# Create a student
student = User.objects.create_user(
    username='student1',
    email='student@test.com',
    password='student123',
    is_student=True
)

# Create a faculty
faculty = User.objects.create_user(
    username='faculty1',
    email='faculty@test.com',
    password='faculty123',
    is_faculty=True
)
```

## 🎯 Common Tasks

### Run Migrations After Model Changes

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create New Module

```bash
python manage.py startapp new_module apps/new_module
```

### Run Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.students

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Collect Static Files (for production)

```bash
python manage.py collectstatic
```

### Load Sample Data

```bash
python manage.py loaddata initial_data.json
```

## 🛠️ Development Tools

### Available Generator Scripts:

```bash
# Generate module structure
python generate_modules.py

# Enhance apps with complete file structure
python enhance_apps.py

# Update sidebar navigation
python update_sidebars.py
```

### Useful Django Commands:

```bash
# Create superuser
python manage.py createsuperuser

# Database shell
python manage.py dbshell

# Python shell with Django
python manage.py shell

# Check for issues
python manage.py check

# Show migrations
python manage.py showmigrations

# Make messages for i18n
python manage.py makemessages

# Compile messages
python manage.py compilemessages
```

## 📊 Database

### SQLite (Development)

Default configuration uses SQLite. No additional setup needed.

### PostgreSQL (Production Recommended)

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE emis_db;
CREATE USER emis_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE emis_db TO emis_user;
```

3. Update settings:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'emis_db',
        'USER': 'emis_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎨 Tailwind CSS

### Development Mode (with watch)

```bash
npm run dev
```

This watches for changes and recompiles CSS automatically.

### Production Build

```bash
npm run build
```

This creates a minified CSS file for production.

## 🔧 Troubleshooting

### Module Not Found Error

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Migration Errors

```bash
# Reset migrations (CAUTION: Development only)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --clear

# Check STATIC_ROOT and STATIC_URL in settings
```

### Port Already in Use

```bash
# Use different port
python manage.py runserver 8001

# Or kill process using port 8000
# On Linux/Mac:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📚 Documentation

- **README.md** - Project overview
- **QUICKSTART.md** - Quick start guide  
- **DEPLOYMENT_GUIDE.md** - Deployment instructions
- **TAILWIND_SETUP.md** - Tailwind CSS configuration

## 🌐 Accessing the Application

After running the server, access:

- **Main Application**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs/
- **API Schema**: http://localhost:8000/api/schema/

## 🎯 Next Steps

1. ✅ Login with superuser credentials
2. ✅ Explore the 18 modules
3. ✅ Create test data
4. ✅ Customize module templates
5. ✅ Add business logic to views
6. ✅ Configure email settings
7. ✅ Set up production database
8. ✅ Deploy to production server

## 🆘 Getting Help

- Check documentation files in `/docs`
- Review code comments
- Examine test files for usage examples
- Check Django documentation: https://docs.djangoproject.com

## ✅ Verification

Verify your installation:

```bash
# Check Python version
python --version

# Check Django version
python -c "import django; print(django.get_version())"

# Check all apps
python manage.py check

# List installed apps
python manage.py show_urls
```

## 🎉 Success!

If you can access http://localhost:8000 and see the login page, your installation is successful!

---

**Need help?** Review the documentation or check the code comments in each module.
