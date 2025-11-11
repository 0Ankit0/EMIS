"""Teacher Hierarchy API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from src.database import get_db
from src.services.teacher_hierarchy_service import TeacherHierarchyService
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/hr/hierarchy", tags=["teacher-hierarchy"])


class HierarchyCreate(BaseModel):
    teacher_id: int
    designation: str
    department_id: Optional[int] = None
    reports_to: Optional[int] = None
    is_department_head: bool = False
    is_program_coordinator: bool = False
    program_id: Optional[int] = None
    subject_coordinator_ids: Optional[List[int]] = None
    effective_from: Optional[date] = None


class HierarchyResponse(BaseModel):
    id: int
    teacher_id: int
    designation: str
    department_id: Optional[int]
    reports_to: Optional[int]
    hierarchy_level: int
    is_department_head: bool
    is_program_coordinator: bool
    effective_from: date
    effective_to: Optional[date]
    
    class Config:
        from_attributes = True


class DepartmentHierarchyCreate(BaseModel):
    department_id: int
    parent_department_id: Optional[int] = None
    head_of_department_id: Optional[int] = None
    annual_budget: Optional[float] = None


@router.post("/teachers", response_model=HierarchyResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher_hierarchy(
    hierarchy_data: HierarchyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:admin"]))
):
    """Create or update teacher hierarchy"""
    service = TeacherHierarchyService(db)
    
    hierarchy = await service.set_teacher_hierarchy(**hierarchy_data.dict())
    return hierarchy


@router.get("/teachers/{teacher_id}", response_model=HierarchyResponse)
async def get_teacher_hierarchy(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:read"]))
):
    """Get teacher hierarchy information"""
    service = TeacherHierarchyService(db)
    hierarchy = await service.get_teacher_hierarchy(teacher_id)
    
    if not hierarchy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hierarchy not found for teacher {teacher_id}"
        )
    
    return hierarchy


@router.get("/departments/{department_id}")
async def get_department_hierarchy(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:read"]))
):
    """Get department hierarchy tree"""
    service = TeacherHierarchyService(db)
    hierarchy = await service.get_department_hierarchy(department_id)
    
    return {
        "department_id": department_id,
        "hierarchy": hierarchy
    }


@router.get("/org-chart")
async def get_organization_chart(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:read"]))
):
    """Get complete organization chart"""
    service = TeacherHierarchyService(db)
    org_chart = await service.get_org_chart()
    return org_chart


@router.get("/teachers/{teacher_id}/subordinates", response_model=List[HierarchyResponse])
async def get_subordinates(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:read"]))
):
    """Get all subordinates of a teacher"""
    service = TeacherHierarchyService(db)
    subordinates = await service.get_subordinates(teacher_id)
    return subordinates


@router.get("/designation/{designation}", response_model=List[HierarchyResponse])
async def get_by_designation(
    designation: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:read"]))
):
    """Get all teachers with specific designation"""
    service = TeacherHierarchyService(db)
    teachers = await service.get_teachers_by_designation(designation)
    return teachers


@router.get("/department-heads", response_model=List[HierarchyResponse])
async def get_department_heads(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:read"]))
):
    """Get all department heads"""
    service = TeacherHierarchyService(db)
    heads = await service.get_department_heads()
    return heads


@router.post("/departments")
async def create_department_hierarchy(
    dept_data: DepartmentHierarchyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hr:admin"]))
):
    """Create or update department hierarchy"""
    service = TeacherHierarchyService(db)
    
    dept_hierarchy = await service.set_department_hierarchy(**dept_data.dict())
    
    return {
        "id": dept_hierarchy.id,
        "department_id": dept_hierarchy.department_id,
        "hierarchy_level": dept_hierarchy.hierarchy_level,
        "head_of_department_id": dept_hierarchy.head_of_department_id
    }
