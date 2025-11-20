"""
Analytics Forms
"""
from django import forms
from .models import Report, AnalyticsQuery


class ReportForm(forms.ModelForm):
    """
    Form for creating and configuring reports
    """
    class Meta:
        model = Report
        fields = ['title', 'report_type', 'description', 'format', 'parameters', 'filters']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Report Title'
            }),
            'report_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Report description',
                'rows': 3
            }),
            'format': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'parameters': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono',
                'placeholder': '{"start_date": "2024-01-01", "end_date": "2024-12-31"}',
                'rows': 4
            }),
            'filters': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono',
                'placeholder': '{"program": "Computer Science", "status": "active"}',
                'rows': 4
            }),
        }


class AnalyticsQueryForm(forms.ModelForm):
    """
    Form for creating analytics queries
    """
    class Meta:
        model = AnalyticsQuery
        fields = ['name', 'description', 'query_type', 'query_config', 'visualization_config', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Query Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Query description',
                'rows': 3
            }),
            'query_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., student_performance, attendance_rate'
            }),
            'query_config': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono',
                'placeholder': '{"model": "Student", "filters": {}, "aggregations": []}',
                'rows': 6
            }),
            'visualization_config': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono',
                'placeholder': '{"chart_type": "bar", "x_axis": "program", "y_axis": "count"}',
                'rows': 6
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 rounded focus:ring-blue-500'
            }),
        }


class DateRangeFilterForm(forms.Form):
    """Form for date range filtering"""
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        }),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        }),
        required=False
    )
