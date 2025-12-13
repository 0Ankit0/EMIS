"""Inventory App Tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta

from apps.inventory.models import Category, Location, Item, Stock, PurchaseOrder, Asset
from apps.inventory.utils import get_total_stock, check_reorder_required

User = get_user_model()


class CategoryTestCase(TestCase):
    """Test Category model"""
    
    def test_category_creation(self):
        category = Category.objects.create(
            name='Electronics',
            code='ELEC'
        )
        self.assertEqual(str(category), 'ELEC - Electronics')


class ItemTestCase(TestCase):
    """Test Item model"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Stationery', code='STAT')
        
        self.item = Item.objects.create(
            name='A4 Paper',
            code='STAT-001',
            item_type='consumable',
            category=self.category,
            unit='box',
            minimum_stock=10,
            reorder_level=15,
            unit_price=Decimal('250.00')
        )
    
    def test_item_creation(self):
        self.assertEqual(str(self.item), 'STAT-001 - A4 Paper')
    
    def test_reorder_check(self):
        # No stock yet
        self.assertTrue(check_reorder_required(self.item))


class StockTestCase(TestCase):
    """Test Stock model"""
    
    def setUp(self):
        category = Category.objects.create(name='Test', code='TST')
        self.item = Item.objects.create(
            name='Test Item',
            code='TST-001',
            item_type='consumable',
            category=category,
            unit='pcs',
            unit_price=Decimal('100')
        )
        
        self.location = Location.objects.create(
            name='Main Store',
            code='MS-01',
            location_type='warehouse'
        )
        
        self.stock = Stock.objects.create(
            item=self.item,
            location=self.location,
            quantity=100,
            reserved_quantity=20
        )
    
    def test_available_quantity(self):
        self.assertEqual(self.stock.available_quantity, 80)
    
    def test_total_stock(self):
        total = get_total_stock(self.item)
        self.assertEqual(total, 100)


class PurchaseOrderTestCase(TestCase):
    """Test PurchaseOrder model"""
    
    def test_po_number_generation(self):
        from apps.inventory.models import Supplier
        
        supplier = Supplier.objects.create(
            name='Test Supplier',
            code='SUP-001',
            supplier_type='distributor',
            contact_person='John Doe',
            email='john@supplier.com',
            phone='+919876543210',
            address='Test Address',
            city='Mumbai',
            state='Maharashtra',
            pincode='400001'
        )
        
        po = PurchaseOrder.objects.create(
            supplier=supplier,
            subtotal=Decimal('10000'),
            tax_amount=Decimal('1800')
        )
        
        self.assertTrue(po.po_number.startswith('PO-'))
        self.assertEqual(po.total_amount, Decimal('11800'))


class AssetTestCase(TestCase):
    """Test Asset model"""
    
    def test_asset_creation(self):
        category = Category.objects.create(name='Equipment', code='EQP')
        item = Item.objects.create(
            name='Laptop',
            code='EQP-001',
            item_type='asset',
            category=category,
            unit='pcs',
            unit_price=Decimal('50000')
        )
        
        location = Location.objects.create(
            name='IT Department',
            code='IT-01',
            location_type='department'
        )
        
        asset = Asset.objects.create(
            item=item,
            location=location,
            serial_number='SN123456',
            purchase_date=date.today(),
            purchase_price=Decimal('50000'),
            current_value=Decimal('50000')
        )
        
        self.assertTrue(asset.asset_number.startswith('AST-') or len(asset.asset_number) > 0)
