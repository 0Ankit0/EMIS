"""Inventory Utility Functions"""
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from decimal import Decimal
import csv
from io import StringIO


def get_total_stock(item):
    """Get total stock across all locations for an item"""
    from .models import Stock
    return Stock.objects.filter(item=item).aggregate(
        total=Sum('quantity')
    )['total'] or 0


def get_available_stock(item, location=None):
    """Get available stock (quantity - reserved) for an item"""
    from .models import Stock
    
    stocks = Stock.objects.filter(item=item)
    if location:
        stocks = stocks.filter(location=location)
    
    return stocks.aggregate(
        available=Sum(F('quantity') - F('reserved_quantity'))
    )['available'] or 0


def check_reorder_required(item):
    """Check if item needs reordering"""
    total_stock = get_total_stock(item)
    return total_stock <= item.reorder_level


def get_low_stock_items():
    """Get all items below reorder level"""
    from .models import Item, Stock
    
    low_stock_items = []
    for item in Item.objects.active():
        if check_reorder_required(item):
            low_stock_items.append({
                'item': item,
                'current_stock': get_total_stock(item),
                'reorder_level': item.reorder_level
            })
    
    return low_stock_items


def calculate_asset_depreciation(asset):
    """Calculate current asset value after depreciation"""
    from datetime import date
    
    years_since_purchase = (date.today() - asset.purchase_date).days / 365.25
    
    if asset.depreciation_rate > 0:
        # Straight-line depreciation
        annual_depreciation = asset.purchase_price * (asset.depreciation_rate / 100)
        total_depreciation = annual_depreciation * years_since_purchase
        current_value = max(0, asset.purchase_price - total_depreciation)
        return round(current_value, 2)
    
    return asset.purchase_price


def generate_stock_report(location=None, category=None):
    """Generate comprehensive stock report"""
    from .models import Stock, Item
    
    stocks = Stock.objects.select_related('item', 'location').all()
    
    if location:
        stocks = stocks.filter(location=location)
    
    if category:
        stocks = stocks.filter(item__category=category)
    
    report_data = []
    for stock in stocks:
        report_data.append({
            'item_code': stock.item.code,
            'item_name': stock.item.name,
            'category': stock.item.category.name,
            'location': stock.location.name,
            'quantity': stock.quantity,
            'reserved': stock.reserved_quantity,
            'available': stock.available_quantity,
            'unit': stock.item.unit,
            'unit_price': stock.item.unit_price,
            'total_value': stock.quantity * stock.item.unit_price
        })
    
    return report_data


def get_stock_valuation(location=None):
    """Calculate total stock valuation"""
    from .models import Stock
    
    stocks = Stock.objects.select_related('item').all()
    if location:
        stocks = stocks.filter(location=location)
    
    total_value = 0
    for stock in stocks:
        total_value += stock.quantity * stock.item.unit_price
    
    return total_value


def process_purchase_order_receipt(po, received_items):
    """Process PO receipt and update stock"""
    from .models import StockTransaction, PurchaseOrderItem
    
    for item_data in received_items:
        po_item = PurchaseOrderItem.objects.get(id=item_data['po_item_id'])
        received_qty = item_data['received_quantity']
        location = item_data['location']
        
        # Create stock transaction
        StockTransaction.objects.create(
            transaction_type='purchase',
            item=po_item.item,
            to_location=location,
            quantity=received_qty,
            reference_number=po.po_number
        )
        
        # Update PO item received quantity
        po_item.received_quantity += received_qty
        po_item.save()
    
    # Update PO status
    all_items = po.items.all()
    if all(item.received_quantity >= item.quantity for item in all_items):
        po.status = 'received'
    elif any(item.received_quantity > 0 for item in all_items):
        po.status = 'partially_received'
    
    po.save()


def process_requisition_fulfillment(requisition, issued_items):
    """Process requisition and issue stock"""
    from .models import StockTransaction, RequisitionItem
    
    for item_data in issued_items:
        req_item = RequisitionItem.objects.get(id=item_data['req_item_id'])
        issued_qty = item_data['issued_quantity']
        from_location = item_data['from_location']
        
        # Create stock transaction
        StockTransaction.objects.create(
            transaction_type='issue',
            item=req_item.item,
            from_location=from_location,
            quantity=issued_qty,
            reference_number=requisition.requisition_number
        )
        
        # Update requisition item issued quantity
        req_item.issued_quantity += issued_qty
        req_item.save()
    
    # Update requisition status
    all_items = requisition.items.all()
    if all(item.issued_quantity >= item.requested_quantity for item in all_items):
        requisition.status = 'fulfilled'
    elif any(item.issued_quantity > 0 for item in all_items):
        requisition.status = 'partially_fulfilled'
    
    requisition.save()


def export_stock_to_csv(queryset):
    """Export stock to CSV"""
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Item Code', 'Item Name', 'Category', 'Location', 
                     'Quantity', 'Reserved', 'Available', 'Unit', 'Value'])
    
    for stock in queryset:
        writer.writerow([
            stock.item.code,
            stock.item.name,
            stock.item.category.name,
            stock.location.name,
            stock.quantity,
            stock.reserved_quantity,
            stock.available_quantity,
            stock.item.unit,
            stock.quantity * stock.item.unit_price
        ])
    
    return output.getvalue()


def get_purchase_order_statistics(start_date=None, end_date=None):
    """Get purchase order statistics"""
    from .models import PurchaseOrder
    
    pos = PurchaseOrder.objects.all()
    
    if start_date:
        pos = pos.filter(order_date__gte=start_date)
    if end_date:
        pos = pos.filter(order_date__lte=end_date)
    
    return {
        'total_pos': pos.count(),
        'by_status': dict(pos.values('status').annotate(count=Count('id')).values_list('status', 'count')),
        'total_value': pos.aggregate(total=Sum('total_amount'))['total'] or 0,
        'pending_value': pos.filter(status__in=['pending', 'approved', 'ordered']).aggregate(
            total=Sum('total_amount'))['total'] or 0,
    }


def get_asset_statistics():
    """Get asset statistics"""
    from .models import Asset
    
    assets = Asset.objects.all()
    
    return {
        'total_assets': assets.count(),
        'by_status': dict(assets.values('status').annotate(count=Count('id')).values_list('status', 'count')),
        'total_value': assets.aggregate(total=Sum('current_value'))['total'] or 0,
        'in_use': assets.filter(status='in_use').count(),
        'available': assets.filter(status='available').count(),
        'under_maintenance': assets.filter(status__in=['maintenance', 'repair']).count(),
    }


def get_warranty_expiring_assets(days=30):
    """Get assets with warranty expiring soon"""
    from .models import Asset
    from datetime import timedelta
    
    future_date = timezone.now().date() + timedelta(days=days)
    
    return Asset.objects.filter(
        warranty_expiry_date__lte=future_date,
        warranty_expiry_date__gte=timezone.now().date()
    )
