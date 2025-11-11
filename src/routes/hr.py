"""HR and Employee API routes for EMIS."""
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.models.auth import User
from src.models.employee import Employee, EmploymentType, EmployeeStatus
from src.services.hr_service import HRService


router = APIRouter(prefix="/api/v1/hr", tags=["HR & Employees"])


# Pydantic schemas
class EmployeeCreate(BaseModel):
    employee_number: str
    first_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = None
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    date_of_joining: date
    department: str
    designation: str
    employment_type: EmploymentType
    basic_salary: Optional[float] = None


class EmployeeUpdate(BaseModel):
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    basic_salary: Optional[float] = None
    status: Optional[EmployeeStatus] = None
    manager_id: Optional[UUID] = None


class EmployeeResponse(BaseModel):
    id: UUID
    employee_number: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: str
    phone: Optional[str]
    department: str
    designation: str
    employment_type: str
    status: str
    date_of_joining: date
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    items: List[EmployeeResponse]
    total: int
    page: int
    size: int


# API Endpoints
@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("employees:create")),
):
    """Create a new employee record."""
    service = HRService(db)

    employee = await service.create_employee(
        employee_number=employee_data.employee_number,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=employee_data.email,
        date_of_joining=employee_data.date_of_joining,
        department=employee_data.department,
        designation=employee_data.designation,
        employment_type=employee_data.employment_type.value,
        basic_salary=employee_data.basic_salary,
        user_id=current_user.id,
    )

    return employee


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("employees:read")),
):
    """Get employee by ID."""
    service = HRService(db)
    employee = await service.get_employee_by_id(employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )

    return employee


@router.get("/employees", response_model=EmployeeListResponse)
async def list_employees(
    department: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("employees:read")),
):
    """List employees with pagination and filters."""
    service = HRService(db)
    skip = (page - 1) * size

    employees, total = await service.list_employees(
        department=department, skip=skip, limit=size
    )

    return {
        "items": employees,
        "total": total,
        "page": page,
        "size": size,
    }


@router.patch("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: UUID,
    employee_data: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("employees:update")),
):
    """Update employee information."""
    service = HRService(db)

    update_data = {k: v for k, v in employee_data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    employee = await service.update_employee(
        employee_id, user_id=current_user.id, **update_data
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )

    return employee
