"""Student service for EMIS - handles student lifecycle operations."""
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student, StudentStatus
from src.models.enrollment import Enrollment
from src.models.academic_record import AcademicRecord
from src.models.attendance import Attendance
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger


logger = get_logger(__name__)


class StudentService:
    """Service for managing student lifecycle operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_student(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_of_birth: date,
        phone: Optional[str] = None,
        middle_name: Optional[str] = None,
        gender: Optional[str] = None,
        nationality: Optional[str] = None,
        address: Optional[str] = None,
        user_id: Optional[UUID] = None,
    ) -> Student:
        """Create a new student record."""
        # Generate unique student number
        student_number = await self._generate_student_number()

        student = Student(
            student_number=student_number,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            nationality=nationality,
            address=address,
            user_id=user_id,
            status=StudentStatus.APPLICANT,
        )

        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.CREATE,
            resource="student",
            resource_id=str(student.id),
            details={"student_number": student_number, "email": email},
        )

        logger.info(f"Created student: {student.id} - {student.student_number}")
        return student

    async def get_student_by_id(self, student_id: UUID) -> Optional[Student]:
        """Get student by ID."""
        result = await self.db.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()

    async def get_student_by_email(self, email: str) -> Optional[Student]:
        """Get student by email."""
        result = await self.db.execute(select(Student).where(Student.email == email))
        return result.scalar_one_or_none()

    async def get_student_by_number(self, student_number: str) -> Optional[Student]:
        """Get student by student number."""
        result = await self.db.execute(
            select(Student).where(Student.student_number == student_number)
        )
        return result.scalar_one_or_none()

    async def list_students(
        self,
        status: Optional[StudentStatus] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[Student], int]:
        """List students with pagination."""
        query = select(Student)

        if status:
            query = query.where(Student.status == status)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Student.created_at.desc())
        result = await self.db.execute(query)
        students = list(result.scalars().all())

        return students, total

    async def update_student(
        self, student_id: UUID, user_id: Optional[UUID] = None, **kwargs
    ) -> Optional[Student]:
        """Update student information."""
        student = await self.get_student_by_id(student_id)
        if not student:
            return None

        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)

        await self.db.commit()
        await self.db.refresh(student)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="student",
            resource_id=str(student.id),
            details={"updated_fields": list(kwargs.keys())},
        )

        logger.info(f"Updated student: {student.id}")
        return student

    async def update_student_status(
        self, student_id: UUID, status: StudentStatus, user_id: Optional[UUID] = None
    ) -> Optional[Student]:
        """Update student status."""
        student = await self.get_student_by_id(student_id)
        if not student:
            return None

        old_status = student.status
        student.status = status

        await self.db.commit()
        await self.db.refresh(student)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="student",
            resource_id=str(student.id),
            details={"old_status": old_status.value, "new_status": status.value},
        )

        logger.info(f"Updated student status: {student.id} - {old_status} -> {status}")
        return student

    async def get_student_enrollments(self, student_id: UUID) -> List[Enrollment]:
        """Get all enrollments for a student."""
        result = await self.db.execute(
            select(Enrollment)
            .where(Enrollment.student_id == student_id)
            .order_by(Enrollment.enrollment_date.desc())
        )
        return list(result.scalars().all())

    async def get_student_academic_records(
        self, student_id: UUID, academic_year: Optional[str] = None
    ) -> List[AcademicRecord]:
        """Get academic records for a student."""
        query = select(AcademicRecord).where(AcademicRecord.student_id == student_id)

        if academic_year:
            query = query.where(AcademicRecord.academic_year == academic_year)

        result = await self.db.execute(query.order_by(AcademicRecord.created_at.desc()))
        return list(result.scalars().all())

    async def get_student_attendance(
        self,
        student_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Attendance]:
        """Get attendance records for a student."""
        query = select(Attendance).where(Attendance.student_id == student_id)

        if start_date:
            query = query.where(Attendance.date >= start_date)
        if end_date:
            query = query.where(Attendance.date <= end_date)

        result = await self.db.execute(query.order_by(Attendance.date.desc()))
        return list(result.scalars().all())

    async def calculate_gpa(self, student_id: UUID) -> Optional[float]:
        """Calculate cumulative GPA for a student."""
        records = await self.get_student_academic_records(student_id)

        if not records:
            return None

        total_points = 0.0
        total_credits = 0

        for record in records:
            if record.grade_points is not None and record.credits:
                total_points += record.grade_points * record.credits
                total_credits += record.credits

        if total_credits == 0:
            return None

        return round(total_points / total_credits, 2)

    async def _generate_student_number(self) -> str:
        """Generate unique student number."""
        year = datetime.now().year
        # Get count of students created this year
        result = await self.db.execute(
            select(func.count())
            .select_from(Student)
            .where(func.extract("year", Student.created_at) == year)
        )
        count = result.scalar_one()
        # Format: YEAR + 5-digit sequential number
        return f"{year}{count + 1:05d}"

    async def delete_student(
        self, student_id: UUID, user_id: Optional[UUID] = None
    ) -> bool:
        """Soft delete a student (set status to deleted)."""
        student = await self.get_student_by_id(student_id)
        if not student:
            return False

        student.status = StudentStatus.WITHDRAWN
        await self.db.commit()

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.DELETE,
            resource="student",
            resource_id=str(student.id),
        )

        logger.info(f"Deleted student: {student.id}")
        return True
