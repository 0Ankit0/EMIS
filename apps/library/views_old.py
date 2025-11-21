"""
Library Views - Complete CRUD Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import LibraryItem
from .forms import LibraryItemForm
from .filters import LibraryItemFilter
from .utils import generate_library_report, export_library_to_csv


# ============================================================================
# Dashboard View
# ============================================================================

@login_required
def dashboard(request):
    """
    Library dashboard with statistics and overview
    """
    # Get statistics
    total_items = LibraryItem.objects.count()
    active_items = LibraryItem.objects.active().count()
    inactive_items = LibraryItem.objects.inactive().count()
    pending_items = LibraryItem.objects.pending().count()
    
    # Recent items
    recent_items = LibraryItem.objects.all()[:5]
    
    # User's items if not admin
    if not request.user.is_staff:
        user_items = LibraryItem.objects.filter(created_by=request.user)
    else:
        user_items = None
    
    context = {
        'total_items': total_items,
        'active_items': active_items,
        'inactive_items': inactive_items,
        'pending_items': pending_items,
        'recent_items': recent_items,
        'user_items': user_items,
    }
    
    return render(request, 'library/dashboard.html', context)


# ============================================================================
# List View (Read - All)
# ============================================================================

@login_required
def item_list(request):
    """
    List all items with filtering, search, and pagination
    """
    # Get all items
    items = LibraryItem.objects.all()
    
    # Apply filters if user is not admin
    if not request.user.is_staff:
        items = items.filter(created_by=request.user)
    
    # Apply filters using django-filter
    filter_instance = LibraryItemFilter(request.GET, queryset=items)
    items = filter_instance.qs
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    items = items.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(items, 20)  # Show 20 items per page
    page = request.GET.get('page')
    
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    
    context = {
        'items': items_page,
        'filter': filter_instance,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'library/item_list.html', context)


# ============================================================================
# Detail View (Read - Single)
# ============================================================================

@login_required
def item_detail(request, pk):
    """
    View single item details
    """
    item = get_object_or_404(LibraryItem, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        messages.error(request, 'You do not have permission to view this item.')
        return redirect('library:list')
    
    context = {
        'item': item,
    }
    
    return render(request, 'library/item_detail.html', context)


# ============================================================================
# Create View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def item_create(request):
    """
    Create new item
    """
    if request.method == 'POST':
        form = LibraryItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    item = form.save(commit=False)
                    item.created_by = request.user
                    item.save()
                    
                    messages.success(request, f'{item.name} created successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_add'):
                        return redirect('library:create')
                    elif request.POST.get('save_and_continue'):
                        return redirect('library:update', pk=item.pk)
                    else:
                        return redirect('library:detail', pk=item.pk)
                        
            except Exception as e:
                messages.error(request, f'Error creating item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LibraryItemForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'library/item_form.html', context)


# ============================================================================
# Update View
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def item_update(request, pk):
    """
    Update existing item
    """
    item = get_object_or_404(LibraryItem, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('library:detail', pk=pk)
    
    if request.method == 'POST':
        form = LibraryItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_item = form.save()
                    
                    messages.success(request, f'{updated_item.name} updated successfully!')
                    
                    # Redirect based on user choice
                    if request.POST.get('save_and_continue'):
                        return redirect('library:update', pk=updated_item.pk)
                    else:
                        return redirect('library:detail', pk=updated_item.pk)
                        
            except Exception as e:
                messages.error(request, f'Error updating item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LibraryItemForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'action': 'Update',
    }
    
    return render(request, 'library/item_form.html', context)


# ============================================================================
# Delete View
# ============================================================================

@login_required
@require_http_methods(["POST"])
def item_delete(request, pk):
    """
    Delete item (soft or hard delete)
    """
    item = get_object_or_404(LibraryItem, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('library:detail', pk=pk)
    
    try:
        item_name = item.name
        item.delete()
        messages.success(request, f'{item_name} deleted successfully!')
        return redirect('library:list')
    except Exception as e:
        messages.error(request, f'Error deleting item: {str(e)}')
        return redirect('library:detail', pk=pk)


# ============================================================================
# Bulk Operations
# ============================================================================

@login_required
@require_http_methods(["POST"])
def bulk_delete(request):
    """
    Delete multiple items at once
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    item_ids = request.POST.getlist('item_ids[]')
    
    try:
        deleted_count = LibraryItem.objects.filter(id__in=item_ids).delete()[0]
        return JsonResponse({
            'success': True,
            'message': f'{deleted_count} items deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def bulk_update_status(request):
    """
    Update status for multiple items
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    item_ids = request.POST.getlist('item_ids[]')
    status = request.POST.get('status')
    
    try:
        updated_count = LibraryItem.objects.filter(id__in=item_ids).update(status=status)
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} items updated successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_csv(request):
    """
    Export items to CSV
    """
    items = LibraryItem.objects.all()
    
    # Apply user filter if not admin
    if not request.user.is_staff:
        items = items.filter(created_by=request.user)
    
    # Generate CSV
    csv_data = export_library_to_csv(items)
    
    # Create response
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="library_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    return response


@login_required
def export_pdf(request):
    """
    Export items to PDF
    """
    items = LibraryItem.objects.all()
    
    # Apply user filter if not admin
    if not request.user.is_staff:
        items = items.filter(created_by=request.user)
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f'Library Report')
    
    # Date
    p.setFont("Helvetica", 10)
    p.drawString(100, 730, f'Generated: {timezone.now().strftime("%Y-%m-%d %H:%M")}')
    
    # Items
    y = 700
    p.setFont("Helvetica", 12)
    
    for item in items[:50]:  # Limit to 50 items for simple PDF
        p.drawString(100, y, f'{item.name} - {item.status}')
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
    response['Content-Disposition'] = f'attachment; filename="library_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    return response


# ============================================================================
# AJAX/API Operations
# ============================================================================

@login_required
def get_item_data(request, pk):
    """
    Get item data as JSON (for AJAX requests)
    """
    item = get_object_or_404(LibraryItem, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    data = {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'status': item.status,
        'created_at': item.created_at.isoformat(),
        'updated_at': item.updated_at.isoformat(),
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def toggle_status(request, pk):
    """
    Toggle item status (active/inactive)
    """
    item = get_object_or_404(LibraryItem, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and item.created_by != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        if item.status == 'active':
            item.status = 'inactive'
        else:
            item.status = 'active'
        
        item.save()
        
        return JsonResponse({
            'success': True,
            'status': item.status,
            'message': f'Status changed to {item.status}'
        })
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
    items = LibraryItem.objects.all()
    
    # Apply user filter if not admin
    if not request.user.is_staff:
        items = items.filter(created_by=request.user)
    
    # Generate report
    report_data = generate_library_report(items)
    
    # Additional statistics
    stats = {
        'total': items.count(),
        'by_status': {
            'active': items.filter(status='active').count(),
            'inactive': items.filter(status='inactive').count(),
            'pending': items.filter(status='pending').count(),
        },
        'by_month': {
            # Add monthly statistics
        },
        'recent_activity': items.order_by('-updated_at')[:10],
    }
    
    context = {
        'report_data': report_data,
        'stats': stats,
    }
    
    return render(request, 'library/statistics.html', context)


# ============================================================================
# Search and Filter
# ============================================================================

@login_required
def search(request):
    """
    Advanced search functionality
    """
    query = request.GET.get('q', '')
    
    items = LibraryItem.objects.all()
    
    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Apply additional filters from request
    status_filter = request.GET.get('status')
    if status_filter:
        items = items.filter(status=status_filter)
    
    date_from = request.GET.get('date_from')
    if date_from:
        items = items.filter(created_at__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        items = items.filter(created_at__lte=date_to)
    
    context = {
        'items': items,
        'query': query,
    }
    
    return render(request, 'library/search_results.html', context)
