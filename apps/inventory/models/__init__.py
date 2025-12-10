"""Inventory Models - Comprehensive Asset & Inventory Management"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from decimal import Decimal

User = get_user_model()


class Category(TimeStampedModel):
    """Item Category"""
    
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_categories'
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Location(TimeStampedModel):
    """Storage Location"""
    
    LOCATION_TYPE_CHOICES = [
        ('warehouse', 'Warehouse'),
        ('store', 'Store Room'),
        ('department', 'Department'),
        ('lab', 'Laboratory'),
        ('office', 'Office'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    
    building = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    
    capacity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    in_charge = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_locations'
    )
    
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_locations'
        ordering = ['name']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Supplier(TimeStampedModel):
    """Supplier/Vendor Information"""
    
    SUPPLIER_TYPE_CHOICES = [
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('retailer', 'Retailer'),
        ('service_provider', 'Service Provider'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    supplier_type = models.CharField(max_length=30, choices=SUPPLIER_TYPE_CHOICES)
    
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    website = models.URLField(blank=True)
    
    # Tax & Legal
    gstin = models.CharField(max_length=15, blank=True, help_text="GST Identification Number")
    pan = models.CharField(max_length=10, blank=True)
    
    # Banking
    bank_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    
    # Credit terms
    credit_days = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    rating = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Supplier rating (1-5)"
    )
    
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_suppliers'
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Item(TimeStampedModel):
    """Inventory Item/Product"""
    
    ITEM_TYPE_CHOICES = [
        ('consumable', 'Consumable'),
        ('non_consumable', 'Non-Consumable'),
        ('asset', 'Asset'),
        ('equipment', 'Equipment'),
    ]
    
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('l', 'Liters'),
        ('ml', 'Milliliters'),
        ('m', 'Meters'),
        ('cm', 'Centimeters'),
        ('box', 'Box'),
        ('set', 'Set'),
        ('dozen', 'Dozen'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    
    description = models.TextField(blank=True)
    specifications = models.TextField(blank=True)
    
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    
    # Stock levels
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Pricing
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Additional info
    manufacturer = models.CharField(max_length=200, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    
    barcode = models.CharField(max_length=100, blank=True, unique=True, null=True)
    
    # Images and docs
    image = models.ImageField(upload_to='inventory/items/%Y/', blank=True, null=True)
    datasheet = models.FileField(upload_to='inventory/datasheets/%Y/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_items'
        ordering = ['name']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['category', 'item_type']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Stock(TimeStampedModel):
    """Stock/Inventory Levels per Location"""
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_records')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stock_items')
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    reserved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_stocks')
    
    class Meta:
        db_table = 'inventory_stock'
        unique_together = ['item', 'location']
        ordering = ['item', 'location']
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock Records'
        indexes = [
            models.Index(fields=['item', 'location']),
        ]
    
    def __str__(self):
        return f"{self.item.code} @ {self.location.code} - Qty: {self.quantity}"
    
    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity


class PurchaseOrder(TimeStampedModel):
    """Purchase Order"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('partially_received', 'Partially Received'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    po_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    
    order_date = models.DateField(default=timezone.now)
    expected_delivery_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    shipping_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    payment_terms = models.CharField(max_length=200, blank=True)
    delivery_address = models.TextField(blank=True)
    
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_pos')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_pos')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'inventory_purchase_orders'
        ordering = ['-order_date']
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        indexes = [
            models.Index(fields=['po_number']),
            models.Index(fields=['supplier', 'status']),
        ]
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate PO number if not set
        if not self.po_number:
            year = timezone.now().year
            from django.db.models import Count
            count = PurchaseOrder.objects.filter(created_at__year=year).count() + 1
            self.po_number = f"PO-{year}-{count:06d}"
        
        # Calculate total
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_charges - self.discount
        
        super().save(*args, **kwargs)


