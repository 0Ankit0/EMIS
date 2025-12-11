from .category import Category
from .location import Location
from .supplier import Supplier
from .item import Item
from .stock import Stock
from .purchase_order import PurchaseOrder
from .purchase_order_item import PurchaseOrderItem
from .stock_transaction import StockTransaction
from .asset import Asset
from .maintenance_record import MaintenanceRecord
from .requisition import Requisition
from .requisition_item import RequisitionItem

# Import and add managers
from ..managers import ItemManager, PurchaseOrderManager, AssetManager, RequisitionManager

Item.add_to_class('objects', ItemManager())
PurchaseOrder.add_to_class('objects', PurchaseOrderManager())
Asset.add_to_class('objects', AssetManager())
Requisition.add_to_class('objects', RequisitionManager())
