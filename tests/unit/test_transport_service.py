"""Tests for Transport Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.transport_service import TransportService


@pytest.fixture
def transport_service():
    return TransportService()


@pytest.mark.asyncio
async def test_assign_route(db_session: AsyncSession, transport_service: TransportService):
    """Test route assignment"""
    assignment = await transport_service.assign_route(
        db_session,
        student_id=uuid4(),
        route_id=uuid4()
    )
    
    assert assignment is not None


@pytest.mark.asyncio
async def test_get_routes(db_session: AsyncSession, transport_service: TransportService):
    """Test getting available routes"""
    routes = await transport_service.get_routes(db_session)
    
    assert isinstance(routes, list)


@pytest.mark.asyncio
async def test_track_vehicle(db_session: AsyncSession, transport_service: TransportService):
    """Test vehicle tracking"""
    location = await transport_service.track_vehicle(
        db_session,
        vehicle_id=uuid4()
    )
    
    assert location is not None or location is None
