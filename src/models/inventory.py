"""
Inventory and Resource Management Models for EMIS
"""
from datetime import datetime, date
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Numeric, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class InventoryStatus(str, Enum):
    """Inventory item status"""
    AVAILABLE = "available"
    IN_USE = "in_use"
    UNDER_MAINTENANCE = "under_maintenance"
    DAMAGED = "damaged"
    LOST = "lost"
    DISPOSED = "disposed"


class PurchaseOrderStatus(str, Enum):
    """Purchase order status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    ORDERED = "ordered"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class InventoryCategory(Base):
    """Inventory category model"""
    __tablename__ = "inventory_categories"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Hierarchy support
    parent_category_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("inventory_categories.id"))
    
    # Settings
    requires_approval: Mapped[bool] = mapped_column(default=False)
    is_consumable: Mapped[bool] = mapped_column(default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent_category = relationship("InventoryCategory", remote_side=[id], back_populates="subcategories")
    subcategories = relationship("InventoryCategory", back_populates="parent_category")
    items = relationship("InventoryItem", back_populates="category")
    
    def __repr__(self) -> str:
        return f"<InventoryCategory(name='{self.name}')>"


class InventoryItem(Base):
    """Inventory item model"""
    __tablename__ = "inventory_items"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Basic information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    category_id: Mapped[UUID] = mapped_column(ForeignKey("inventory_categories.id"), nullable=False)
    
    # Quantity and location
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    min_quantity: Mapped[int] = mapped_column(Integer, default=0)  # Minimum stock level
    max_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    unit: Mapped[str] = mapped_column(String(50))  # pieces, kg, liters, etc.
    location: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Financial
    unit_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    total_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    
    # Status
    status: Mapped[InventoryStatus] = mapped_column(String(50), default=InventoryStatus.AVAILABLE, index=True)
    
    # Asset details (for non-consumables)
    is_asset: Mapped[bool] = mapped_column(default=False)
    asset_tag: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True)
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    model: Mapped[Optional[str]] = mapped_column(String(255))
    manufacturer: Mapped[Optional[str]] = mapped_column(String(255))
    purchase_date: Mapped[Optional[date]] = mapped_column(Date)
    warranty_expiry: Mapped[Optional[date]] = mapped_column(Date)
    
    # Tracking
    last_inspection_date: Mapped[Optional[date]] = mapped_column(Date)
    next_inspection_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("InventoryCategory", back_populates="items")
    transactions = relationship("StockTransaction", back_populates="item", cascade="all, delete-orphan")
    
    @property
    def is_low_stock(self) -> bool:
        """Check if item is low on stock"""
        return self.quantity <= self.min_quantity
    
    @property
    def needs_reorder(self) -> bool:
        """Check if item needs reordering"""
        return self.quantity < self.min_quantity
    
    def __repr__(self) -> str:
        return f"<InventoryItem(code='{self.code}', name='{self.name}')>"


class Vendor(Base):
    """Vendor/Supplier model"""
    __tablename__ = "vendors"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Basic information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    # Contact information
    contact_person: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(Text)
    
    # Business information
    gstin: Mapped[Optional[str]] = mapped_column(String(50))  # GST Identification Number
    pan: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Banking
    bank_name: Mapped[Optional[str]] = mapped_column(String(255))
    account_number: Mapped[Optional[str]] = mapped_column(String(50))
    ifsc_code: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5 rating
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")
    
    def __repr__(self) -> str:
        return f"<Vendor(code='{self.code}', name='{self.name}')>"


class PurchaseOrder(Base):
    """Purchase order model"""
    __tablename__ = "purchase_orders"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Order information
    po_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    vendor_id: Mapped[UUID] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    
    # Dates
    order_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    expected_delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    actual_delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Financial
    total_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    discount_amount: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    final_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Status
    status: Mapped[PurchaseOrderStatus] = mapped_column(String(50), default=PurchaseOrderStatus.DRAFT, index=True)
    
    # Approval workflow
    requested_by: Mapped[UUID] = mapped_column(nullable=False)
    approved_by: Mapped[Optional[UUID]] = mapped_column()
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Delivery information
    delivery_address: Mapped[Optional[str]] = mapped_column(Text)
    shipping_method: Mapped[Optional[str]] = mapped_column(String(100))
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    terms_and_conditions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<PurchaseOrder(po_number='{self.po_number}', status='{self.status}')>"


class PurchaseOrderItem(Base):
    """Purchase order items"""
    __tablename__ = "purchase_order_items"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    purchase_order_id: Mapped[UUID] = mapped_column(ForeignKey("purchase_orders.id"), nullable=False)
    inventory_item_id: Mapped[UUID] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    
    received_quantity: Mapped[int] = mapped_column(Integer, default=0)
    
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    inventory_item = relationship("InventoryItem")
    
    def __repr__(self) -> str:
        return f"<PurchaseOrderItem(po_id={self.purchase_order_id}, item_id={self.inventory_item_id})>"


class StockTransactionType(str, Enum):
    """Stock transaction types"""
    PURCHASE = "purchase"
    SALE = "sale"
    ISSUE = "issue"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    LOSS = "loss"
    TRANSFER = "transfer"


class StockTransaction(Base):
    """Stock transaction model for tracking inventory movements"""
    __tablename__ = "stock_transactions"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    item_id: Mapped[UUID] = mapped_column(ForeignKey("inventory_items.id"), nullable=False, index=True)
    
    # Transaction details
    transaction_type: Mapped[StockTransactionType] = mapped_column(String(50), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    total_cost: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    
    # Balance after transaction
    balance_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # References
    reference_type: Mapped[Optional[str]] = mapped_column(String(50))  # purchase_order, issue, etc.
    reference_id: Mapped[Optional[UUID]] = mapped_column()
    
    # Location and assignment
    from_location: Mapped[Optional[str]] = mapped_column(String(255))
    to_location: Mapped[Optional[str]] = mapped_column(String(255))
    issued_to: Mapped[Optional[UUID]] = mapped_column()  # User/Student ID
    
    # Details
    reason: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Tracking
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    performed_by: Mapped[UUID] = mapped_column(nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    
    # Relationships
    item = relationship("InventoryItem", back_populates="transactions")
    
    def __repr__(self) -> str:
        return f"<StockTransaction(type='{self.transaction_type}', quantity={self.quantity})>"
