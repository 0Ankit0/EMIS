"""
Faculty Filters
"""
import django_filters
from .models import Faculty, FacultyAttendance, FacultyLeave, Department


class FacultyFilter(django_filters.FilterSet):
    """Filter for Faculty"""
    name = django_filters.CharFilter(method='filter_by_name', label='Name')
    department = django_filters.ModelChoiceFilter(queryset=Department.objects.all())
    designation = django_filters.ChoiceFilter(choices=Faculty.DESIGNATION_CHOICES)
    status = django_filters.ChoiceFilter(choices=Faculty.STATUS_CHOICES)
    employment_type = django_filters.ChoiceFilter(choices=Faculty.EMPLOYMENT_TYPE_CHOICES)
    is_teaching = django_filters.BooleanFilter()
    is_research_active = django_filters.BooleanFilter()
    is_hod = django_filters.BooleanFilter()
    date_of_joining = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Faculty
        fields = ['department', 'designation', 'status', 'employment_type', 
                  'is_teaching', 'is_research_active', 'is_hod']
    
    def filter_by_name(self, queryset, name, value):
        """Filter by first name, middle name, or last name"""
        return queryset.filter(
            django_filters.Q(first_name__icontains=value) |
            django_filters.Q(middle_name__icontains=value) |
            django_filters.Q(last_name__icontains=value)
        )


class FacultyAttendanceFilter(django_filters.FilterSet):
    """Filter for FacultyAttendance"""
    faculty = django_filters.ModelChoiceFilter(queryset=Faculty.objects.all())
    date = django_filters.DateFromToRangeFilter()
    status = django_filters.ChoiceFilter(choices=FacultyAttendance.STATUS_CHOICES)
    
    class Meta:
        model = FacultyAttendance
        fields = ['faculty', 'date', 'status']


class FacultyLeaveFilter(django_filters.FilterSet):
    """Filter for FacultyLeave"""
    faculty = django_filters.ModelChoiceFilter(queryset=Faculty.objects.all())
    leave_type = django_filters.ChoiceFilter(choices=FacultyLeave.LEAVE_TYPE_CHOICES)
    status = django_filters.ChoiceFilter(choices=FacultyLeave.STATUS_CHOICES)
    start_date = django_filters.DateFromToRangeFilter()
    end_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = FacultyLeave
        fields = ['faculty', 'leave_type', 'status']

