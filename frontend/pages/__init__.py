"""
Dashboard Page Module
"""
from .dashboard import show as show_dashboard
from .students import show as show_students
from .admissions import show as show_admissions
from .academics import show as show_academics
from .hr import show as show_hr
from .library import show as show_library
from .finance import show as show_finance
from .reports import show as show_reports
from .settings import show as show_settings

__all__ = [
    'show_dashboard',
    'show_students',
    'show_admissions',
    'show_academics',
    'show_hr',
    'show_library',
    'show_finance',
    'show_reports',
    'show_settings'
]
