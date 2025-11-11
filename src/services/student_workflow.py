"""Student workflow service - handles admission, enrollment, graduation, and alumni workflows."""
from datetime import datetime, date
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student, StudentStatus
from src.models.enrollment import Enrollment, EnrollmentStatus
from src.services.student_service import StudentService
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger


logger = get_logger(__name__)


class StudentWorkflowService:
    """Service for managing student lifecycle workflows."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.student_service = StudentService(db)

    async def admit_student(
        self,
        student_id: UUID,
        admission_date: Optional[datetime] = None,
        user_id: Optional[UUID] = None,
    ) -> Optional[Student]:
        """
        Admit a student (transition from APPLICANT to ACTIVE).

        Args:
            student_id: Student ID
            admission_date: Date of admission (defaults to now)
            user_id: User performing the action

        Returns:
            Updated student or None if not found
        """
        student = await self.student_service.get_student_by_id(student_id)
        if not student:
            return None

        if student.status != StudentStatus.APPLICANT:
            logger.warning(
                f"Cannot admit student {student_id}: current status is {student.status}"
            )
            return None

        student.status = StudentStatus.ACTIVE
        student.admission_date = admission_date or datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(student)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="student_admission",
            resource_id=str(student.id),
            details={"action": "admitted", "admission_date": str(student.admission_date)},
        )

        logger.info(f"Admitted student: {student.id} - {student.student_number}")
        return student

    async def enroll_student(
        self,
        student_id: UUID,
        program_id: UUID,
        academic_year: str,
        semester: str,
        enrollment_date: date,
        enrollment_type: str = "full-time",
        credits_enrolled: Optional[int] = None,
        user_id: Optional[UUID] = None,
    ) -> Optional[Enrollment]:
        """
        Enroll a student in a program.

        Args:
            student_id: Student ID
            program_id: Program ID
            academic_year: Academic year (e.g., "2024-2025")
            semester: Semester (e.g., "Fall 2024")
            enrollment_date: Date of enrollment
            enrollment_type: Type of enrollment (full-time, part-time)
            credits_enrolled: Number of credits
            user_id: User performing the action

        Returns:
            Created enrollment or None
        """
        student = await self.student_service.get_student_by_id(student_id)
        if not student:
            return None

        if student.status not in [StudentStatus.ACTIVE, StudentStatus.APPLICANT]:
            logger.warning(
                f"Cannot enroll student {student_id}: current status is {student.status}"
            )
            return None

        # If student is still an applicant, admit them first
        if student.status == StudentStatus.APPLICANT:
            await self.admit_student(student_id, datetime.utcnow(), user_id)

        enrollment = Enrollment(
            student_id=student_id,
            program_id=program_id,
            academic_year=academic_year,
            semester=semester,
            enrollment_date=enrollment_date,
            enrollment_type=enrollment_type,
            credits_enrolled=credits_enrolled,
            status=EnrollmentStatus.ACTIVE,
        )

        self.db.add(enrollment)
        await self.db.commit()
        await self.db.refresh(enrollment)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.CREATE,
            resource="enrollment",
            resource_id=str(enrollment.id),
            details={
                "student_id": str(student_id),
                "program_id": str(program_id),
                "academic_year": academic_year,
                "semester": semester,
            },
        )

        logger.info(f"Enrolled student: {student_id} in {program_id} for {semester}")
        return enrollment

    async def suspend_enrollment(
        self,
        enrollment_id: UUID,
        reason: str,
        user_id: Optional[UUID] = None,
    ) -> Optional[Enrollment]:
        """Suspend a student's enrollment."""
        result = await self.db.get(Enrollment, enrollment_id)
        enrollment = result

        if not enrollment:
            return None

        enrollment.status = EnrollmentStatus.SUSPENDED
        enrollment.notes = f"Suspended: {reason}"

        await self.db.commit()
        await self.db.refresh(enrollment)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="enrollment",
            resource_id=str(enrollment.id),
            details={"action": "suspended", "reason": reason},
        )

        logger.info(f"Suspended enrollment: {enrollment_id}")
        return enrollment

    async def withdraw_enrollment(
        self,
        enrollment_id: UUID,
        withdrawal_date: date,
        reason: str,
        user_id: Optional[UUID] = None,
    ) -> Optional[Enrollment]:
        """Withdraw a student from enrollment."""
        result = await self.db.get(Enrollment, enrollment_id)
        enrollment = result

        if not enrollment:
            return None

        enrollment.status = EnrollmentStatus.WITHDRAWN
        enrollment.withdrawal_date = withdrawal_date
        enrollment.withdrawal_reason = reason
        enrollment.end_date = withdrawal_date

        await self.db.commit()
        await self.db.refresh(enrollment)

        # Update student status if all enrollments are withdrawn
        student = await self.student_service.get_student_by_id(enrollment.student_id)
        if student:
            active_enrollments = await self.student_service.get_student_enrollments(
                enrollment.student_id
            )
            all_withdrawn = all(
                e.status == EnrollmentStatus.WITHDRAWN for e in active_enrollments
            )
            if all_withdrawn:
                await self.student_service.update_student_status(
                    enrollment.student_id, StudentStatus.WITHDRAWN, user_id
                )

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="enrollment",
            resource_id=str(enrollment.id),
            details={
                "action": "withdrawn",
                "withdrawal_date": str(withdrawal_date),
                "reason": reason,
            },
        )

        logger.info(f"Withdrew enrollment: {enrollment_id}")
        return enrollment

    async def graduate_student(
        self,
        student_id: UUID,
        graduation_date: datetime,
        degree_earned: str,
        honors: Optional[str] = None,
        user_id: Optional[UUID] = None,
    ) -> Optional[Student]:
        """
        Graduate a student.

        Args:
            student_id: Student ID
            graduation_date: Date of graduation
            degree_earned: Degree/certificate earned
            honors: Honors designation (e.g., "Magna Cum Laude")
            user_id: User performing the action

        Returns:
            Updated student or None
        """
        student = await self.student_service.get_student_by_id(student_id)
        if not student:
            return None

        if student.status != StudentStatus.ACTIVE:
            logger.warning(
                f"Cannot graduate student {student_id}: current status is {student.status}"
            )
            return None

        student.status = StudentStatus.GRADUATED
        student.graduation_date = graduation_date
        student.degree_earned = degree_earned
        student.honors = honors

        await self.db.commit()
        await self.db.refresh(student)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="student_graduation",
            resource_id=str(student.id),
            details={
                "action": "graduated",
                "graduation_date": str(graduation_date),
                "degree": degree_earned,
                "honors": honors,
            },
        )

        logger.info(f"Graduated student: {student.id} - {degree_earned}")
        return student

    async def convert_to_alumni(
        self, student_id: UUID, user_id: Optional[UUID] = None
    ) -> Optional[Student]:
        """
        Convert a graduated student to alumni status.

        Args:
            student_id: Student ID
            user_id: User performing the action

        Returns:
            Updated student or None
        """
        student = await self.student_service.get_student_by_id(student_id)
        if not student:
            return None

        if student.status != StudentStatus.GRADUATED:
            logger.warning(
                f"Cannot convert to alumni: student {student_id} status is {student.status}"
            )
            return None

        student.status = StudentStatus.ALUMNI

        await self.db.commit()
        await self.db.refresh(student)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="student_alumni",
            resource_id=str(student.id),
            details={"action": "converted_to_alumni"},
        )

        logger.info(f"Converted student to alumni: {student.id}")
        return student

    async def reactivate_enrollment(
        self,
        enrollment_id: UUID,
        reason: str,
        user_id: Optional[UUID] = None,
    ) -> Optional[Enrollment]:
        """Reactivate a suspended enrollment."""
        result = await self.db.get(Enrollment, enrollment_id)
        enrollment = result

        if not enrollment:
            return None

        if enrollment.status != EnrollmentStatus.SUSPENDED:
            logger.warning(
                f"Cannot reactivate enrollment {enrollment_id}: status is {enrollment.status}"
            )
            return None

        enrollment.status = EnrollmentStatus.ACTIVE
        enrollment.notes = f"Reactivated: {reason}"

        await self.db.commit()
        await self.db.refresh(enrollment)

        await log_audit(
            self.db,
            user_id=user_id,
            action=AuditAction.UPDATE,
            resource="enrollment",
            resource_id=str(enrollment.id),
            details={"action": "reactivated", "reason": reason},
        )

        logger.info(f"Reactivated enrollment: {enrollment_id}")
        return enrollment
