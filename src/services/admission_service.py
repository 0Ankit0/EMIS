"""Admission service for EMIS."""
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.admission import Application, ApplicationStatus
from src.models.finance import Program
from src.models.student import Student, StudentStatus
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger

logger = get_logger(__name__)


class AdmissionService:
    """Service for managing admissions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_application(
        self,
        program_id: UUID,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        date_of_birth: date,
        academic_year: str,
        previous_education: Optional[dict] = None,
        documents: Optional[dict] = None,
        middle_name: Optional[str] = None,
        gender: Optional[str] = None,
        nationality: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Application:
        """Create a new admission application."""
        # Verify program exists
        result = await self.db.execute(
            select(Program).where(Program.id == program_id)
        )
        if not result.scalar_one_or_none():
            raise ValueError(f"Program {program_id} not found")

        # Generate application number
        application_number = await self._generate_application_number(academic_year)

        application = Application(
            application_number=application_number,
            program_id=program_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            nationality=nationality,
            address=address,
            academic_year=academic_year,
            application_date=date.today(),
            status=ApplicationStatus.SUBMITTED,
            previous_education=previous_education,
            documents=documents,
        )

        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Application",
            entity_id=application.id,
            details={
                "application_number": application_number,
                "email": email,
                "program_id": str(program_id)
            }
        )

        logger.info(f"Application created: {application_number}")
        return application

    async def update_application_status(
        self,
        application_id: UUID,
        status: ApplicationStatus,
        reviewed_by: Optional[UUID] = None,
        comments: Optional[str] = None,
    ) -> Application:
        """Update application status."""
        result = await self.db.execute(
            select(Application).where(Application.id == application_id)
        )
        application = result.scalar_one_or_none()

        if not application:
            raise ValueError(f"Application {application_id} not found")

        old_status = application.status
        application.status = status

        if reviewed_by:
            application.reviewed_by = reviewed_by
            application.review_date = date.today()

        if comments:
            application.comments = comments

        await self.db.commit()
        await self.db.refresh(application)

        await log_audit(
            self.db,
            action=AuditAction.UPDATE,
            entity_type="Application",
            entity_id=application.id,
            user_id=reviewed_by,
            details={
                "old_status": old_status.value,
                "new_status": status.value,
                "application_number": application.application_number
            }
        )

        logger.info(f"Application {application.application_number} status: {old_status} -> {status}")
        return application

    async def approve_application(
        self,
        application_id: UUID,
        reviewed_by: UUID,
        create_student: bool = True,
    ) -> tuple[Application, Optional[Student]]:
        """Approve an application and optionally create student record."""
        application = await self.update_application_status(
            application_id,
            ApplicationStatus.APPROVED,
            reviewed_by=reviewed_by
        )

        student = None
        if create_student:
            student = await self._create_student_from_application(application)
            application.student_id = student.id
            await self.db.commit()

        return application, student

    async def reject_application(
        self,
        application_id: UUID,
        reviewed_by: UUID,
        rejection_reason: str,
    ) -> Application:
        """Reject an application."""
        return await self.update_application_status(
            application_id,
            ApplicationStatus.REJECTED,
            reviewed_by=reviewed_by,
            comments=rejection_reason
        )

    async def schedule_interview(
        self,
        application_id: UUID,
        interview_date: datetime,
        interviewer_id: Optional[UUID] = None,
    ) -> Application:
        """Schedule an interview for an application."""
        result = await self.db.execute(
            select(Application).where(Application.id == application_id)
        )
        application = result.scalar_one_or_none()

        if not application:
            raise ValueError(f"Application {application_id} not found")

        application.status = ApplicationStatus.INTERVIEW_SCHEDULED
        application.interview_date = interview_date

        await self.db.commit()
        await self.db.refresh(application)

        await log_audit(
            self.db,
            action=AuditAction.UPDATE,
            entity_type="Application",
            entity_id=application.id,
            user_id=interviewer_id,
            details={
                "interview_date": interview_date.isoformat(),
                "application_number": application.application_number
            }
        )

        logger.info(f"Interview scheduled for application {application.application_number}")
        return application

    async def get_applications_by_status(
        self,
        status: ApplicationStatus,
        academic_year: Optional[str] = None,
    ) -> List[Application]:
        """Get applications by status."""
        query = select(Application).where(Application.status == status)

        if academic_year:
            query = query.where(Application.academic_year == academic_year)

        query = query.order_by(Application.application_date.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _generate_application_number(self, academic_year: str) -> str:
        """Generate unique application number."""
        year_code = academic_year.split("-")[0][2:]  # Last 2 digits of start year
        
        # Get count of applications this year
        result = await self.db.execute(
            select(Application).where(Application.academic_year == academic_year)
        )
        count = len(list(result.scalars().all())) + 1

        return f"APP{year_code}{count:05d}"

    async def _create_student_from_application(self, application: Application) -> Student:
        """Create a student record from an approved application."""
        from src.services.student_service import StudentService

        student_service = StudentService(self.db)
        
        student = await student_service.create_student(
            first_name=application.first_name,
            last_name=application.last_name,
            email=application.email,
            phone=application.phone,
            date_of_birth=application.date_of_birth,
            middle_name=application.middle_name,
            gender=application.gender,
            nationality=application.nationality,
            address=application.address,
        )

        # Set program
        student.program_id = application.program_id
        student.admission_date = application.admission_date or date.today()
        student.status = StudentStatus.ACTIVE

        await self.db.commit()
        await self.db.refresh(student)

        logger.info(f"Student {student.student_number} created from application {application.application_number}")
        return student
