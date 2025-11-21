# Role-Based Access Control (RBAC) Implementation Guide

## Overview

The EMIS system implements a comprehensive role-based access control system where:
- Each **app/module** has specific permission requirements
- Each **user** has one or more **roles** (Admin, Staff, Student, Faculty, etc.)
- Each **role** determines which **modules** the user can access
- Each **view** is protected with **decorators** that check permissions

## Role Types

### 1. **Superuser** (`is_superuser=True`)
- Full access to all modules and features
- Can access Django admin panel
- Bypasses all permission checks

### 2. **Staff** (`is_staff=True`)
- Full access to all administrative modules
- Can access Django admin panel
- Same access as superuser for most features

### 3. **Student** (`is_student=True`)
- Access to student portal modules:
  - My Profile
  - My Courses
  - My Grades
  - Fee Payments
  - Attendance
  - LMS Portal

### 4. **Faculty** (`is_faculty=True`)
- Access to faculty portal modules:
  - My Classes
  - Student Grades (can enter/update)
  - Attendance (can mark)
  - Course Materials (can upload/manage)

### 5. **Custom Roles** (via `UserRole` model)
- Librarian
- Accountant
- HR Manager
- etc.

## Module-to-Role Mapping

### Admin/Staff Modules
| Module | App | Required Role | Permissions |
|--------|-----|---------------|-------------|
| Student Management | `students` | `is_staff` | view, create, update, delete |
| Admissions | `admissions` | `is_staff` | view, create, update, approve |
| Academic Management | `courses` | `is_staff` | view, create, update, delete |
| Finance | `finance` | `is_staff` | view, create, update, delete |
| Exams & Grades | `exams` | `is_staff` | view, create, update, delete |
| Faculty | `faculty` | `is_staff` | view, create, update, delete |
| Library | `library` | `is_staff` | view, create, update, delete |
| Hostel | `hostel` | `is_staff` | view, create, update, delete |
| Timetable | `timetable` | `is_staff` | view, create, update, delete |
| LMS | `lms` | `is_staff` | view, create, update, delete |
| Reports & Analytics | `reports` | `is_staff` | view, export |
| Notifications | `notifications` | `is_staff` | view, create |

### Student Modules
| Module | App | Required Role | Permissions |
|--------|-----|---------------|-------------|
| My Profile | `students` | `is_student` | view, update |
| My Courses | `courses` | `is_student` | view |
| My Grades | `exams` | `is_student` | view |
| Fee Payments | `finance` | `is_student` | view |
| Attendance | `students` | `is_student` | view |
| LMS Portal | `lms` | `is_student` | view |

### Faculty Modules
| Module | App | Required Role | Permissions |
|--------|-----|---------------|-------------|
| My Classes | `courses` | `is_faculty` | view |
| Student Grades | `exams` | `is_faculty` | view, create, update |
| Attendance | `students` | `is_faculty` | view, create, update |
| Course Materials | `lms` | `is_faculty` | view, create, update, delete |

## Implementation Files

### 1. **Decorators** (`apps/core/decorators.py`)
Permission decorators for protecting views:

```python
from apps.core.decorators import (
    permission_required,
    admin_required,
    student_required,
    faculty_required,
    staff_or_faculty_required,
)

# Usage examples:

@admin_required
def admin_view(request):
    # Only admins can access
    pass

@student_required
def student_view(request):
    # Only students can access
    pass

@permission_required(allowed_roles=['is_staff', 'is_faculty'])
def mixed_view(request):
    # Staff or faculty can access
    pass

@permission_required(resource='students', action='update')
def specific_permission_view(request):
    # Requires specific resource permission
    pass
```

### 2. **Utilities** (`apps/core/utils.py`)
Helper functions for permission checking:

```python
from apps.core.utils import (
    get_user_modules,
    get_user_apps,
    can_access_app,
    user_has_permission,
)

# Get modules for user's dashboard
modules = get_user_modules(request.user)

# Get list of apps user can access
apps = get_user_apps(request.user)

# Check if user can access specific app
if can_access_app(request.user, 'students'):
    # User has access to students app
    pass

# Check specific permission
if user_has_permission(request.user, 'students', 'update'):
    # User can update students
    pass
```

### 3. **API Permissions** (`apps/core/permissions.py`)
DRF permission classes for API views:

```python
from apps.core.permissions import (
    IsStaffOrAdmin,
    IsFacultyOrAdmin,
    IsOwnerOrAdmin,
)

# Usage in API views:
class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrAdmin]
    # Only staff/admin can access
```

## Protecting Views by App

### Students App
```python
# apps/students/views.py
from apps.core.decorators import admin_required, student_required

@admin_required
def student_list(request):
    """Admin only - list all students"""
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

@student_required
def student_profile(request):
    """Student only - view own profile"""
    student = request.user.student
    return render(request, 'students/profile.html', {'student': student})
```

### Courses App
```python
# apps/courses/views.py
from apps.core.decorators import admin_required, student_required, faculty_required

@admin_required
def course_create(request):
    """Admin only - create courses"""
    pass

@student_required
def my_courses(request):
    """Student only - view enrolled courses"""
    pass

@faculty_required
def my_classes(request):
    """Faculty only - view assigned classes"""
    pass
```

