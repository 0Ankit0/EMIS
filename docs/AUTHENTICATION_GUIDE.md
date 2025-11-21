# EMIS Authentication & Authorization System

## Overview
Complete role-based access control system with authentication, authorization, and modular dashboard.

## Key Features

### 1. Authentication System
- ✅ Login page with beautiful gradient UI
- ✅ Password reset (placeholder)
- ✅ User profile management
- ✅ Session management
- ✅ 2FA setup (placeholder)
- ✅ Logout functionality

### 2. Authorization & Roles
- ✅ Role-based access control
- ✅ Permission-based module visibility
- ✅ Superuser/Admin full access
- ✅ Staff member access
- ✅ Student portal modules
- ✅ Faculty portal modules

### 3. Dashboard System
- ✅ Dynamic module cards based on user role
- ✅ Color-coded modules by category
- ✅ Quick statistics for admin/staff
- ✅ Responsive grid layout
- ✅ Hover effects and smooth animations

## URL Structure

### Public URLs
- `/` - Redirects to login if not authenticated, dashboard if authenticated
- `/auth/login/` - Login page
- `/auth/register/` - Registration (admin only message)
- `/auth/password-reset/` - Password reset request

### Protected URLs (require login)
- `/dashboard/` - Main dashboard with role-based modules
- `/auth/profile/` - User profile page
- `/auth/password-change/` - Password change page
- `/auth/setup-2fa/` - Two-factor authentication setup
- `/auth/logout/` - Logout

### Admin URLs
- `/admin/` - Django admin panel

## User Roles & Module Access

### Superuser/Administrator
Gets access to ALL modules:
- Student Management
- Admissions
- Academic Management
- Finance
- Exams & Grades
- Faculty
- Library
- Hostel
- Timetable
- Reports & Analytics
- Notifications
- Settings

### Staff Members
Same as Superuser - full access to all administrative modules

### Students (`is_student=True` or role='student'`)
- My Profile
- My Courses
- My Grades
- Fee Payments
- Attendance

### Faculty (`is_faculty=True` or role='faculty'`)
- My Classes
- Student Grades
- Attendance
- Course Materials

## Settings Configuration

```python
# Authentication URLs
LOGIN_URL = 'authentication:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'authentication:login'
```

## Templates Created

### Authentication Templates
1. `templates/authentication/login.html` - Modern gradient login page
2. `templates/authentication/profile.html` - User profile with info display
3. `templates/authentication/password_reset.html` - Password reset request
4. `templates/authentication/password_change.html` - Password change form
5. `templates/authentication/setup_2fa.html` - 2FA setup page
6. `templates/authentication/register.html` - Registration info page

### Core Templates
1. `templates/core/dashboard.html` - Role-based dashboard with modules
2. `templates/base.html` - Base template with navbar for authenticated users

## Views & Logic

### Core Views (`apps/core/views.py`)
- `home()` - Redirects to login or dashboard based on auth status
- `dashboard()` - Displays role-based module cards

### Authentication Views (`apps/authentication/views.py`)
- `login_view()` - Handles login with username/email + password
- `profile_view()` - Displays user profile information
- `password_reset_view()` - Password reset (placeholder)
- `password_change_view()` - Password change (placeholder)
- `setup_2fa_view()` - 2FA setup (placeholder)

## Module Card Structure

Each module card contains:
```python
{
    'name': 'Module Name',
    'description': 'Module description',
    'icon': 'fa-icon-name',  # FontAwesome icon
    'color': 'primary|success|info|warning|danger|secondary',
    'url': '/path/to/module/',  # Optional
}
```

## Security Features

### Login Required
All protected pages use `@login_required` decorator to ensure authentication.

### Role-Based Access
Dashboard logic checks:
- `user.is_superuser` - Full admin access
- `user.is_staff` - Staff access
- `user.is_student` - Student portal
- `user.is_faculty` - Faculty portal
- `user.user_roles.all()` - Dynamic role assignments

### Session Management
- Sessions stored in Redis cache
- Configurable session timeout
- Remember me functionality

## Test Credentials

### Administrator
- Username: `admin`
- Password: `admin123`
- Email: `admin@emis.edu`

## Usage Flow

1. **First Visit**: User visits `/` → Redirected to `/auth/login/`
2. **Login**: User enters credentials → Authenticated
3. **Dashboard**: User redirected to `/dashboard/` → Sees role-based modules
4. **Module Access**: User clicks module card → Opens respective section
5. **Profile**: User can view/edit profile via navbar or dashboard
6. **Logout**: User logs out → Redirected to login page

## Module Icons & Colors

### Color Scheme
- **Primary** (Blue): Core modules, user-related
- **Success** (Green): Academic, admissions
- **Info** (Cyan): Courses, library
- **Warning** (Yellow): Finance, reports
- **Danger** (Red): Exams, critical functions
- **Secondary** (Gray): Settings, utilities

### Icon Mapping
- `fa-users` - Student Management
- `fa-user-graduate` - Admissions
- `fa-book` - Academic/Courses
- `fa-dollar-sign` - Finance
- `fa-clipboard-check` - Exams
- `fa-chalkboard-teacher` - Faculty
- `fa-book-open` - Library
- `fa-building` - Hostel
- `fa-calendar-alt` - Timetable
- `fa-chart-line` - Analytics
- `fa-bell` - Notifications
- `fa-cogs` - Settings

## Next Steps for Full Implementation

### 1. Student Module Views
Create views for:
- Student profile viewing/editing
- Course enrollment viewing
- Grade viewing
- Fee payment processing
- Attendance viewing

### 2. Faculty Module Views  
Create views for:
- Class management
- Grade entry
- Attendance marking
- Course material upload

### 3. Admin Module Views
Create full CRUD interfaces for:
- Student management
- Faculty management
- Course management
- Financial management
- Exam management

### 4. Permission System
Implement granular permissions:
- View, Create, Update, Delete permissions per module
- Resource group-based access control
- Role-permission mapping from database

### 5. Additional Features
- Email verification
- Password reset via email
- 2FA with TOTP
- Audit logging
- Activity tracking
- Notification system

## File Structure

```
EMIS/
├── apps/
│   ├── authentication/
│   │   ├── views.py (login, profile, etc.)
│   │   ├── urls.py (auth URL patterns)
│   │   └── models.py (User, Role, Permission)
│   └── core/
│       ├── views.py (home, dashboard)
│       └── urls.py (core URL patterns)
├── templates/
│   ├── authentication/
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── password_reset.html
│   │   ├── password_change.html
│   │   ├── setup_2fa.html
│   │   └── register.html
│   ├── core/
│   │   └── dashboard.html
│   └── base.html
└── config/
    ├── settings.py (LOGIN_URL, etc.)
    └── urls.py (main URL config)
```

## Design Highlights

### Login Page
- Gradient purple background
- Centered card layout
- FontAwesome icons
- Error message display
- Remember me checkbox
- Links to password reset and admin

### Dashboard
- Welcome header with user info
- Role badge display
- Module grid (3-4 columns responsive)
- Hover effects on cards
- Quick statistics for admin
- Profile and logout buttons

### Module Cards
- Icon with colored background
- Module name and description
- Action button
- Smooth hover animation
- Color-coded by category

## Responsive Design
- Mobile-first approach
- Bootstrap 5 grid system
- Cards stack on mobile
- Touch-friendly buttons
- Optimized for all screen sizes
