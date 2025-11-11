"""Leave management API routes for EMIS."""
from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.models.auth import User
from src.models.leave import Leave, LeaveType, LeaveStatus


router = APIRouter(prefix="/api/v1/hr/leave", tags=["Leave Management"])


class LeaveCreate(BaseModel):
    employee_id: UUID
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str


class LeaveResponse(BaseModel):
    id: UUID
    employee_id: UUID
    leave_type: str
    start_date: date
    end_date: date
    number_of_days: int
    status: str
    reason: str

    class Config:
        from_attributes = True


@router.post("/", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
async def submit_leave_request(
    leave_data: LeaveCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("leave:create")),
):
    """Submit a leave request."""
    # Calculate number of days
    number_of_days = (leave_data.end_date - leave_data.start_date).days + 1

    leave = Leave(
        **leave_data.dict(),
        number_of_days=number_of_days,
        status=LeaveStatus.PENDING
    )

    db.add(leave)
    await db.commit()
    await db.refresh(leave)

    return leave


@router.patch("/{leave_id}/approve")
async def approve_leave(
    leave_id: UUID,
    comments: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("leave:approve")),
):
    """Approve a leave request."""
    leave = await db.get(Leave, leave_id)

    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found"
        )

    leave.status = LeaveStatus.APPROVED
    leave.approved_by = current_user.id
    leave.approved_at = datetime.utcnow()
    leave.approval_comments = comments

    await db.commit()
    await db.refresh(leave)

    return leave


@router.patch("/{leave_id}/reject")
async def reject_leave(
    leave_id: UUID,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("leave:approve")),
):
    """Reject a leave request."""
    leave = await db.get(Leave, leave_id)

    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found"
        )

    leave.status = LeaveStatus.REJECTED
    leave.rejected_by = current_user.id
    leave.rejected_at = datetime.utcnow()
    leave.rejection_reason = reason

    await db.commit()
    await db.refresh(leave)

    return leave
