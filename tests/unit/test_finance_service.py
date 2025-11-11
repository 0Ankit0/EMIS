"""Tests for Finance Service"""
import pytest
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.finance_service import FinanceService


@pytest.fixture
def finance_service():
    return FinanceService()


@pytest.mark.asyncio
async def test_calculate_net_amount(finance_service: FinanceService):
    """Test net amount calculation"""
    gross = Decimal("100000.00")
    tax = Decimal("10000.00")
    
    net = finance_service.calculate_net(gross, tax)
    
    assert net == Decimal("90000.00")


@pytest.mark.asyncio
async def test_generate_invoice(db_session: AsyncSession, finance_service: FinanceService):
    """Test invoice generation"""
    invoice = await finance_service.generate_invoice(
        db_session,
        customer_id=uuid4(),
        amount=Decimal("50000.00"),
        items=[]
    )
    
    assert invoice is not None


@pytest.mark.asyncio
async def test_process_refund(db_session: AsyncSession, finance_service: FinanceService):
    """Test refund processing"""
    refund = await finance_service.process_refund(
        db_session,
        transaction_id=uuid4(),
        amount=Decimal("1000.00")
    )
    
    assert refund is not None
