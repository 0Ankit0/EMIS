"""Library Settings API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

from src.database import get_db
from src.services.fine_service import FineService
from src.models.library_settings import MemberType
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/library/settings", tags=["library-settings"])


class LibrarySettingsCreate(BaseModel):
    member_type: MemberType
    max_books_allowed: int = 3
    borrowing_period_days: int = 14
    fine_per_day: float = 5.0
    grace_period_days: int = 0
    max_fine_amount: float = 500.0
    max_reservations: int = 2
    reservation_hold_days: int = 3
    max_renewals: int = 2
    digital_access_enabled: bool = True
    digital_download_limit: int = 10
    description: Optional[str] = None


class LibrarySettingsResponse(BaseModel):
    id: int
    member_type: MemberType
    max_books_allowed: int
    borrowing_period_days: int
    fine_per_day: float
    grace_period_days: int
    max_fine_amount: float
    max_reservations: int
    reservation_hold_days: int
    max_renewals: int
    digital_access_enabled: bool
    digital_download_limit: int
    is_active: bool
    description: Optional[str]
    
    class Config:
        from_attributes = True


class FineCalculationRequest(BaseModel):
    member_type: MemberType
    due_date: date
    return_date: Optional[date] = None


class FineCalculationResponse(BaseModel):
    fine_amount: float
    days_overdue: int
    member_type: MemberType


class FineWaiverCreate(BaseModel):
    fine_id: int
    member_id: int
    original_amount: float
    waived_amount: float
    reason: str


class FineWaiverResponse(BaseModel):
    id: int
    fine_id: int
    member_id: int
    original_amount: float
    waived_amount: float
    final_amount: float
    reason: str
    approved_by: int
    
    class Config:
        from_attributes = True


@router.post("/", response_model=LibrarySettingsResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_settings(
    settings_data: LibrarySettingsCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["library:admin"]))
):
    """Create or update library settings for a member type"""
    service = FineService(db)
    settings = await service.create_library_settings(
        **settings_data.dict(),
        updated_by=current_user.get("id")
    )
    return settings


@router.get("/", response_model=List[LibrarySettingsResponse])
async def get_all_settings(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["library:read"]))
):
    """Get all library settings"""
    service = FineService(db)
    settings = await service.get_all_library_settings()
    return settings


@router.get("/{member_type}", response_model=LibrarySettingsResponse)
async def get_settings_by_member_type(
    member_type: MemberType,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["library:read"]))
):
    """Get library settings for a specific member type"""
    service = FineService(db)
    settings = await service.get_library_settings(member_type)
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Settings not found for member type: {member_type}"
        )
    
    return settings


@router.post("/calculate-fine", response_model=FineCalculationResponse)
async def calculate_fine(
    fine_data: FineCalculationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["library:read"]))
):
    """Calculate fine for an overdue book"""
    service = FineService(db)
    fine_amount, days_overdue = await service.calculate_fine(
        fine_data.member_type,
        fine_data.due_date,
        fine_data.return_date
    )
    
    return FineCalculationResponse(
        fine_amount=fine_amount,
        days_overdue=days_overdue,
        member_type=fine_data.member_type
    )


@router.post("/fine-waiver", response_model=FineWaiverResponse, status_code=status.HTTP_201_CREATED)
async def create_fine_waiver(
    waiver_data: FineWaiverCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["library:admin"]))
):
    """Create a fine waiver"""
    service = FineService(db)
    waiver = await service.create_fine_waiver(
        **waiver_data.dict(),
        approved_by=current_user.get("id")
    )
    return waiver


@router.get("/member/{member_id}/waivers", response_model=List[FineWaiverResponse])
async def get_member_waivers(
    member_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["library:read"]))
):
    """Get all fine waivers for a member"""
    service = FineService(db)
    waivers = await service.get_fine_waivers_by_member(member_id)
    return waivers


@router.post("/initialize-defaults", status_code=status.HTTP_201_CREATED)
async def initialize_default_settings(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["library:admin"]))
):
    """Initialize default library settings for all member types"""
    service = FineService(db)
    await service.initialize_default_settings(created_by=current_user.get("id"))
    return {"message": "Default settings initialized successfully"}
