"""
Faculty Serializers
"""
from .department import DepartmentSerializer
from .qualification import FacultyQualificationSerializer
from .experience import FacultyExperienceSerializer
from .publication import FacultyPublicationSerializer
from .award import FacultyAwardSerializer
from .faculty import (
    FacultyListSerializer,
    FacultyDetailSerializer,
    FacultyCreateUpdateSerializer
)
from .attendance import FacultyAttendanceSerializer
from .leave import FacultyLeaveSerializer

__all__ = [
    'DepartmentSerializer',
    'FacultyQualificationSerializer',
    'FacultyExperienceSerializer',
    'FacultyPublicationSerializer',
    'FacultyAwardSerializer',
    'FacultyListSerializer',
    'FacultyDetailSerializer',
    'FacultyCreateUpdateSerializer',
    'FacultyAttendanceSerializer',
    'FacultyLeaveSerializer',
]