class PurchaseOrderItem(TimeStampedModel):
    """Purchase Order Line Items"""
    
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='po_items')
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_po_items'
        ordering = ['purchase_order', 'id']
        verbose_name = 'PO Item'
        verbose_name_plural = 'PO Items'
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.item.name}"
    
    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class StockTransaction(TimeStampedModel):
    """Stock Movement/Transaction"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('purchase', 'Purchase/Receipt'),
        ('issue', 'Issue/Consumption'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
        ('damage', 'Damage/Loss'),
    ]
    
    transaction_number = models.CharField(max_length=50, unique=True, db_index=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='transactions')
    
    from_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='outgoing_transactions'
    )
    to_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='incoming_transactions'
    )
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    reference_number = models.CharField(max_length=100, blank=True, help_text="PO/Invoice/Requisition number")
    
    transaction_date = models.DateTimeField(default=timezone.now)
    
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_transactions')
    
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_transactions'
        ordering = ['-transaction_date']
        verbose_name = 'Stock Transaction'
        verbose_name_plural = 'Stock Transactions'
        indexes = [
            models.Index(fields=['transaction_number']),
            models.Index(fields=['item', 'transaction_date']),
        ]
    
    def __str__(self):
        return f"{self.transaction_number} - {self.transaction_type}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_number:
            year = timezone.now().year
            from django.db.models import Count
            count = StockTransaction.objects.filter(created_at__year=year).count() + 1
            self.transaction_number = f"TXN-{year}-{count:06d}"
        super().save(*args, **kwargs)


class Asset(TimeStampedModel):
    """Fixed Asset Management"""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('repair', 'Under Repair'),
        ('retired', 'Retired'),
        ('disposed', 'Disposed'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    asset_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='assets')
    
    serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='assets')
    
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    
    current_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    depreciation_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Annual depreciation rate in percentage"
    )
    
    warranty_expiry_date = models.DateField(null=True, blank=True)
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_assets'
    )
    assigned_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_assets'
        ordering = ['asset_number']
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        indexes = [
            models.Index(fields=['asset_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.asset_number} - {self.item.name}"


class MaintenanceRecord(TimeStampedModel):
    """Asset Maintenance Record"""
    
    MAINTENANCE_TYPE_CHOICES = [
        ('preventive', 'Preventive Maintenance'),
        ('corrective', 'Corrective Maintenance'),
        ('repair', 'Repair'),
        ('calibration', 'Calibration'),
        ('inspection', 'Inspection'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE_CHOICES)
    
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    description = models.TextField()
    work_performed = models.TextField(blank=True)
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    vendor = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_jobs')
    
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='performed_maintenance')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    next_maintenance_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'inventory_maintenance'
        ordering = ['-scheduled_date']
        verbose_name = 'Maintenance Record'
        verbose_name_plural = 'Maintenance Records'
    
    def __str__(self):
        return f"{self.asset.asset_number} - {self.maintenance_type} ({self.scheduled_date})"


class Requisition(TimeStampedModel):
    """Stock/Item Requisition"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('partially_fulfilled', 'Partially Fulfilled'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]
    
    requisition_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    requested_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='requisitions')
    department = models.CharField(max_length=200)
    
    request_date = models.DateField(default=timezone.now)
    required_date = models.DateField()
    
    purpose = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requisitions')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_requisitions'
        ordering = ['-request_date']
        verbose_name = 'Requisition'
        verbose_name_plural = 'Requisitions'
        indexes = [
            models.Index(fields=['requisition_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.requisition_number} - {self.requested_by.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.requisition_number:
            year = timezone.now().year
            from django.db.models import Count
            count = Requisition.objects.filter(created_at__year=year).count() + 1
            self.requisition_number = f"REQ-{year}-{count:06d}"
        super().save(*args, **kwargs)


class RequisitionItem(TimeStampedModel):
    """Requisition Line Items"""
    
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='requisition_items')
    
    requested_quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    issued_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_requisition_items'
        ordering = ['requisition', 'id']
        verbose_name = 'Requisition Item'
        verbose_name_plural = 'Requisition Items'
    
    def __str__(self):
        return f"{self.requisition.requisition_number} - {self.item.name}"

# Import and add managers
from .managers import ItemManager, PurchaseOrderManager, AssetManager, RequisitionManager

Item.add_to_class('objects', ItemManager())
PurchaseOrder.add_to_class('objects', PurchaseOrderManager())
Asset.add_to_class('objects', AssetManager())
Requisition.add_to_class('objects', RequisitionManager())
