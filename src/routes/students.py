"""Student API routes for EMIS."""
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import get_current_user, require_permissions
from src.models.auth import User
from src.models.student import Student, StudentStatus, Gender
from src.services.student_service import StudentService
from src.services.student_workflow import StudentWorkflowService


router = APIRouter(prefix="/api/v1/students", tags=["Students"])


# Pydantic schemas
class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: date
    gender: Optional[Gender] = None
    nationality: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    gender: Optional[Gender] = None
    nationality: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class StudentResponse(BaseModel):
    id: UUID
    student_number: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: str
    phone: Optional[str]
    date_of_birth: date
    gender: Optional[str]
    status: str
    admission_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    items: List[StudentResponse]
    total: int
    page: int
    size: int


class AdmissionRequest(BaseModel):
    admission_date: Optional[datetime] = None


class GraduationRequest(BaseModel):
    graduation_date: datetime
    degree_earned: str
    honors: Optional[str] = None


# API Endpoints
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:create")),
):
    """Create a new student record."""
    service = StudentService(db)

    # Check if email already exists
    existing = await service.get_student_by_email(student_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this email already exists",
        )

    student = await service.create_student(
        first_name=student_data.first_name,
        middle_name=student_data.middle_name,
        last_name=student_data.last_name,
        email=student_data.email,
        phone=student_data.phone,
        date_of_birth=student_data.date_of_birth,
        gender=student_data.gender.value if student_data.gender else None,
        nationality=student_data.nationality,
        address=student_data.address,
        user_id=current_user.id,
    )

    return student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:read")),
):
    """Get student by ID."""
    service = StudentService(db)
    student = await service.get_student_by_id(student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )

    return student


@router.get("/", response_model=StudentListResponse)
async def list_students(
    status_filter: Optional[StudentStatus] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:read")),
):
    """List students with pagination and filters."""
    service = StudentService(db)
    skip = (page - 1) * size

    students, total = await service.list_students(
        status=status_filter, skip=skip, limit=size
    )

    return {
        "items": students,
        "total": total,
        "page": page,
        "size": size,
    }


@router.patch("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: UUID,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:update")),
):
    """Update student information."""
    service = StudentService(db)

    # Filter out None values
    update_data = {k: v for k, v in student_data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    student = await service.update_student(
        student_id, user_id=current_user.id, **update_data
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )

    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:delete")),
):
    """Delete (soft delete) a student."""
    service = StudentService(db)
    success = await service.delete_student(student_id, user_id=current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )


@router.post("/{student_id}/admit", response_model=StudentResponse)
async def admit_student(
    student_id: UUID,
    admission_data: AdmissionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:admit")),
):
    """Admit a student (transition from applicant to active)."""
    workflow_service = StudentWorkflowService(db)

    student = await workflow_service.admit_student(
        student_id,
        admission_date=admission_data.admission_date,
        user_id=current_user.id,
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or cannot be admitted",
        )

    return student


@router.post("/{student_id}/graduate", response_model=StudentResponse)
async def graduate_student(
    student_id: UUID,
    graduation_data: GraduationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:graduate")),
):
    """Graduate a student."""
    workflow_service = StudentWorkflowService(db)

    student = await workflow_service.graduate_student(
        student_id,
        graduation_date=graduation_data.graduation_date,
        degree_earned=graduation_data.degree_earned,
        honors=graduation_data.honors,
        user_id=current_user.id,
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or cannot be graduated",
        )

    return student


@router.get("/{student_id}/gpa")
async def get_student_gpa(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("students:read")),
):
    """Get student's cumulative GPA."""
    service = StudentService(db)
    gpa = await service.calculate_gpa(student_id)

    if gpa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or no academic records",
        )

    return {"student_id": student_id, "cumulative_gpa": gpa}
