"""HR service for managing employee operations."""
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.employee import Employee, EmployeeStatus
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger

logger = get_logger(__name__)


class HRService:
    """Service for managing HR operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_employee(
        self,
        employee_number: str,
        first_name: str,
        last_name: str,
        email: str,
        date_of_joining: date,
        department: str,
        designation: str,
        employment_type: str,
        basic_salary: Optional[float] = None,
        user_id: Optional[UUID] = None,
    ) -> Employee:
        """Create a new employee record."""
        employee = Employee(
            employee_number=employee_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_joining=date_of_joining,
            department=department,
            designation=designation,
            employment_type=employment_type,
            basic_salary=basic_salary,
            status=EmployeeStatus.ACTIVE,
        )

        self.db.add(employee)
        await self.db.commit()
        await self.db.refresh(employee)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.CREATE,
            resource="employee",
            resource_id=str(employee.id),
            details={"employee_number": employee_number, "email": email},
        )

        logger.info(f"Created employee: {employee.id} - {employee.employee_number}")
        return employee

    async def get_employee_by_id(self, employee_id: UUID) -> Optional[Employee]:
        """Get employee by ID."""
        result = await self.db.execute(select(Employee).where(Employee.id == employee_id))
        return result.scalar_one_or_none()

    async def list_employees(
        self, department: Optional[str] = None, skip: int = 0, limit: int = 20
    ) -> tuple[List[Employee], int]:
        """List employees with pagination."""
        query = select(Employee)

        if department:
            query = query.where(Employee.department == department)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        query = query.offset(skip).limit(limit).order_by(Employee.created_at.desc())
        result = await self.db.execute(query)
        employees = list(result.scalars().all())

        return employees, total

    async def update_employee(
        self, employee_id: UUID, user_id: Optional[UUID] = None, **kwargs
    ) -> Optional[Employee]:
        """Update employee information."""
        employee = await self.get_employee_by_id(employee_id)
        if not employee:
            return None

        for key, value in kwargs.items():
            if hasattr(employee, key):
                setattr(employee, key, value)

        await self.db.commit()
        await self.db.refresh(employee)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="employee",
            resource_id=str(employee.id),
            details={"updated_fields": list(kwargs.keys())},
        )

        logger.info(f"Updated employee: {employee.id}")
        return employee
