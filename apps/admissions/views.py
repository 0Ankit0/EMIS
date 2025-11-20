"""
Admissions Views - Complete CRUD Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Application, MeritList
from .forms import ApplicationForm, MeritListForm
from .filters import ApplicationFilter
from .utils import generate_admissions_report, export_admissions_to_csv


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """
    Admissions dashboard with statistics and overview
    """
    # Get statistics
    total_applications = Application.objects.count()
    submitted_applications = Application.objects.filter(status='submitted').count()
    approved_applications = Application.objects.filter(status='approved').count()
    pending_applications = Application.objects.filter(status__in=['under_review', 'documents_pending']).count()
    rejected_applications = Application.objects.filter(status='rejected').count()
    
    # Recent applications
    recent_applications = Application.objects.all()[:10]
    
    # Status breakdown
    status_breakdown = Application.objects.values('status').annotate(count=Count('id'))
    
    # Merit lists
    merit_lists = MeritList.objects.filter(is_published=True)[:5]
    
    context = {
        'total_applications': total_applications,
        'submitted_applications': submitted_applications,
        'approved_applications': approved_applications,
        'pending_applications': pending_applications,
        'rejected_applications': rejected_applications,
        'recent_applications': recent_applications,
        'status_breakdown': status_breakdown,
        'merit_lists': merit_lists,
    }
    
    return render(request, 'admissions/dashboard.html', context)


# ============================================================================
# List View (Read - All)
# ============================================================================

@login_required
def application_list(request):
    """
    List all applications with filtering, search, and pagination
    """
    # Get all applications
    applications = Application.objects.all()
    
    # Apply filters using django-filter
    filter_instance = ApplicationFilter(request.GET, queryset=applications)
    applications = filter_instance.qs
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(
            Q(application_number__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(program__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-submitted_at')
    applications = applications.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(applications, 20)  # Show 20 applications per page
    page = request.GET.get('page')
    
    try:
        applications_page = paginator.page(page)
    except PageNotAnInteger:
        applications_page = paginator.page(1)
    except EmptyPage:
        applications_page = paginator.page(paginator.num_pages)
    
    context = {
        'applications': applications_page,
        'filter': filter_instance,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'admissions/application_list.html', context)


# ============================================================================
# Detail View (Read - Single)
# ============================================================================

@login_required
def application_detail(request, pk):
    """
    View single application details
    """
    application = get_object_or_404(Application, pk=pk)
    
    context = {
        'application': application,
    }
    
    return render(request, 'admissions/application_detail.html', context)


# ============================================================================
# Create View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def application_create(request):
    """
    Create new application
    """
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    application = form.save(commit=False)
                    # Set submitted timestamp if status is submitted
                    if application.status == 'submitted' and not application.submitted_at:
                        application.submitted_at = timezone.now()
                    application.save()
                    
                    messages.success(request, f'Application {application.application_number} created successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_add'):
                        return redirect('admissions:application_create')
                    elif request.POST.get('save_and_continue'):
                        return redirect('admissions:application_update', pk=application.pk)
                    else:
                        return redirect('admissions:application_detail', pk=application.pk)
                        
            except Exception as e:
                messages.error(request, f'Error creating application: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplicationForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'admissions/application_form.html', context)


# ============================================================================
# Update View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def application_update(request, pk):
    """
    Update existing application
    """
    application = get_object_or_404(Application, pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_application = form.save(commit=False)
                    # Set submitted timestamp if status changed to submitted
                    if updated_application.status == 'submitted' and not updated_application.submitted_at:
                        updated_application.submitted_at = timezone.now()
                    updated_application.save()
                    
                    messages.success(request, f'Application {updated_application.application_number} updated successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_continue'):
                        return redirect('admissions:application_update', pk=updated_application.pk)
                    else:
                        return redirect('admissions:application_detail', pk=updated_application.pk)
                        
            except Exception as e:
                messages.error(request, f'Error updating application: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplicationForm(instance=application)
    
    context = {
        'form': form,
        'application': application,
        'action': 'Update',
    }
    
    return render(request, 'admissions/application_form.html', context)


# ============================================================================
# Delete View
# ============================================================================

@login_required
@require_http_methods(["POST"])
def application_delete(request, pk):
    """
    Delete application
    """
    application = get_object_or_404(Application, pk=pk)
    
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete applications.')
        return redirect('admissions:application_detail', pk=pk)
    
    try:
        app_number = application.application_number
        application.delete()
        messages.success(request, f'Application {app_number} deleted successfully!')
        return redirect('admissions:application_list')
    except Exception as e:
        messages.error(request, f'Error deleting application: {str(e)}')
        return redirect('admissions:application_detail', pk=pk)


# ============================================================================
# Bulk Operations
# ============================================================================

@login_required
@require_http_methods(["POST"])
def bulk_delete(request):
    """
    Delete multiple applications at once
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    app_ids = request.POST.getlist('app_ids[]')
    
    try:
        deleted_count = Application.objects.filter(id__in=app_ids).delete()[0]
        return JsonResponse({
            'success': True,
            'message': f'{deleted_count} applications deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def bulk_update_status(request):
    """
    Update status for multiple applications
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    app_ids = request.POST.getlist('app_ids[]')
    status = request.POST.get('status')
    
    try:
        updated_count = Application.objects.filter(id__in=app_ids).update(status=status)
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} applications updated successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_csv(request):
    """
    Export applications to CSV
    """
    applications = Application.objects.all()
    
    # Generate CSV
    csv_data = export_admissions_to_csv(applications)
    
    # Create response
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="applications_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    return response


@login_required
def export_pdf(request):
    """
    Export applications to PDF
    """
    applications = Application.objects.all()[:100]
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, 'Admissions Applications Report')
    
    # Date
    p.setFont("Helvetica", 10)
    p.drawString(100, 730, f'Generated: {timezone.now().strftime("%Y-%m-%d %H:%M")}')
    
    # Applications
    y = 700
    p.setFont("Helvetica", 10)
    
    for app in applications:
        text = f'{app.application_number} - {app.first_name} {app.last_name} - {app.status}'
        p.drawString(100, y, text)
        y -= 20
        
        if y < 100:
            p.showPage()
            y = 750
    
    p.save()
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="applications_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    return response


# ============================================================================
# AJAX/API Operations
# ============================================================================

@login_required
def get_application_data(request, pk):
    """
    Get application data as JSON (for AJAX requests)
    """
    application = get_object_or_404(Application, pk=pk)
    
    data = {
        'id': str(application.id),
        'application_number': application.application_number,
        'first_name': application.first_name,
        'last_name': application.last_name,
        'email': application.email,
        'phone': application.phone,
        'program': application.program,
        'status': application.status,
        'submitted_at': application.submitted_at.isoformat() if application.submitted_at else None,
        'created_at': application.created_at.isoformat(),
        'updated_at': application.updated_at.isoformat(),
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def toggle_status(request, pk):
    """
    Toggle application status
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    application = get_object_or_404(Application, pk=pk)
    
    try:
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            
            return JsonResponse({
                'success': True,
                'status': application.status,
                'message': f'Status changed to {application.get_status_display()}'
            })
        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Statistics and Reports
# ============================================================================

@login_required
def statistics(request):
    """
    View statistics and reports
    """
    applications = Application.objects.all()
    
    # Generate report
    report_data = generate_admissions_report(applications)
    
    # Additional statistics
    stats = {
        'total': applications.count(),
        'by_status': {},
        'by_program': applications.values('program').annotate(count=Count('id')),
        'by_year': applications.values('admission_year').annotate(count=Count('id')),
        'recent_activity': applications.order_by('-updated_at')[:10],
    }
    
    # Count by status
    for status_code, status_name in Application.STATUS_CHOICES:
        stats['by_status'][status_name] = applications.filter(status=status_code).count()
    
    context = {
        'report_data': report_data,
        'stats': stats,
    }
    
    return render(request, 'admissions/statistics.html', context)


@login_required
def search(request):
    """
    Advanced search functionality
    """
    query = request.GET.get('q', '')
    
    applications = Application.objects.all()
    
    if query:
        applications = applications.filter(
            Q(application_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(program__icontains=query)
        )
    
    # Apply additional filters from request
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    program_filter = request.GET.get('program')
    if program_filter:
        applications = applications.filter(program=program_filter)
    
    year_filter = request.GET.get('year')
    if year_filter:
        applications = applications.filter(admission_year=year_filter)
    
    date_from = request.GET.get('date_from')
    if date_from:
        applications = applications.filter(submitted_at__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        applications = applications.filter(submitted_at__lte=date_to)
    
    context = {
        'applications': applications,
        'query': query,
    }
    
    return render(request, 'admissions/search_results.html', context)


# ============================================================================
# Merit List Views
# ============================================================================

@login_required
def merit_list_list(request):
    """List all merit lists"""
    merit_lists = MeritList.objects.all()
    
    # Filter by program
    program = request.GET.get('program')
    if program:
        merit_lists = merit_lists.filter(program=program)
    
    # Filter by year
    year = request.GET.get('year')
    if year:
        merit_lists = merit_lists.filter(admission_year=year)
    
    # Filter published/unpublished
    is_published = request.GET.get('published')
    if is_published == 'true':
        merit_lists = merit_lists.filter(is_published=True)
    elif is_published == 'false':
        merit_lists = merit_lists.filter(is_published=False)
    
    paginator = Paginator(merit_lists, 20)
    page = request.GET.get('page')
    merit_lists_page = paginator.get_page(page)
    
    context = {
        'merit_lists': merit_lists_page,
    }
    
    return render(request, 'admissions/merit_list_list.html', context)


@login_required
def merit_list_detail(request, pk):
    """View merit list details"""
    merit_list = get_object_or_404(MeritList, pk=pk)
    
    # Get ranked applications
    ranked_app_ids = merit_list.ranked_applications
    applications = Application.objects.filter(id__in=ranked_app_ids)
    
    # Sort applications by rank
    applications_dict = {str(app.id): app for app in applications}
    ranked_applications = [applications_dict.get(str(app_id)) for app_id in ranked_app_ids if str(app_id) in applications_dict]
    
    context = {
        'merit_list': merit_list,
        'ranked_applications': ranked_applications,
    }
    
    return render(request, 'admissions/merit_list_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def merit_list_create(request):
    """Create new merit list"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create merit lists.')
        return redirect('admissions:merit_list_list')
    
    if request.method == 'POST':
        form = MeritListForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    merit_list = form.save(commit=False)
                    merit_list.generated_by = request.user
                    
                    # Get applications for this program/year
                    applications = Application.objects.filter(
                        program=merit_list.program,
                        admission_year=merit_list.admission_year,
                        admission_semester=merit_list.admission_semester,
                        status__in=['submitted', 'under_review', 'approved']
                    ).order_by('-merit_score', 'submitted_at')
                    
                    # Rank applications
                    ranked_ids = []
                    for rank, app in enumerate(applications, 1):
                        app.rank = rank
                        app.save(update_fields=['rank'])
                        ranked_ids.append(str(app.id))
                    
                    merit_list.ranked_applications = ranked_ids
                    merit_list.total_applications = len(ranked_ids)
                    merit_list.save()
                    
                    messages.success(request, f'Merit list "{merit_list.name}" created successfully!')
                    return redirect('admissions:merit_list_detail', pk=merit_list.pk)
                    
            except Exception as e:
                messages.error(request, f'Error creating merit list: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MeritListForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'admissions/merit_list_form.html', context)


@login_required
@require_http_methods(["POST"])
def merit_list_publish(request, pk):
    """Publish merit list"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    merit_list = get_object_or_404(MeritList, pk=pk)
    
    try:
        merit_list.is_published = True
        merit_list.published_at = timezone.now()
        merit_list.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Merit list published successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
