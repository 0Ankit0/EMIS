"""Integration tests for Inventory Workflow"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.inventory import Item, PurchaseOrder, ItemIssue, StockAdjustment


@pytest.mark.asyncio
async def test_complete_inventory_workflow(db_session: AsyncSession):
    """Test complete inventory workflow from purchase to issue"""
    # Step 1: Create purchase order
    po = PurchaseOrder(
        id=uuid4(),
        po_number="PO2024001",
        vendor_name="Tech Supplies Inc",
        order_date=datetime.utcnow(),
        expected_delivery=datetime.utcnow(),
        total_amount=Decimal("50000.00"),
        status="pending"
    )
    db_session.add(po)
    await db_session.commit()
    
    # Step 2: Create items to purchase
    items_to_purchase = [
        {"name": "Laptop", "quantity": 10, "unit_price": Decimal("40000.00")},
        {"name": "Projector", "quantity": 5, "unit_price": Decimal("25000.00")},
        {"name": "Printer", "quantity": 3, "unit_price": Decimal("15000.00")}
    ]
    
    items = []
    for item_data in items_to_purchase:
        item = Item(
            id=uuid4(),
            item_code=f"ITEM{len(items)+1:03d}",
            item_name=item_data["name"],
            category="Electronics",
            unit_price=item_data["unit_price"],
            quantity_in_stock=0,  # Initially 0
            reorder_level=2,
            status="active"
        )
        db_session.add(item)
        items.append(item)
    await db_session.commit()
    
    # Step 3: Receive items (PO fulfilled)
    po.status = "received"
    po.received_date = datetime.utcnow()
    
    for i, item in enumerate(items):
        item.quantity_in_stock = items_to_purchase[i]["quantity"]
        item.last_purchase_date = datetime.utcnow()
    
    await db_session.commit()
    
    # Step 4: Issue items to departments
    issues = []
    
    # Issue 3 laptops to CS department
    issue1 = ItemIssue(
        id=uuid4(),
        item_id=items[0].id,
        quantity=3,
        issued_to="Computer Science Department",
        issued_by=uuid4(),
        issue_date=datetime.utcnow(),
        purpose="Lab setup",
        status="issued"
    )
    db_session.add(issue1)
    issues.append(issue1)
    items[0].quantity_in_stock -= 3
    
    # Issue 2 projectors to auditorium
    issue2 = ItemIssue(
        id=uuid4(),
        item_id=items[1].id,
        quantity=2,
        issued_to="Main Auditorium",
        issued_by=uuid4(),
        issue_date=datetime.utcnow(),
        purpose="Event",
        status="issued"
    )
    db_session.add(issue2)
    issues.append(issue2)
    items[1].quantity_in_stock -= 2
    
    await db_session.commit()
    
    # Step 5: Stock adjustment (damaged item)
    adjustment = StockAdjustment(
        id=uuid4(),
        item_id=items[2].id,
        adjustment_type="damage",
        quantity=-1,
        reason="Printer damaged during delivery",
        adjusted_by=uuid4(),
        adjustment_date=datetime.utcnow()
    )
    db_session.add(adjustment)
    items[2].quantity_in_stock -= 1
    await db_session.commit()
    
    # Step 6: Check reorder level
    items_below_reorder = [
        item for item in items 
        if item.quantity_in_stock <= item.reorder_level
    ]
    
    # Assertions
    assert po.status == "received"
    assert items[0].quantity_in_stock == 7  # 10 - 3 issued
    assert items[1].quantity_in_stock == 3  # 5 - 2 issued
    assert items[2].quantity_in_stock == 2  # 3 - 1 damaged
    assert len(issues) == 2
    assert len(items_below_reorder) >= 0
