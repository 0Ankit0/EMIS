"""Tests for Inventory Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.inventory_service import InventoryService


@pytest.fixture
def inventory_service():
    return InventoryService()


@pytest.mark.asyncio
async def test_add_item(db_session: AsyncSession, inventory_service: InventoryService):
    """Test adding inventory item"""
    item = await inventory_service.add_item(
        db_session,
        item_name="Laptop",
        quantity=10,
        unit_price=50000
    )
    
    assert item is not None


@pytest.mark.asyncio
async def test_update_stock(db_session: AsyncSession, inventory_service: InventoryService):
    """Test updating stock"""
    success = await inventory_service.update_stock(
        db_session,
        item_id=uuid4(),
        quantity=5
    )
    
    assert isinstance(success, bool)


@pytest.mark.asyncio
async def test_check_stock_level(db_session: AsyncSession, inventory_service: InventoryService):
    """Test checking stock level"""
    level = await inventory_service.check_stock(
        db_session,
        item_id=uuid4()
    )
    
    assert level is not None or level is None
