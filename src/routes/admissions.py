"""Admissions API routes for EMIS."""
from datetime import date
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.models.auth import User


router = APIRouter(prefix="/api/v1/admissions", tags=["Admissions"])


class ApplicationCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date
    program_id: UUID
    academic_year: str
    previous_education: Optional[str] = None
    marks_obtained: Optional[float] = None


class ApplicationResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    program_id: UUID
    application_status: str
    application_date: date

    class Config:
        from_attributes = True


class ApplicationReview(BaseModel):
    status: str
    comments: Optional[str] = None
    interview_date: Optional[date] = None


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    application_data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Submit a new admission application."""
    return {"message": "Application submitted successfully"}


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("admissions:read")),
):
    """Get application details."""
    return {"message": "Application details"}


@router.patch("/applications/{application_id}/review")
async def review_application(
    application_id: UUID,
    review_data: ApplicationReview,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("admissions:review")),
):
    """Review an application."""
    return {"message": "Application reviewed successfully"}


@router.post("/applications/{application_id}/approve")
async def approve_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("admissions:approve")),
):
    """Approve an application and create student record."""
    return {"message": "Application approved, student record created"}


@router.get("/applications")
async def list_applications(
    status: Optional[str] = None,
    program_id: Optional[UUID] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("admissions:read")),
):
    """List applications with filters."""
    return {"items": [], "total": 0, "page": page, "size": size}