### Finance App
```python
# apps/finance/views.py
from apps.core.decorators import admin_required, student_required

@admin_required
def invoice_list(request):
    """Admin only - manage all invoices"""
    pass

@student_required
def my_fees(request):
    """Student only - view own fees"""
    pass
```

### Exams App
```python
# apps/exams/views.py
from apps.core.decorators import admin_required, student_required, faculty_required

@admin_required
def exam_create(request):
    """Admin only - create exams"""
    pass

@student_required
def my_grades(request):
    """Student only - view own grades"""
    pass

@faculty_required
def enter_grades(request):
    """Faculty only - enter/update student grades"""
    pass
```

## URL Configuration

Each app should have its URLs organized by role:

```python
# apps/students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Admin URLs
    path('', views.student_list, name='list'),  # @admin_required
    path('<uuid:pk>/', views.student_detail, name='detail'),  # @admin_required
    path('create/', views.student_create, name='create'),  # @admin_required
    
    # Student portal URLs
    path('profile/', views.student_profile, name='profile'),  # @student_required
    path('courses/', views.student_courses, name='courses'),  # @student_required
    path('grades/', views.student_grades, name='grades'),  # @student_required
]
```

Then include in main URLs:
```python
# config/urls.py
urlpatterns = [
    path('students/', include('apps.students.urls')),
    path('courses/', include('apps.courses.urls')),
    path('finance/', include('apps.finance.urls')),
    # ... etc
]
```

## Testing Permissions

### Create Test Users
```python
# Create admin
admin = User.objects.create_superuser(
    username='admin',
    email='admin@emis.edu',
    password='admin123'
)

# Create student
student_user = User.objects.create_user(
    username='student1',
    email='student1@emis.edu',
    password='student123'
)
student_user.is_student = True
student_user.save()

# Create faculty
faculty_user = User.objects.create_user(
    username='faculty1',
    email='faculty1@emis.edu',
    password='faculty123'
)
faculty_user.is_faculty = True
faculty_user.save()
```

### Test Access
```python
# Test student accessing admin view
from django.test import Client

client = Client()
client.login(username='student1', password='student123')
response = client.get('/students/')  # Should redirect with error
assert response.status_code == 302  # Redirected

# Test admin accessing admin view
client.login(username='admin', password='admin123')
response = client.get('/students/')  # Should work
assert response.status_code == 200  # Success
```

## Best Practices

### 1. **Always Use Decorators**
Never create unprotected views. Always use at least `@login_required`.

### 2. **Principle of Least Privilege**
Give users only the minimum access they need.

### 3. **Check Ownership**
For views that show user-specific data, always verify ownership:
```python
@student_required
def student_grades(request):
    student = request.user.student
    grades = student.grade_records.all()  # Only own grades
    # NOT: GradeRecord.objects.all()  # Would show all grades!
```

### 4. **Use Mixins for Class-Based Views**
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.mixins import AdminRequiredMixin

class StudentListView(AdminRequiredMixin, ListView):
    model = Student
```

### 5. **Consistent Error Messages**
Use the built-in message system for permission errors:
```python
if not user.has_permission():
    messages.error(request, 'You do not have permission to access this page.')
    return redirect('core:dashboard')
```

## Common Patterns

### Pattern 1: Admin or Owner
```python
@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Admin can view any student
    if request.user.is_staff:
        pass
    # Student can only view own profile
    elif request.user.is_student and request.user.student == student:
        pass
    else:
        messages.error(request, 'Permission denied.')
        return redirect('core:dashboard')
    
    return render(request, 'students/detail.html', {'student': student})
```

### Pattern 2: Multiple Roles
```python
@permission_required(allowed_roles=['is_staff', 'is_faculty'])
def attendance_mark(request):
    # Staff and faculty can mark attendance
    pass
```

### Pattern 3: Granular Permissions
```python
@login_required
def student_update(request, pk):
    if not user_has_permission(request.user, 'students', 'update'):
        messages.error(request, 'You cannot update student records.')
        return redirect('core:dashboard')
    
    # Proceed with update
    pass
```

## Checklist for Each New View

- [ ] Add `@login_required` decorator (minimum)
- [ ] Add role-specific decorator (`@admin_required`, `@student_required`, etc.)
- [ ] Verify user owns the resource (if applicable)
- [ ] Add permission check in template
- [ ] Test with different user roles
- [ ] Add to appropriate URL pattern
- [ ] Document in module mapping

## Troubleshooting

### Issue: User can't access module they should have access to
1. Check user role flags: `user.is_staff`, `user.is_student`, etc.
2. Check custom roles: `user.user_roles.all()`
3. Verify decorator is correct for the view
4. Check URL is correct in dashboard module

### Issue: User can access module they shouldn't
1. Check if decorator is missing from view
2. Verify decorator logic is correct
3. Check if user has superuser access

### Issue: Permission denied but should work
1. Check if user is authenticated
2. Verify role flags are set correctly
3. Check decorator allowed_roles list
4. Review permission logic in decorator

## Summary

✅ Roles: Superuser, Staff, Student, Faculty, Custom
✅ Decorators: `@admin_required`, `@student_required`, `@faculty_required`
✅ Utilities: `get_user_modules()`, `can_access_app()`, `user_has_permission()`
✅ Dashboard: Auto-generates modules based on user roles
✅ Views: Protected with decorators
✅ URLs: Organized by role (admin vs portal)
✅ Testing: Create users with different roles and test access
