"""
Inventory Management Routes for EMIS
"""
from datetime import date
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.database import get_db
from src.services.inventory_service import InventoryService
from src.middleware.rbac import get_current_user
from src.models.auth import User
from src.models.inventory import InventoryStatus, PurchaseOrderStatus, StockTransactionType

router = APIRouter(prefix="/inventory", tags=["inventory"])


# ============ Schemas ============

class InventoryItemCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    category_id: UUID
    quantity: int = 0
    min_quantity: int = 0
    max_quantity: Optional[int] = None
    unit: str
    location: Optional[str] = None
    unit_cost: Optional[float] = None
    is_asset: bool = False
    asset_tag: Optional[str] = None
    serial_number: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None


class CategoryCreate(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    parent_category_id: Optional[UUID] = None
    is_consumable: bool = False


class VendorCreate(BaseModel):
    name: str
    code: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None


class PurchaseOrderItemData(BaseModel):
    inventory_item_id: UUID
    quantity: int
    unit_price: float
    description: Optional[str] = None


class PurchaseOrderCreate(BaseModel):
    vendor_id: UUID
    items: List[PurchaseOrderItemData]
    expected_delivery_date: Optional[date] = None
    tax_amount: float = 0
    discount_amount: float = 0
    delivery_address: Optional[str] = None
    notes: Optional[str] = None


class StockAdjustment(BaseModel):
    quantity: int
    unit_cost: Optional[float] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


# ============ Inventory Items ============

@router.post("/items", status_code=201)
async def create_inventory_item(
    item_data: InventoryItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create inventory item"""
    service = InventoryService(db)
    
    item = await service.create_item(item_data.dict())
    
    return {"message": "Inventory item created successfully", "item_id": item.id}


@router.get("/items")
async def get_inventory_items(
    category_id: Optional[UUID] = Query(None),
    status: Optional[InventoryStatus] = Query(None),
    is_asset: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all inventory items with filters"""
    service = InventoryService(db)
    
    items = await service.get_all_items(
        category_id=category_id,
        status=status,
        is_asset=is_asset,
        search=search
    )
    
    return {"items": items, "count": len(items)}


@router.get("/items/low-stock")
async def get_low_stock_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get items with low stock"""
    service = InventoryService(db)
    
    items = await service.get_low_stock_items()
    
    return {"items": items, "count": len(items)}


@router.get("/items/need-inspection")
async def get_items_needing_inspection(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get items that need inspection"""
    service = InventoryService(db)
    
    items = await service.get_items_needing_inspection()
    
    return {"items": items, "count": len(items)}


@router.get("/items/{item_id}")
async def get_inventory_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inventory item by ID"""
    service = InventoryService(db)
    
    item = await service.get_item(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


@router.put("/items/{item_id}")
async def update_inventory_item(
    item_id: UUID,
    item_data: InventoryItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update inventory item"""
    service = InventoryService(db)
    
    item = await service.update_item(item_id, item_data.dict())
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": "Item updated successfully"}


# ============ Stock Management ============

@router.post("/items/{item_id}/add-stock")
async def add_stock(
    item_id: UUID,
    stock_data: StockAdjustment,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add stock to inventory"""
    service = InventoryService(db)
    
    try:
        transaction = await service.add_stock(
            item_id=item_id,
            quantity=stock_data.quantity,
            unit_cost=stock_data.unit_cost,
            performed_by=current_user.id,
            transaction_type=StockTransactionType.ADJUSTMENT,
            reason=stock_data.reason,
            notes=stock_data.notes
        )
        
        return {"message": "Stock added successfully", "transaction_id": transaction.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/items/{item_id}/remove-stock")
async def remove_stock(
    item_id: UUID,
    stock_data: StockAdjustment,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove stock from inventory"""
    service = InventoryService(db)
    
    try:
        transaction = await service.remove_stock(
            item_id=item_id,
            quantity=stock_data.quantity,
            performed_by=current_user.id,
            transaction_type=StockTransactionType.ISSUE,
            reason=stock_data.reason,
            notes=stock_data.notes
        )
        
        return {"message": "Stock removed successfully", "transaction_id": transaction.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/items/{item_id}/history")
async def get_stock_history(
    item_id: UUID,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get stock transaction history"""
    service = InventoryService(db)
    
    transactions = await service.get_stock_history(
        item_id=item_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return {"transactions": transactions, "count": len(transactions)}


# ============ Categories ============

@router.post("/categories", status_code=201)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create inventory category"""
    service = InventoryService(db)
    
    category = await service.create_category(category_data.dict())
    
    return {"message": "Category created successfully", "category_id": category.id}


@router.get("/categories")
async def get_categories(
    parent_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get categories"""
    service = InventoryService(db)
    
    categories = await service.get_categories(parent_id=parent_id)
    
    return {"categories": categories, "count": len(categories)}


# ============ Vendors ============

@router.post("/vendors", status_code=201)
async def create_vendor(
    vendor_data: VendorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create vendor"""
    service = InventoryService(db)
    
    vendor = await service.create_vendor(vendor_data.dict())
    
    return {"message": "Vendor created successfully", "vendor_id": vendor.id}


@router.get("/vendors")
async def get_vendors(
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all vendors"""
    service = InventoryService(db)
    
    vendors = await service.get_all_vendors(is_active=is_active)
    
    return {"vendors": vendors, "count": len(vendors)}


@router.get("/vendors/{vendor_id}")
async def get_vendor(
    vendor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get vendor by ID"""
    service = InventoryService(db)
    
    vendor = await service.get_vendor(vendor_id)
    
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    return vendor


# ============ Purchase Orders ============

@router.post("/purchase-orders", status_code=201)
async def create_purchase_order(
    po_data: PurchaseOrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create purchase order"""
    service = InventoryService(db)
    
    po = await service.create_purchase_order(
        vendor_id=po_data.vendor_id,
        requested_by=current_user.id,
        items=[item.dict() for item in po_data.items],
        expected_delivery_date=po_data.expected_delivery_date,
        tax_amount=po_data.tax_amount,
        discount_amount=po_data.discount_amount,
        delivery_address=po_data.delivery_address,
        notes=po_data.notes
    )
    
    return {"message": "Purchase order created successfully", "po_id": po.id, "po_number": po.po_number}


@router.post("/purchase-orders/{po_id}/approve")
async def approve_purchase_order(
    po_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve purchase order"""
    service = InventoryService(db)
    
    try:
        po = await service.approve_purchase_order(po_id, current_user.id)
        
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        
        return {"message": "Purchase order approved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class ReceiveItemData(BaseModel):
    po_item_id: UUID
    received_quantity: int


class ReceivePOData(BaseModel):
    items: List[ReceiveItemData]


@router.post("/purchase-orders/{po_id}/receive")
async def receive_purchase_order(
    po_id: UUID,
    receive_data: ReceivePOData,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Receive items from purchase order"""
    service = InventoryService(db)
    
    po = await service.receive_purchase_order(
        po_id=po_id,
        received_items=[item.dict() for item in receive_data.items],
        received_by=current_user.id
    )
    
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    return {"message": "Items received successfully"}


# ============ Summary & Reports ============

@router.get("/summary")
async def get_inventory_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inventory summary"""
    service = InventoryService(db)
    
    summary = await service.get_inventory_summary()
    
    return summary
