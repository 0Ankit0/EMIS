"""
Analytics Views - Dashboard and Reporting
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Avg, Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import json

from .models import DashboardMetric, Report, AnalyticsQuery
from .forms import ReportForm, AnalyticsQueryForm
from .services.dashboard_service import DashboardService
from .services.admissions_metrics_service import AdmissionsMetricsService
from .services.attendance_metrics_service import AttendanceMetricsService
from .services.fee_metrics_service import FeeMetricsService
from .services.course_metrics_service import CourseMetricsService


# ============================================================================
# Dashboard Views
# ============================================================================

@login_required
def dashboard(request):
    """
    Main analytics dashboard with all metrics
    """
    # Get time period from request
    period = request.GET.get('period', '30')  # days
    try:
        days = int(period)
    except ValueError:
        days = 30
    
    start_date = timezone.now() - timedelta(days=days)
    
    # Get dashboard summary
    try:
        summary = DashboardService.get_dashboard_summary()
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        summary = {}
    
    # Get recent reports
    recent_reports = Report.objects.filter(
        generated_by=request.user
    ).order_by('-created_at')[:5]
    
    # Get featured queries
    featured_queries = AnalyticsQuery.objects.filter(
        is_featured=True
    ).order_by('-usage_count')[:5]
    
    context = {
        'summary': summary,
        'recent_reports': recent_reports,
        'featured_queries': featured_queries,
        'selected_period': days,
    }
    
    return render(request, 'analytics/dashboard.html', context)


@login_required
def admissions_analytics(request):
    """Detailed admissions analytics"""
    metrics = AdmissionsMetricsService.calculate_funnel()
    program_stats = AdmissionsMetricsService.get_program_statistics()
    timeline = AdmissionsMetricsService.get_application_timeline()
    
    context = {
        'metrics': metrics,
        'program_stats': program_stats,
        'timeline': timeline,
    }
    
    return render(request, 'analytics/admissions_analytics.html', context)


@login_required
def attendance_analytics(request):
    """Detailed attendance analytics"""
    metrics = AttendanceMetricsService.calculate_rates()
    by_program = AttendanceMetricsService.get_by_program()
    trends = AttendanceMetricsService.get_trends()
    
    context = {
        'metrics': metrics,
        'by_program': by_program,
        'trends': trends,
    }
    
    return render(request, 'analytics/attendance_analytics.html', context)


@login_required
def financial_analytics(request):
    """Detailed financial analytics"""
    metrics = FeeMetricsService.calculate_collection()
    by_program = FeeMetricsService.get_by_program()
    outstanding = FeeMetricsService.get_outstanding_fees()
    
    context = {
        'metrics': metrics,
        'by_program': by_program,
        'outstanding': outstanding,
    }
    
    return render(request, 'analytics/financial_analytics.html', context)


@login_required
def academic_analytics(request):
    """Detailed academic performance analytics"""
    metrics = CourseMetricsService.calculate_completion()
    by_program = CourseMetricsService.get_by_program()
    grade_distribution = CourseMetricsService.get_grade_distribution()
    
    context = {
        'metrics': metrics,
        'by_program': by_program,
        'grade_distribution': grade_distribution,
    }
    
    return render(request, 'analytics/academic_analytics.html', context)


# ============================================================================
# Report Management
# ============================================================================

@login_required
def report_list(request):
    """List all reports"""
    reports = Report.objects.filter(
        Q(generated_by=request.user) | Q(shared_with=request.user)
    ).distinct().order_by('-created_at')
    
    # Filter by type
    report_type = request.GET.get('type')
    if report_type:
        reports = reports.filter(report_type=report_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        reports = reports.filter(status=status)
    
    # Pagination
    paginator = Paginator(reports, 20)
    page = request.GET.get('page')
    reports_page = paginator.get_page(page)
    
    context = {
        'reports': reports_page,
        'report_types': Report.REPORT_TYPES,
    }
    
    return render(request, 'analytics/report_list.html', context)


@login_required
def report_detail(request, pk):
    """View report details"""
    report = get_object_or_404(Report, pk=pk)
    
    # Check permissions
    if report.generated_by != request.user and request.user not in report.shared_with.all():
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to view this report.')
            return redirect('analytics:report_list')
    
    context = {
        'report': report,
    }
    
    return render(request, 'analytics/report_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def report_create(request):
    """Create new report"""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    report = form.save(commit=False)
                    report.generated_by = request.user
                    report.status = 'pending'
                    report.save()
                    
                    # Trigger report generation (can be async with Celery)
                    # generate_report_task.delay(report.id)
                    
                    messages.success(request, 'Report generation started!')
                    return redirect('analytics:report_detail', pk=report.pk)
                    
            except Exception as e:
                messages.error(request, f'Error creating report: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'analytics/report_form.html', context)


@login_required
@require_http_methods(["POST"])
def report_delete(request, pk):
    """Delete a report"""
    report = get_object_or_404(Report, pk=pk)
    
    # Check permissions
    if report.generated_by != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        report.delete()
        messages.success(request, 'Report deleted successfully!')
        return redirect('analytics:report_list')
    except Exception as e:
        messages.error(request, f'Error deleting report: {str(e)}')
        return redirect('analytics:report_detail', pk=pk)


@login_required
def report_download(request, pk):
    """Download report file"""
    report = get_object_or_404(Report, pk=pk)
    
    # Check permissions
    if report.generated_by != request.user and request.user not in report.shared_with.all():
        if not request.user.is_staff:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if not report.file_path:
        messages.error(request, 'Report file not available.')
        return redirect('analytics:report_detail', pk=pk)
    
    # Serve file
    response = HttpResponse(report.file_path.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{report.title}.{report.format}"'
    return response


# ============================================================================
# Analytics Queries
# ============================================================================

@login_required
def query_list(request):
    """List saved analytics queries"""
    queries = AnalyticsQuery.objects.filter(
        Q(created_by=request.user) | Q(is_public=True)
    ).order_by('-last_used_at')
    
    paginator = Paginator(queries, 20)
    page = request.GET.get('page')
    queries_page = paginator.get_page(page)
    
    context = {
        'queries': queries_page,
    }
    
    return render(request, 'analytics/query_list.html', context)


@login_required
def query_detail(request, pk):
    """View and execute analytics query"""
    query = get_object_or_404(AnalyticsQuery, pk=pk)
    
    # Update usage stats
    query.usage_count += 1
    query.last_used_at = timezone.now()
    query.save(update_fields=['usage_count', 'last_used_at'])
    
    # Execute query (simplified - implement based on query_config)
    results = {}
    
    context = {
        'query': query,
        'results': results,
    }
    
    return render(request, 'analytics/query_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def query_create(request):
    """Create new analytics query"""
    if request.method == 'POST':
        form = AnalyticsQueryForm(request.POST)
        
        if form.is_valid():
            try:
                query = form.save(commit=False)
                query.created_by = request.user
                query.save()
                
                messages.success(request, 'Query created successfully!')
                return redirect('analytics:query_detail', pk=query.pk)
                
            except Exception as e:
                messages.error(request, f'Error creating query: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AnalyticsQueryForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'analytics/query_form.html', context)


# ============================================================================
# API Endpoints for Charts and Real-time Data
# ============================================================================

@login_required
def api_dashboard_summary(request):
    """API endpoint for dashboard summary"""
    try:
        summary = DashboardService.get_dashboard_summary()
        return JsonResponse(summary)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def api_refresh_metrics(request):
    """API endpoint to refresh all metrics"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        summary = DashboardService.refresh_metrics()
        return JsonResponse({
            'success': True,
            'message': 'Metrics refreshed successfully',
            'data': summary
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def api_chart_data(request):
    """API endpoint for chart data"""
    chart_type = request.GET.get('type')
    period = request.GET.get('period', '30')
    
    try:
        days = int(period)
    except ValueError:
        days = 30
    
    data = {}
    
    if chart_type == 'admissions_funnel':
        data = AdmissionsMetricsService.calculate_funnel()
    elif chart_type == 'attendance_trends':
        data = AttendanceMetricsService.get_trends()
    elif chart_type == 'fee_collection':
        data = FeeMetricsService.calculate_collection()
    elif chart_type == 'course_completion':
        data = CourseMetricsService.calculate_completion()
    
    return JsonResponse(data)
