"""Tests for Book Loss Service"""
import pytest
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.book_loss_service import BookLossService


@pytest.fixture
def book_loss_service():
    return BookLossService()


@pytest.mark.asyncio
async def test_report_book_loss(db_session: AsyncSession, book_loss_service: BookLossService):
    """Test reporting lost book"""
    loss_data = {
        "book_id": uuid4(),
        "member_id": uuid4(),
        "reported_date": "2024-01-15",
        "circumstances": "Lost during transit"
    }
    
    loss_report = await book_loss_service.report_loss(db_session, loss_data)
    
    assert loss_report is not None
    assert loss_report.circumstances == "Lost during transit"


@pytest.mark.asyncio
async def test_calculate_replacement_cost(book_loss_service: BookLossService):
    """Test calculating book replacement cost"""
    book_price = Decimal("500.00")
    
    replacement_cost = book_loss_service.calculate_replacement_cost(
        book_price,
        processing_fee=Decimal("50.00")
    )
    
    assert replacement_cost == Decimal("550.00")


@pytest.mark.asyncio
async def test_process_compensation(db_session: AsyncSession, book_loss_service: BookLossService):
    """Test processing loss compensation"""
    compensation = await book_loss_service.process_compensation(
        db_session,
        loss_id=uuid4(),
        amount=Decimal("550.00"),
        payment_method="cash"
    )
    
    assert compensation is not None


@pytest.mark.asyncio
async def test_mark_book_as_lost(db_session: AsyncSession, book_loss_service: BookLossService):
    """Test marking book as lost in inventory"""
    success = await book_loss_service.mark_as_lost(
        db_session,
        book_id=uuid4()
    )
    
    assert isinstance(success, bool)


@pytest.mark.asyncio
async def test_get_loss_statistics(db_session: AsyncSession, book_loss_service: BookLossService):
    """Test getting book loss statistics"""
    stats = await book_loss_service.get_statistics(
        db_session,
        year=2024
    )
    
    assert stats is not None


@pytest.mark.asyncio
async def test_notify_member_about_loss(db_session: AsyncSession, book_loss_service: BookLossService):
    """Test sending loss notification"""
    success = await book_loss_service.notify_member(
        db_session,
        loss_id=uuid4()
    )
    
    assert isinstance(success, bool)
