"""
Reports Views - Complete Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from django.core.files.base import ContentFile
import time
import json

from .models import (
    ReportTemplate, GeneratedReport, ScheduledReport,
    ReportWidget, ReportFavorite, ReportAccessLog
)
from .forms import (
    ReportTemplateForm, GenerateReportForm, ScheduledReportForm,
    ReportWidgetForm, ReportParametersForm
)
from .filters import ReportTemplateFilter, GeneratedReportFilter, ScheduledReportFilter
from .utils import (
    execute_report_query, generate_pdf_report, generate_excel_report,
    generate_csv_report, generate_html_report, log_report_access,
    calculate_next_run, validate_report_parameters
)


# Dashboard
@login_required
def dashboard(request):
    """Reports dashboard"""
    templates = ReportTemplate.objects.for_user(request.user)
    recent_reports = GeneratedReport.objects.for_user(request.user).completed()[:5]
    favorites = ReportFavorite.objects.filter(user=request.user).select_related('template')
    
    stats = {
        'total_templates': templates.count(),
        'total_generated': GeneratedReport.objects.for_user(request.user).count(),
        'favorites_count': favorites.count(),
        'pending_reports': GeneratedReport.objects.for_user(request.user).pending().count(),
    }
    
    context = {
        'stats': stats,
        'recent_reports': recent_reports,
        'favorites': favorites,
        'templates_by_category': templates.values('category').annotate(count=Count('id')),
    }
    
    return render(request, 'reports/dashboard.html', context)


# Report Templates
@login_required
def template_list(request):
    """List all report templates"""
    templates = ReportTemplate.objects.for_user(request.user)
    
    filter_instance = ReportTemplateFilter(request.GET, queryset=templates)
    templates = filter_instance.qs
    
    paginator = Paginator(templates, 20)
    page = request.GET.get('page')
    templates_page = paginator.get_page(page)
    
    context = {
        'templates': templates_page,
        'filter': filter_instance,
    }
    
    return render(request, 'reports/template_list.html', context)


@login_required
def template_detail(request, pk):
    """View report template details"""
    template = get_object_or_404(ReportTemplate, pk=pk)
    
    # Check permissions
    if not template.is_public and not request.user.is_staff:
        if hasattr(request.user, 'student') and 'student' not in template.roles_allowed:
            messages.error(request, "You don't have permission to access this report.")
            return redirect('reports:template_list')
    
    recent_generated = GeneratedReport.objects.filter(
        template=template,
        generated_by=request.user
    ).order_by('-generated_at')[:10]
    
    is_favorite = ReportFavorite.objects.filter(
        user=request.user,
        template=template
    ).exists()
    
    context = {
        'template': template,
        'recent_generated': recent_generated,
        'is_favorite': is_favorite,
    }
    
    return render(request, 'reports/template_detail.html', context)


@login_required
def template_create(request):
    """Create new report template"""
    if not request.user.is_staff:
        messages.error(request, "Only staff can create report templates.")
        return redirect('reports:template_list')
    
    if request.method == 'POST':
        form = ReportTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.save()
            messages.success(request, "Report template created successfully.")
            return redirect('reports:template_detail', pk=template.pk)
    else:
        form = ReportTemplateForm()
    
    context = {'form': form}
    return render(request, 'reports/template_form.html', context)


@login_required
def template_update(request, pk):
    """Update report template"""
    template = get_object_or_404(ReportTemplate, pk=pk)
    
    if not request.user.is_staff:
        messages.error(request, "Only staff can update report templates.")
        return redirect('reports:template_detail', pk=pk)
    
    if request.method == 'POST':
        form = ReportTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, "Report template updated successfully.")
            return redirect('reports:template_detail', pk=pk)
    else:
        form = ReportTemplateForm(instance=template)
    
    context = {'form': form, 'template': template}
    return render(request, 'reports/template_form.html', context)


@login_required
@require_http_methods(["POST"])
def template_delete(request, pk):
    """Delete report template"""
    template = get_object_or_404(ReportTemplate, pk=pk)
    
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    template.delete()
    messages.success(request, "Report template deleted successfully.")
    return redirect('reports:template_list')


# Report Generation
@login_required
def generate_report(request, template_id):
    """Generate a report from template"""
    template = get_object_or_404(ReportTemplate, pk=template_id)
    
    if request.method == 'POST':
        param_form = ReportParametersForm(request.POST, parameters=template.parameters)
        
        if param_form.is_valid():
            try:
                parameters = param_form.cleaned_data
                validated_params = validate_report_parameters(parameters, template.parameters)
                
                # Create generated report record
                generated_report = GeneratedReport.objects.create(
                    template=template,
                    title=request.POST.get('title', template.name),
                    generated_by=request.user,
                    parameters=validated_params,
                    format=request.POST.get('format', template.default_format),
                    status='processing'
                )
                
                # Generate report asynchronously or synchronously
                try:
                    start_time = time.time()
                    
                    # Execute query or call data source
                    if template.query_sql:
                        data = execute_report_query(template.query_sql, validated_params)
                    elif template.data_source:
                        # Dynamic import and call
                        module_path, function_name = template.data_source.rsplit('.', 1)
                        module = __import__(module_path, fromlist=[function_name])
                        data_function = getattr(module, function_name)
                        data = data_function(validated_params)
                    else:
                        data = []
                    
                    # Define columns (simplified - should come from template config)
                    columns = [{'key': key, 'label': key.replace('_', ' ').title()} 
                              for key in data[0].keys()] if data else []
                    
                    # Generate output in requested format
                    output_format = generated_report.format
                    
                    if output_format == 'pdf':
                        file_buffer = generate_pdf_report(generated_report.title, data, columns)
                        file_ext = 'pdf'
                    elif output_format == 'excel':
                        file_buffer = generate_excel_report(generated_report.title, data, columns)
                        file_ext = 'xlsx'
                    elif output_format == 'csv':
                        csv_content = generate_csv_report(data, columns)
                        file_buffer = BytesIO(csv_content.encode('utf-8'))
                        file_ext = 'csv'
                    elif output_format == 'html':
                        html_content = generate_html_report(generated_report.title, data, columns)
                        file_buffer = BytesIO(html_content.encode('utf-8'))
                        file_ext = 'html'
                    else:
                        file_buffer = BytesIO(json.dumps(data, indent=2).encode('utf-8'))
                        file_ext = 'json'
                    
                    # Save file
                    filename = f"report_{generated_report.id}.{file_ext}"
                    generated_report.file.save(filename, ContentFile(file_buffer.getvalue()))
                    generated_report.file_size = file_buffer.getbuffer().nbytes
                    generated_report.record_count = len(data)
                    generated_report.generation_time = time.time() - start_time
                    generated_report.status = 'completed'
                    generated_report.save()
                    
                    # Log access
                    log_report_access(request.user, template, 'generate', request, generated_report)
                    
                    messages.success(request, "Report generated successfully.")
                    return redirect('reports:generated_detail', pk=generated_report.pk)
                    
                except Exception as e:
                    generated_report.status = 'failed'
                    generated_report.error_message = str(e)
                    generated_report.save()
                    messages.error(request, f"Failed to generate report: {str(e)}")
                    
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        param_form = ReportParametersForm(parameters=template.parameters)
    
    context = {
        'template': template,
        'param_form': param_form,
    }
    
    return render(request, 'reports/generate_report.html', context)


# Generated Reports
@login_required
def generated_list(request):
    """List generated reports"""
    reports = GeneratedReport.objects.for_user(request.user)
    
    filter_instance = GeneratedReportFilter(request.GET, queryset=reports)
    reports = filter_instance.qs
    
    paginator = Paginator(reports, 20)
    page = request.GET.get('page')
    reports_page = paginator.get_page(page)
    
    context = {
        'reports': reports_page,
        'filter': filter_instance,
    }
    
    return render(request, 'reports/generated_list.html', context)


@login_required
def generated_detail(request, pk):
    """View generated report details"""
    report = get_object_or_404(GeneratedReport, pk=pk)
    
    if report.generated_by != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this report.")
        return redirect('reports:generated_list')
    
    context = {'report': report}
    return render(request, 'reports/generated_detail.html', context)


@login_required
def download_report(request, pk):
    """Download generated report"""
    report = get_object_or_404(GeneratedReport, pk=pk)
    
    if report.generated_by != request.user and not request.user.is_staff:
        return HttpResponse("Permission denied", status=403)
    
    if not report.file:
        messages.error(request, "Report file not found.")
        return redirect('reports:generated_detail', pk=pk)
    
    # Update download stats
    report.download_count += 1
    report.last_downloaded_at = timezone.now()
    report.save(update_fields=['download_count', 'last_downloaded_at'])
    
    # Log access
    log_report_access(request.user, report.template, 'download', request, report)
    
    # Determine content type
    content_types = {
        'pdf': 'application/pdf',
        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'csv': 'text/csv',
        'html': 'text/html',
        'json': 'application/json',
    }
    
    content_type = content_types.get(report.format, 'application/octet-stream')
    
    response = FileResponse(report.file.open('rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{report.file.name.split("/")[-1]}"'
    
    return response


@login_required
@require_http_methods(["POST"])
def delete_generated(request, pk):
    """Delete generated report"""
    report = get_object_or_404(GeneratedReport, pk=pk)
    
    if report.generated_by != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Delete file
    if report.file:
        report.file.delete()
    
    report.delete()
    messages.success(request, "Report deleted successfully.")
    return redirect('reports:generated_list')


# Scheduled Reports
@login_required
def scheduled_list(request):
    """List scheduled reports"""
    if not request.user.is_staff:
        scheduled = ScheduledReport.objects.filter(created_by=request.user)
    else:
        scheduled = ScheduledReport.objects.all()
    
    filter_instance = ScheduledReportFilter(request.GET, queryset=scheduled)
    scheduled = filter_instance.qs
    
    paginator = Paginator(scheduled, 20)
    page = request.GET.get('page')
    scheduled_page = paginator.get_page(page)
    
    context = {
        'scheduled_reports': scheduled_page,
        'filter': filter_instance,
    }
    
    return render(request, 'reports/scheduled_list.html', context)


@login_required
def scheduled_create(request):
    """Create scheduled report"""
    if request.method == 'POST':
        form = ScheduledReportForm(request.POST)
        if form.is_valid():
            scheduled = form.save(commit=False)
            scheduled.created_by = request.user
            
            # Calculate next run
            scheduled.next_run = calculate_next_run(
                scheduled.schedule_type,
                scheduled.scheduled_time,
                scheduled.timezone
            )
            scheduled.save()
            form.save_m2m()
            
            messages.success(request, "Scheduled report created successfully.")
            return redirect('reports:scheduled_list')
    else:
        form = ScheduledReportForm()
    
    context = {'form': form}
    return render(request, 'reports/scheduled_form.html', context)


@login_required
def scheduled_update(request, pk):
    """Update scheduled report"""
    scheduled = get_object_or_404(ScheduledReport, pk=pk)
    
    if scheduled.created_by != request.user and not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect('reports:scheduled_list')
    
    if request.method == 'POST':
        form = ScheduledReportForm(request.POST, instance=scheduled)
        if form.is_valid():
            scheduled = form.save(commit=False)
            scheduled.next_run = calculate_next_run(
                scheduled.schedule_type,
                scheduled.scheduled_time,
                scheduled.timezone
            )
            scheduled.save()
            form.save_m2m()
            
            messages.success(request, "Scheduled report updated successfully.")
            return redirect('reports:scheduled_list')
    else:
        form = ScheduledReportForm(instance=scheduled)
    
    context = {'form': form, 'scheduled': scheduled}
    return render(request, 'reports/scheduled_form.html', context)


@login_required
@require_http_methods(["POST"])
def scheduled_delete(request, pk):
    """Delete scheduled report"""
    scheduled = get_object_or_404(ScheduledReport, pk=pk)
    
    if scheduled.created_by != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    scheduled.delete()
    messages.success(request, "Scheduled report deleted successfully.")
    return redirect('reports:scheduled_list')


# Favorites
@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, template_id):
    """Toggle report template as favorite"""
    template = get_object_or_404(ReportTemplate, pk=template_id)
    
    favorite, created = ReportFavorite.objects.get_or_create(
        user=request.user,
        template=template
    )
    
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'is_favorite': False})
    
    return JsonResponse({'status': 'added', 'is_favorite': True})


@login_required
def favorites_list(request):
    """List favorite reports"""
    favorites = ReportFavorite.objects.filter(user=request.user).select_related('template')
    
    context = {'favorites': favorites}
    return render(request, 'reports/favorites.html', context)


# API-style endpoints
@login_required
def template_categories(request):
    """Get report templates by category (JSON)"""
    categories = ReportTemplate.objects.for_user(request.user).values('category').annotate(
        count=Count('id')
    )
    
    return JsonResponse({'categories': list(categories)})


@login_required
def report_stats(request):
    """Get report statistics (JSON)"""
    stats = {
        'total_templates': ReportTemplate.objects.for_user(request.user).count(),
        'generated_today': GeneratedReport.objects.filter(
            generated_by=request.user,
            generated_at__date=timezone.now().date()
        ).count(),
        'favorites': ReportFavorite.objects.filter(user=request.user).count(),
        'scheduled': ScheduledReport.objects.filter(created_by=request.user, is_active=True).count(),
    }
    
    return JsonResponse({'stats': stats})
