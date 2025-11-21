"""
Utility functions for permissions and role management
"""


def user_has_permission(user, resource, action):
    """
    Check if user has permission for a resource action
    
    Args:
        user: User object
        resource: Resource name (e.g., 'students', 'courses')
        action: Action name (e.g., 'view', 'create', 'update', 'delete')
    
    Returns:
        bool: True if user has permission
    """
    # Superuser has all permissions
    if user.is_superuser:
        return True
    
    # Staff has most permissions
    if user.is_staff:
        return True
    
    # Check granular permissions from database
    if hasattr(user, 'user_roles'):
        for user_role in user.user_roles.all():
            role = user_role.role
            # Check if role has permission for this resource/action
            if hasattr(role, 'role_permissions'):
                for role_permission in role.role_permissions.all():
                    permission = role_permission.permission
                    if (permission.resource_group.name == resource and 
                        permission.action == action):
                        return True
    
    return False


def get_user_modules(user):
    """
    Get list of modules user has access to based on their roles
    
    Args:
        user: User object
    
    Returns:
        list: List of module dictionaries
    """
    modules = []
    
    # Admin/Staff modules
    if user.is_superuser or user.is_staff:
        modules.extend([
            {
                'name': 'Student Management',
                'description': 'Manage student records, enrollments, and profiles',
                'icon': 'fa-users',
                'color': 'primary',
                'url': '/students/',
                'app': 'students',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Admissions',
                'description': 'Process applications and manage admissions',
                'icon': 'fa-user-graduate',
                'color': 'success',
                'url': '/admissions/',
                'app': 'admissions',
                'permissions': ['view', 'create', 'update', 'approve']
            },
            {
                'name': 'Attendance',
                'description': 'Track and manage student attendance',
                'icon': 'fa-clipboard-check',
                'color': 'info',
                'url': '/attendance/',
                'app': 'attendance',
                'permissions': ['view', 'create', 'update']
            },
            {
                'name': 'Courses',
                'description': 'Course and curriculum management',
                'icon': 'fa-book-open',
                'color': 'primary',
                'url': '/courses/',
                'app': 'courses',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Exams & Grades',
                'description': 'Examination management and grade records',
                'icon': 'fa-file-alt',
                'color': 'danger',
                'url': '/exams/',
                'app': 'exams',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Finance',
                'description': 'Fee management, invoices, and payments',
                'icon': 'fa-dollar-sign',
                'color': 'warning',
                'url': '/finance/',
                'app': 'finance',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Library',
                'description': 'Library resources and book management',
                'icon': 'fa-book',
                'color': 'primary',
                'url': '/library/',
                'app': 'library',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'LMS',
                'description': 'Learning management system',
                'icon': 'fa-graduation-cap',
                'color': 'info',
                'url': '/lms/',
                'app': 'lms',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Faculty',
                'description': 'Faculty records and assignments',
                'icon': 'fa-chalkboard-teacher',
                'color': 'success',
                'url': '/faculty/',
                'app': 'faculty',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Timetable',
                'description': 'Class schedules and timetable management',
                'icon': 'fa-calendar-week',
                'color': 'danger',
                'url': '/timetable/',
                'app': 'timetable',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'HR Management',
                'description': 'Human resources and employee management',
                'icon': 'fa-user-friends',
                'color': 'warning',
                'url': '/hr/',
                'app': 'hr',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Analytics',
                'description': 'View analytics and insights',
                'icon': 'fa-chart-pie',
                'color': 'info',
                'url': '/analytics/',
                'app': 'analytics',
                'permissions': ['view', 'export']
            },
            {
                'name': 'Hostel',
                'description': 'Hostel room allocation and management',
                'icon': 'fa-building',
                'color': 'success',
                'url': '/hostel/',
                'app': 'hostel',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Transport',
                'description': 'Transportation and vehicle management',
                'icon': 'fa-bus',
                'color': 'primary',
                'url': '/transport/',
                'app': 'transport',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Inventory',
                'description': 'Inventory and stock management',
                'icon': 'fa-boxes',
                'color': 'warning',
                'url': '/inventory/',
                'app': 'inventory',
                'permissions': ['view', 'create', 'update', 'delete']
            },
            {
                'name': 'Reports',
                'description': 'Generate reports and analytics',
                'icon': 'fa-chart-bar',
                'color': 'info',
                'url': '/reports/',
                'app': 'reports',
                'permissions': ['view', 'export']
            },
            {
                'name': 'Notifications',
                'description': 'System notifications and announcements',
                'icon': 'fa-bell',
                'color': 'danger',
                'url': '/notifications/',
                'app': 'notifications',
                'permissions': ['view', 'create']
            },
            {
                'name': 'CMS',
                'description': 'Content Management System',
                'icon': 'fa-file-alt',
                'color': 'secondary',
                'url': '/cms/',
                'app': 'cms',
                'permissions': ['view', 'create', 'update', 'delete']
            },
        ])
    
    # Student modules
    if user.is_student:
        modules.extend([
            {
                'name': 'My Profile',
                'description': 'View and update your student profile',
                'icon': 'fa-user',
                'color': 'primary',
                'url': '/students/profile/',
                'app': 'students',
                'permissions': ['view', 'update']
            },
            {
                'name': 'My Courses',
                'description': 'View your enrolled courses',
                'icon': 'fa-book',
                'color': 'success',
                'url': '/students/courses/',
                'app': 'courses',
                'permissions': ['view']
            },
            {
                'name': 'My Grades',
                'description': 'View your exam results and grades',
                'icon': 'fa-certificate',
                'color': 'info',
                'url': '/students/grades/',
                'app': 'exams',
                'permissions': ['view']
            },
            {
                'name': 'Fee Payments',
                'description': 'View and pay your fees',
                'icon': 'fa-money-bill',
                'color': 'warning',
                'url': '/students/fees/',
                'app': 'finance',
                'permissions': ['view']
            },
            {
                'name': 'Attendance',
                'description': 'View your attendance records',
                'icon': 'fa-calendar-check',
                'color': 'danger',
                'url': '/students/attendance/',
                'app': 'students',
                'permissions': ['view']
            },
            {
                'name': 'LMS Portal',
                'description': 'Access learning materials and assignments',
                'icon': 'fa-laptop',
                'color': 'secondary',
                'url': '/lms/student/',
                'app': 'lms',
                'permissions': ['view']
            },
        ])
    
    # Faculty modules
    if user.is_faculty:
        modules.extend([
            {
                'name': 'My Classes',
                'description': 'View your assigned classes',
                'icon': 'fa-chalkboard',
                'color': 'primary',
                'url': '/faculty/classes/',
                'app': 'courses',
                'permissions': ['view']
            },
            {
                'name': 'Student Grades',
                'description': 'Enter and manage student grades',
                'icon': 'fa-clipboard-list',
                'color': 'success',
                'url': '/faculty/grades/',
                'app': 'exams',
                'permissions': ['view', 'create', 'update']
            },
            {
                'name': 'Attendance',
                'description': 'Mark student attendance',
                'icon': 'fa-user-check',
                'color': 'info',
                'url': '/faculty/attendance/',
                'app': 'students',
                'permissions': ['view', 'create', 'update']
            },
            {
                'name': 'Course Materials',
                'description': 'Upload and manage course materials',
                'icon': 'fa-folder-open',
                'color': 'warning',
                'url': '/faculty/materials/',
                'app': 'lms',
                'permissions': ['view', 'create', 'update', 'delete']
            },
        ])
    
    # Remove duplicates based on name
    seen_names = set()
    unique_modules = []
    for module in modules:
        if module['name'] not in seen_names:
            seen_names.add(module['name'])
            unique_modules.append(module)
    
    return unique_modules


def get_user_apps(user):
    """
    Get list of app names user has access to
    
    Args:
        user: User object
    
    Returns:
        set: Set of app names
    """
    modules = get_user_modules(user)
    return set(module['app'] for module in modules)


def can_access_app(user, app_name):
    """
    Check if user can access a specific app
    
    Args:
        user: User object
        app_name: Name of the app (e.g., 'students', 'finance')
    
    Returns:
        bool: True if user can access the app
    """
    if user.is_superuser or user.is_staff:
        return True
    
    user_apps = get_user_apps(user)
    return app_name in user_apps
