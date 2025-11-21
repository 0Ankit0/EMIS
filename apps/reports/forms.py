"""
Reports Forms
"""
from django import forms
from .models import ReportTemplate, GeneratedReport, ScheduledReport, ReportWidget


class ReportTemplateForm(forms.ModelForm):
    """Form for creating and updating report templates"""
    class Meta:
        model = ReportTemplate
        fields = [
            'name', 'code', 'description', 'category',
            'query_sql', 'data_source', 'parameters',
            'template_file', 'template_content',
            'supported_formats', 'default_format', 'page_size', 'orientation',
            'roles_allowed', 'is_public', 'is_active', 'is_scheduled'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Report name'
            }),
            'code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'unique-code'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Report description',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'query_sql': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono',
                'placeholder': 'SELECT * FROM ...',
                'rows': 6
            }),
            'data_source': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'module.function_name'
            }),
            'template_content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono',
                'rows': 10
            }),
        }


class GenerateReportForm(forms.Form):
    """Form for generating reports with parameters"""
    template = forms.ModelChoiceField(
        queryset=ReportTemplate.objects.active(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Report title'
        })
    )
    format = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
    
    def __init__(self, *args, **kwargs):
        template = kwargs.pop('template', None)
        super().__init__(*args, **kwargs)
        if template:
            self.fields['format'].choices = [
                (fmt, fmt.upper()) for fmt in template.supported_formats
            ]


class ScheduledReportForm(forms.ModelForm):
    """Form for scheduling reports"""
    class Meta:
        model = ScheduledReport
        fields = [
            'name', 'description', 'template', 'schedule_type',
            'cron_expression', 'scheduled_time', 'timezone',
            'parameters', 'format', 'recipients', 'recipient_emails', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Schedule name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3
            }),
            'template': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'schedule_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'scheduled_time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'time'
            }),
        }


class ReportWidgetForm(forms.ModelForm):
    """Form for report widgets"""
    class Meta:
        model = ReportWidget
        fields = [
            'name', 'template', 'widget_type', 'config',
            'default_parameters', 'order', 'width', 'roles_allowed', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Widget name'
            }),
            'template': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'widget_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
        }


class ReportParametersForm(forms.Form):
    """Dynamic form for report parameters"""
    
    def __init__(self, *args, **kwargs):
        parameters = kwargs.pop('parameters', {})
        super().__init__(*args, **kwargs)
        
        for param_name, param_config in parameters.items():
            param_type = param_config.get('type', 'text')
            label = param_config.get('label', param_name.replace('_', ' ').title())
            required = param_config.get('required', False)
            
            if param_type == 'text':
                field = forms.CharField(
                    label=label,
                    required=required,
                    widget=forms.TextInput(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
                    })
                )
            elif param_type == 'date':
                field = forms.DateField(
                    label=label,
                    required=required,
                    widget=forms.DateInput(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                        'type': 'date'
                    })
                )
            elif param_type == 'number':
                field = forms.IntegerField(
                    label=label,
                    required=required,
                    widget=forms.NumberInput(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
                    })
                )
            elif param_type == 'select':
                choices = param_config.get('choices', [])
                field = forms.ChoiceField(
                    label=label,
                    required=required,
                    choices=choices,
                    widget=forms.Select(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
                    })
                )
            else:
                field = forms.CharField(
                    label=label,
                    required=required,
                    widget=forms.TextInput(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
                    })
                )
            
            self.fields[param_name] = field
