# Quick Start Guide - EMIS Authentication System

## Login & Test

### Default Credentials
```
Username: admin
Password: admin123
Email: admin@emis.edu
```

### Access Points
- **Home**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/auth/login/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Profile**: http://127.0.0.1:8000/auth/profile/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations (if needed)
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Adding New Modules to Dashboard

Edit `apps/core/views.py` in the `dashboard()` function:

```python
modules.append({
    'name': 'Module Name',
    'description': 'Short description',
    'icon': 'fa-icon-name',  # FontAwesome icon
    'color': 'primary',  # primary, success, info, warning, danger, secondary
    'url': '/path/to/module/',  # Optional
})
```

## Protecting Views with Login

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    return render(request, 'myapp/template.html')
```

## Checking User Roles

```python
# In view
if request.user.is_superuser:
    # Admin access
    
if request.user.is_staff:
    # Staff access
    
if request.user.is_student:
    # Student access
    
if request.user.is_faculty:
    # Faculty access

# Check custom roles
user_roles = [ur.role.name.lower() for ur in request.user.user_roles.all()]
if 'librarian' in user_roles:
    # Librarian access
```

## In Templates

```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.get_full_name }}!</p>
{% endif %}

{% if user.is_superuser %}
    <a href="/admin/">Admin Panel</a>
{% endif %}

{% if user.is_student %}
    <a href="/students/dashboard/">Student Portal</a>
{% endif %}
```

## URL Reversing

```python
# In views
from django.urls import reverse
from django.shortcuts import redirect

return redirect('core:dashboard')
return redirect('authentication:login')
```

```django
<!-- In templates -->
<a href="{% url 'core:dashboard' %}">Dashboard</a>
<a href="{% url 'authentication:profile' %}">Profile</a>
<a href="{% url 'authentication:logout' %}">Logout</a>
```

## Bootstrap 5 Components Available

### Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
```

### Cards
```html
<div class="card">
    <div class="card-header">Header</div>
    <div class="card-body">Content</div>
</div>
```

### Alerts
```html
<div class="alert alert-info">Information</div>
<div class="alert alert-warning">Warning</div>
<div class="alert alert-danger">Error</div>
```

## FontAwesome Icons

```html
<i class="fas fa-user"></i>
<i class="fas fa-graduation-cap"></i>
<i class="fas fa-book"></i>
<i class="fas fa-dollar-sign"></i>
<i class="fas fa-chart-line"></i>
```

## Common Tasks

### Create a New User
```python
from apps.authentication.models import User

user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='securepass123',
    first_name='John',
    last_name='Doe'
)
user.is_student = True
user.save()
```

### Assign a Role
```python
from apps.authentication.models import Role, UserRole

role = Role.objects.get(name='Student')
UserRole.objects.create(user=user, role=role)
```

### Check Permissions (Future)
```python
# Will be implemented with permission system
if user.has_permission('students', 'view'):
    # Allow access
```

## Troubleshooting

### Issue: Can't login
- Check username/password
- Verify user exists: `User.objects.filter(username='admin').exists()`
- Check user is active: `user.is_active`

### Issue: Redirected to wrong page after login
- Check `LOGIN_REDIRECT_URL` in settings.py
- Check `next` parameter in login URL

### Issue: 404 on dashboard
- Verify URL pattern: `python manage.py check`
- Check template exists: `templates/core/dashboard.html`

### Issue: No modules showing
- Check user role/permissions
- Verify `modules` list in dashboard view
- Check console for errors

## Environment Variables

Create `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:pass@localhost/emis
REDIS_URL=redis://localhost:6379/0
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.authentication

# Run with coverage
pytest --cov=apps --cov-report=html
```

## API Access

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Use Token
```bash
curl http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Support & Documentation

- **Full Documentation**: `/docs/AUTHENTICATION_GUIDE.md`
- **API Docs**: http://127.0.0.1:8000/api/docs/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Django Docs**: https://docs.djangoproject.com/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/

## Status

✅ Authentication system complete
✅ Login/Logout working
✅ Role-based dashboard working
✅ User profile working
✅ URL routing complete
⏳ Individual module pages (to be implemented)
⏳ Permission system (to be implemented)
⏳ Email verification (to be implemented)
⏳ 2FA implementation (to be implemented)
