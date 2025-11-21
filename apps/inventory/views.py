"""Inventory Views"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.utils import timezone
import csv

from .models import *


@login_required
def dashboard(request):
    """Inventory dashboard"""
    stats = {
        'total_items': Item.objects.active().count(),
        'low_stock_items': Item.objects.low_stock().count(),
        'total_assets': Asset.objects.count(),
        'pending_pos': PurchaseOrder.objects.pending().count(),
        'pending_requisitions': Requisition.objects.pending().count(),
    }
    
    low_stock_items = Item.objects.low_stock()[:10]
    recent_transactions = StockTransaction.objects.all()[:10]
    
    return render(request, 'inventory/dashboard.html', {
        'stats': stats,
        'low_stock_items': low_stock_items,
        'recent_transactions': recent_transactions,
    })


@login_required
def item_list(request):
    """List all items"""
    items = Item.objects.active()
    return render(request, 'inventory/item_list.html', {'items': items})


@login_required
def stock_report(request):
    """Stock report"""
    stocks = Stock.objects.select_related('item', 'location').all()
    return render(request, 'inventory/stock_report.html', {'stocks': stocks})


@login_required
def purchase_order_list(request):
    """Purchase orders list"""
    pos = PurchaseOrder.objects.all()
    return render(request, 'inventory/po_list.html', {'purchase_orders': pos})


@login_required
def asset_list(request):
    """Assets list"""
    assets = Asset.objects.all()
    return render(request, 'inventory/asset_list.html', {'assets': assets})


@login_required
def requisition_list(request):
    """Requisitions list"""
    requisitions = Requisition.objects.all()
    return render(request, 'inventory/requisition_list.html', {'requisitions': requisitions})


@login_required
def export_stock_csv(request):
    """Export stock to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Item Code', 'Item Name', 'Location', 'Quantity', 'Unit'])
    
    for stock in Stock.objects.select_related('item', 'location').all():
        writer.writerow([
            stock.item.code,
            stock.item.name,
            stock.location.name,
            stock.quantity,
            stock.item.unit
        ])
    
    return response
