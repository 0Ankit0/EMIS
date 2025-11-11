"""
Inventory Service for EMIS
Manages inventory items, stock transactions, and purchase orders
"""
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func

from src.models.inventory import (
    InventoryItem, InventoryCategory, Vendor, PurchaseOrder, PurchaseOrderItem,
    StockTransaction, InventoryStatus, PurchaseOrderStatus, StockTransactionType
)
from src.lib.logging import get_logger

logger = get_logger(__name__)


class InventoryService:
    """Service for inventory management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ============ Inventory Items ============
    
    async def create_item(self, item_data: Dict[str, Any]) -> InventoryItem:
        """Create inventory item"""
        item = InventoryItem(**item_data)
        
        # Calculate total value
        if item.unit_cost and item.quantity:
            item.total_value = float(item.unit_cost) * item.quantity
        
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        
        logger.info(f"Created inventory item: {item.code}")
        return item
    
    async def get_item(self, item_id: UUID) -> Optional[InventoryItem]:
        """Get inventory item by ID"""
        result = await self.db.execute(
            select(InventoryItem).where(InventoryItem.id == item_id)
        )
        return result.scalar_one_or_none()
    
    async def get_item_by_code(self, code: str) -> Optional[InventoryItem]:
        """Get inventory item by code"""
        result = await self.db.execute(
            select(InventoryItem).where(InventoryItem.code == code)
        )
        return result.scalar_one_or_none()
    
    async def update_item(self, item_id: UUID, item_data: Dict[str, Any]) -> Optional[InventoryItem]:
        """Update inventory item"""
        item = await self.get_item(item_id)
        if not item:
            return None
        
        for key, value in item_data.items():
            setattr(item, key, value)
        
        # Recalculate total value
        if item.unit_cost and item.quantity:
            item.total_value = float(item.unit_cost) * item.quantity
        
        await self.db.commit()
        await self.db.refresh(item)
        
        logger.info(f"Updated inventory item: {item.code}")
        return item
    
    async def get_all_items(
        self,
        category_id: Optional[UUID] = None,
        status: Optional[InventoryStatus] = None,
        is_asset: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[InventoryItem]:
        """Get all inventory items with filters"""
        query = select(InventoryItem)
        
        conditions = []
        
        if category_id:
            conditions.append(InventoryItem.category_id == category_id)
        
        if status:
            conditions.append(InventoryItem.status == status)
        
        if is_asset is not None:
            conditions.append(InventoryItem.is_asset == is_asset)
        
        if search:
            conditions.append(
                or_(
                    InventoryItem.name.ilike(f"%{search}%"),
                    InventoryItem.code.ilike(f"%{search}%"),
                    InventoryItem.description.ilike(f"%{search}%")
                )
            )
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(InventoryItem.name)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    # T151: Stock alert logic
    async def get_low_stock_items(self) -> List[InventoryItem]:
        """Get items with low stock"""
        result = await self.db.execute(
            select(InventoryItem).where(
                InventoryItem.quantity <= InventoryItem.min_quantity
            ).order_by(InventoryItem.quantity.asc())
        )
        return result.scalars().all()
    
    async def get_items_needing_inspection(self) -> List[InventoryItem]:
        """Get items that need inspection"""
        today = date.today()
        result = await self.db.execute(
            select(InventoryItem).where(
                and_(
                    InventoryItem.is_asset == True,
                    InventoryItem.next_inspection_date <= today
                )
            ).order_by(InventoryItem.next_inspection_date)
        )
        return result.scalars().all()
    
    # ============ Categories ============
    
    async def create_category(self, category_data: Dict[str, Any]) -> InventoryCategory:
        """Create inventory category"""
        category = InventoryCategory(**category_data)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        
        logger.info(f"Created inventory category: {category.name}")
        return category
    
    async def get_categories(self, parent_id: Optional[UUID] = None) -> List[InventoryCategory]:
        """Get categories"""
        query = select(InventoryCategory)
        
        if parent_id:
            query = query.where(InventoryCategory.parent_category_id == parent_id)
        else:
            query = query.where(InventoryCategory.parent_category_id.is_(None))
        
        result = await self.db.execute(query.order_by(InventoryCategory.name))
        return result.scalars().all()
    
    # ============ Vendors ============
    
    async def create_vendor(self, vendor_data: Dict[str, Any]) -> Vendor:
        """Create vendor"""
        vendor = Vendor(**vendor_data)
        self.db.add(vendor)
        await self.db.commit()
        await self.db.refresh(vendor)
        
        logger.info(f"Created vendor: {vendor.code}")
        return vendor
    
    async def get_vendor(self, vendor_id: UUID) -> Optional[Vendor]:
        """Get vendor by ID"""
        result = await self.db.execute(
            select(Vendor).where(Vendor.id == vendor_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_vendors(self, is_active: Optional[bool] = None) -> List[Vendor]:
        """Get all vendors"""
        query = select(Vendor)
        
        if is_active is not None:
            query = query.where(Vendor.is_active == is_active)
        
        result = await self.db.execute(query.order_by(Vendor.name))
        return result.scalars().all()
    
    # T152: Purchase workflow
    async def create_purchase_order(
        self,
        vendor_id: UUID,
        requested_by: UUID,
        items: List[Dict[str, Any]],
        **kwargs
    ) -> PurchaseOrder:
        """Create purchase order"""
        
        # Generate PO number
        po_number = await self._generate_po_number()
        
        # Calculate totals
        total_amount = sum(item['quantity'] * item['unit_price'] for item in items)
        tax_amount = kwargs.get('tax_amount', 0)
        discount_amount = kwargs.get('discount_amount', 0)
        final_amount = total_amount + tax_amount - discount_amount
        
        # Create PO
        po = PurchaseOrder(
            po_number=po_number,
            vendor_id=vendor_id,
            requested_by=requested_by,
            total_amount=total_amount,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            final_amount=final_amount,
            order_date=date.today(),
            **{k: v for k, v in kwargs.items() if k not in ['tax_amount', 'discount_amount']}
        )
        
        self.db.add(po)
        await self.db.flush()
        
        # Add items
        for item_data in items:
            po_item = PurchaseOrderItem(
                purchase_order_id=po.id,
                inventory_item_id=item_data['inventory_item_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total_price=item_data['quantity'] * item_data['unit_price'],
                description=item_data.get('description')
            )
            self.db.add(po_item)
        
        await self.db.commit()
        await self.db.refresh(po)
        
        logger.info(f"Created purchase order: {po_number}")
        return po
    
    async def _generate_po_number(self) -> str:
        """Generate unique PO number"""
        today = date.today()
        prefix = f"PO{today.year}{today.month:02d}"
        
        result = await self.db.execute(
            select(func.count(PurchaseOrder.id)).where(
                PurchaseOrder.po_number.like(f"{prefix}%")
            )
        )
        count = result.scalar() or 0
        
        return f"{prefix}{count + 1:04d}"
    
    async def approve_purchase_order(
        self,
        po_id: UUID,
        approved_by: UUID
    ) -> Optional[PurchaseOrder]:
        """Approve purchase order"""
        po = await self.db.execute(
            select(PurchaseOrder).where(PurchaseOrder.id == po_id)
        )
        po = po.scalar_one_or_none()
        
        if not po:
            return None
        
        if po.status != PurchaseOrderStatus.SUBMITTED:
            raise ValueError(f"PO must be in SUBMITTED status to approve")
        
        po.status = PurchaseOrderStatus.APPROVED
        po.approved_by = approved_by
        po.approved_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(po)
        
        logger.info(f"Approved purchase order: {po.po_number}")
        return po
    
    async def receive_purchase_order(
        self,
        po_id: UUID,
        received_items: List[Dict[str, Any]],
        received_by: UUID
    ) -> Optional[PurchaseOrder]:
        """Receive items from purchase order"""
        po = await self.db.execute(
            select(PurchaseOrder).where(PurchaseOrder.id == po_id)
        )
        po = po.scalar_one_or_none()
        
        if not po:
            return None
        
        # Update received quantities and create stock transactions
        for item_data in received_items:
            # Update PO item
            po_item = await self.db.execute(
                select(PurchaseOrderItem).where(
                    and_(
                        PurchaseOrderItem.purchase_order_id == po_id,
                        PurchaseOrderItem.id == item_data['po_item_id']
                    )
                )
            )
            po_item = po_item.scalar_one_or_none()
            
            if po_item:
                received_qty = item_data['received_quantity']
                po_item.received_quantity += received_qty
                
                # Create stock transaction
                await self.add_stock(
                    item_id=po_item.inventory_item_id,
                    quantity=received_qty,
                    unit_cost=po_item.unit_price,
                    transaction_type=StockTransactionType.PURCHASE,
                    reference_type="purchase_order",
                    reference_id=po_id,
                    performed_by=received_by,
                    notes=f"Received from PO {po.po_number}"
                )
        
        # Update PO status
        po.status = PurchaseOrderStatus.RECEIVED
        po.actual_delivery_date = date.today()
        
        await self.db.commit()
        await self.db.refresh(po)
        
        logger.info(f"Received purchase order: {po.po_number}")
        return po
    
    # ============ Stock Transactions ============
    
    async def add_stock(
        self,
        item_id: UUID,
        quantity: int,
        performed_by: UUID,
        unit_cost: Optional[float] = None,
        transaction_type: StockTransactionType = StockTransactionType.PURCHASE,
        **kwargs
    ) -> StockTransaction:
        """Add stock to inventory"""
        
        # Get current item
        item = await self.get_item(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")
        
        # Update item quantity
        new_quantity = item.quantity + quantity
        item.quantity = new_quantity
        
        # Calculate costs
        total_cost = None
        if unit_cost:
            total_cost = unit_cost * quantity
            
            # Update item unit cost (weighted average)
            if item.unit_cost and item.quantity > 0:
                total_value = (float(item.unit_cost) * (item.quantity - quantity)) + total_cost
                item.unit_cost = total_value / item.quantity
            else:
                item.unit_cost = unit_cost
            
            item.total_value = float(item.unit_cost) * item.quantity
        
        # Create transaction
        transaction = StockTransaction(
            item_id=item_id,
            transaction_type=transaction_type,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=total_cost,
            balance_quantity=new_quantity,
            transaction_date=date.today(),
            performed_by=performed_by,
            **kwargs
        )
        
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        
        logger.info(f"Added {quantity} units to item {item.code}")
        return transaction
    
    async def remove_stock(
        self,
        item_id: UUID,
        quantity: int,
        performed_by: UUID,
        transaction_type: StockTransactionType = StockTransactionType.ISSUE,
        **kwargs
    ) -> StockTransaction:
        """Remove stock from inventory"""
        
        # Get current item
        item = await self.get_item(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")
        
        if item.quantity < quantity:
            raise ValueError(f"Insufficient stock. Available: {item.quantity}, Requested: {quantity}")
        
        # Update item quantity
        new_quantity = item.quantity - quantity
        item.quantity = new_quantity
        
        # Update total value
        if item.unit_cost:
            item.total_value = float(item.unit_cost) * item.quantity
        
        # Create transaction
        transaction = StockTransaction(
            item_id=item_id,
            transaction_type=transaction_type,
            quantity=-quantity,  # Negative for removal
            unit_cost=item.unit_cost,
            total_cost=float(item.unit_cost) * quantity if item.unit_cost else None,
            balance_quantity=new_quantity,
            transaction_date=date.today(),
            performed_by=performed_by,
            **kwargs
        )
        
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        
        logger.info(f"Removed {quantity} units from item {item.code}")
        return transaction
    
    async def get_stock_history(
        self,
        item_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[StockTransaction]:
        """Get stock transaction history"""
        query = select(StockTransaction).where(StockTransaction.item_id == item_id)
        
        if start_date:
            query = query.where(StockTransaction.transaction_date >= start_date)
        
        if end_date:
            query = query.where(StockTransaction.transaction_date <= end_date)
        
        query = query.order_by(StockTransaction.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    # ============ Reports ============
    
    async def get_inventory_summary(self) -> Dict[str, Any]:
        """Get inventory summary"""
        
        # Total items
        total_items_result = await self.db.execute(select(func.count(InventoryItem.id)))
        total_items = total_items_result.scalar()
        
        # Total value
        total_value_result = await self.db.execute(select(func.sum(InventoryItem.total_value)))
        total_value = total_value_result.scalar() or 0
        
        # Low stock items
        low_stock = await self.get_low_stock_items()
        
        # Items by status
        status_result = await self.db.execute(
            select(
                InventoryItem.status,
                func.count(InventoryItem.id)
            ).group_by(InventoryItem.status)
        )
        status_counts = {status: count for status, count in status_result.all()}
        
        return {
            "total_items": total_items,
            "total_value": float(total_value),
            "low_stock_count": len(low_stock),
            "by_status": status_counts,
            "low_stock_items": low_stock
        }
