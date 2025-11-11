

"""Attendance API routes for EMIS."""
from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.services.attendance_service import AttendanceService


router = APIRouter(prefix="/api/v1/attendance", tags=["Attendance"])


# T070: Leave request endpoints
class LeaveRequestCreate(BaseModel):
    course_id: UUID
    subject_teacher_id: UUID
    leave_date: date
    leave_type: str
    reason: str
    supporting_document_url: Optional[str] = None


class LeaveRequestApprove(BaseModel):
    approved: bool
    rejection_reason: Optional[str] = None


@router.post("/leave-requests", status_code=status.HTTP_201_CREATED)
async def create_leave_request(
    leave_data: LeaveRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["attendance:request_leave"]))
):
    """Student creates leave request (T064)"""
    service = AttendanceService(db)
    
    try:
        leave_request = await service.create_leave_request(
            student_id=current_user.get("student_id"),
            **leave_data.dict()
        )
        return {
            "id": leave_request.id,
            "student_id": leave_request.student_id,
            "leave_date": leave_request.leave_date,
            "status": leave_request.status,
            "message": "Leave request submitted successfully. Waiting for teacher approval."
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/leave-requests/pending")
async def get_pending_leave_requests(
    course_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["attendance:approve_leave"]))
):
    """Teacher gets pending leave requests (T071)"""
    service = AttendanceService(db)
    
    requests = await service.get_pending_leave_requests(
        teacher_id=current_user.get("id"),
        course_id=course_id
    )
    
    return {
        "pending_requests": [
            {
                "id": req.id,
                "student_id": req.student_id,
                "course_id": req.course_id,
                "leave_date": req.leave_date,
                "leave_type": req.leave_type,
                "reason": req.reason,
                "supporting_document_url": req.supporting_document_url,
                "requested_at": req.requested_at
            }
            for req in requests
        ],
        "total": len(requests)
    }


@router.post("/leave-requests/{request_id}/approve")
async def approve_leave_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["attendance:approve_leave"]))
):
    """Teacher approves leave request (T071, T065)"""
    service = AttendanceService(db)
    
    try:
        leave_request = await service.approve_leave_request(
            leave_request_id=request_id,
            approved_by=current_user.get("id")
        )
        return {
            "id": leave_request.id,
            "status": leave_request.status,
            "approved_at": leave_request.approved_at,
            "message": "Leave approved. Attendance automatically marked as LEAVE for the requested date."
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/leave-requests/{request_id}/reject")
async def reject_leave_request(
    request_id: UUID,
    rejection_data: LeaveRequestApprove,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["attendance:approve_leave"]))
):
    """Teacher rejects leave request (T071)"""
    service = AttendanceService(db)
    
    if not rejection_data.rejection_reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection reason is required"
        )
    
    try:
        leave_request = await service.reject_leave_request(
            leave_request_id=request_id,
            rejected_by=current_user.get("id"),
            rejection_reason=rejection_data.rejection_reason
        )
        return {
            "id": leave_request.id,
            "status": leave_request.status,
            "rejection_reason": leave_request.rejection_reason,
            "message": "Leave request rejected"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/leave-requests/student/{student_id}")
async def get_student_leave_requests(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["attendance:read"]))
):
    """Get all leave requests for a student"""
    from sqlalchemy import select
    from src.models.attendance import LeaveRequest
    
    result = await db.execute(
        select(LeaveRequest).where(
            LeaveRequest.student_id == student_id
        ).order_by(LeaveRequest.requested_at.desc())
    )
    requests = result.scalars().all()
    
    return {
        "leave_requests": [
            {
                "id": req.id,
                "course_id": req.course_id,
                "leave_date": req.leave_date,
                "leave_type": req.leave_type,
                "reason": req.reason,
                "status": req.status,
                "requested_at": req.requested_at,
                "approved_at": req.approved_at,
                "rejection_reason": req.rejection_reason
            }
            for req in requests
        ]
    }
