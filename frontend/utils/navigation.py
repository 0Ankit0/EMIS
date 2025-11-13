"""
Navigation utilities for role-based menus
"""
from typing import Dict, List


def get_menu_items(role: str) -> List[Dict]:
    """Get menu items based on user role"""
    
    # Common menu items for all roles
    common_items = [
        {
            "title": "Dashboard",
            "icon": "speedometer2",
            "page": "dashboard"
        },
        {
            "title": "Profile",
            "icon": "person",
            "page": "profile"
        },
    ]
    
    # Role-specific menu items
    role_menus = {
        "student": [
            {
                "title": "My Courses",
                "icon": "book",
                "page": "student_courses"
            },
            {
                "title": "Assignments",
                "icon": "clipboard-check",
                "page": "student_assignments"
            },
            {
                "title": "Attendance",
                "icon": "calendar-check",
                "page": "student_attendance"
            },
            {
                "title": "Exams & Results",
                "icon": "trophy",
                "page": "student_exams"
            },
            {
                "title": "Fees & Payments",
                "icon": "currency-dollar",
                "page": "student_fees"
            },
            {
                "title": "Library",
                "icon": "journal-text",
                "page": "student_library"
            },
        ],
        "teacher": [
            {
                "title": "My Courses",
                "icon": "book",
                "page": "faculty_courses"
            },
            {
                "title": "Attendance",
                "icon": "calendar-check",
                "page": "faculty_attendance"
            },
            {
                "title": "Assignments",
                "icon": "clipboard-check",
                "page": "faculty_assignments"
            },
            {
                "title": "Grading",
                "icon": "award",
                "page": "faculty_grading"
            },
            {
                "title": "Timetable",
                "icon": "calendar3",
                "page": "faculty_timetable"
            },
        ],
        "staff": [
            {
                "title": "Students",
                "icon": "people",
                "page": "students"
            },
            {
                "title": "Admissions",
                "icon": "file-earmark-text",
                "page": "admissions"
            },
            {
                "title": "Library",
                "icon": "journal-text",
                "page": "library"
            },
            {
                "title": "Reports",
                "icon": "bar-chart",
                "page": "reports"
            },
        ],
        "admin": [
            {
                "title": "Students",
                "icon": "people",
                "page": "students"
            },
            {
                "title": "Admissions",
                "icon": "file-earmark-text",
                "page": "admissions"
            },
            {
                "title": "Academics",
                "icon": "book",
                "page": "academics"
            },
            {
                "title": "HR & Payroll",
                "icon": "briefcase",
                "page": "hr"
            },
            {
                "title": "Library",
                "icon": "journal-text",
                "page": "library"
            },
            {
                "title": "Finance",
                "icon": "currency-dollar",
                "page": "finance"
            },
            {
                "title": "Reports",
                "icon": "bar-chart",
                "page": "reports"
            },
            {
                "title": "Settings",
                "icon": "gear",
                "page": "settings"
            },
        ]
    }
    
    # Get role-specific items, default to staff if role not found
    menu_items = common_items + role_menus.get(role, role_menus["staff"])
    
    return menu_items


def get_page_title(page_key: str) -> str:
    """Get page title from page key"""
    titles = {
        "dashboard": "Dashboard",
        "profile": "My Profile",
        # Student pages
        "student_courses": "My Courses",
        "student_assignments": "Assignments",
        "student_attendance": "Attendance",
        "student_exams": "Exams & Results",
        "student_fees": "Fees & Payments",
        "student_library": "Library",
        # Faculty pages
        "faculty_courses": "My Courses",
        "faculty_attendance": "Mark Attendance",
        "faculty_assignments": "Assignments",
        "faculty_grading": "Grading",
        "faculty_timetable": "Timetable",
        # Admin pages
        "students": "Students Management",
        "admissions": "Admissions",
        "academics": "Academics",
        "hr": "HR & Payroll",
        "library": "Library Management",
        "finance": "Finance",
        "reports": "Reports",
        "settings": "System Settings",
    }
    return titles.get(page_key, page_key.replace("_", " ").title())
