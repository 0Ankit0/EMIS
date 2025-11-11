"""Course service for EMIS."""
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.course import Course, Assignment, AssignmentSubmission
from src.models.enrollment import Enrollment
from src.models.student import Student
from src.models.employee import Employee
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger

logger = get_logger(__name__)


class CourseService:
    """Service for managing courses and assignments."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_course(
        self,
        course_code: str,
        course_name: str,
        credits: int,
        instructor_id: UUID,
        academic_year: str,
        semester: str,
        description: Optional[str] = None,
        syllabus: Optional[str] = None,
        max_students: Optional[int] = None,
    ) -> Course:
        """Create a new course."""
        # Verify instructor exists
        result = await self.db.execute(
            select(Employee).where(Employee.id == instructor_id)
        )
        if not result.scalar_one_or_none():
            raise ValueError(f"Instructor {instructor_id} not found")

        course = Course(
            course_code=course_code,
            course_name=course_name,
            description=description,
            credits=credits,
            instructor_id=instructor_id,
            academic_year=academic_year,
            semester=semester,
            syllabus=syllabus,
            max_students=max_students,
        )
        
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Course",
            entity_id=course.id,
            details={"course_code": course_code, "instructor_id": str(instructor_id)}
        )

        logger.info(f"Course created: {course_code}")
        return course

    async def enroll_student(self, student_id: UUID, course_id: UUID) -> Enrollment:
        """Enroll a student in a course."""
        # Verify student exists
        student_result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        student = student_result.scalar_one_or_none()
        if not student:
            raise ValueError(f"Student {student_id} not found")

        # Verify course exists
        course_result = await self.db.execute(
            select(Course).where(Course.id == course_id)
        )
        course = course_result.scalar_one_or_none()
        if not course:
            raise ValueError(f"Course {course_id} not found")

        # Check if already enrolled
        existing_result = await self.db.execute(
            select(Enrollment).where(
                and_(
                    Enrollment.student_id == student_id,
                    Enrollment.course_id == course_id
                )
            )
        )
        if existing_result.scalar_one_or_none():
            raise ValueError("Student already enrolled in this course")

        # Check max students
        if course.max_students:
            count_result = await self.db.execute(
                select(func.count(Enrollment.id)).where(
                    Enrollment.course_id == course_id
                )
            )
            current_count = count_result.scalar()
            if current_count >= course.max_students:
                raise ValueError("Course is full")

        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
            enrollment_date=datetime.utcnow().date(),
            academic_year=course.academic_year,
            semester=course.semester,
            status="active"
        )

        self.db.add(enrollment)
        await self.db.commit()
        await self.db.refresh(enrollment)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Enrollment",
            entity_id=enrollment.id,
            user_id=student.user_id,
            details={
                "student_id": str(student_id),
                "course_id": str(course_id),
                "course_code": course.course_code
            }
        )

        logger.info(f"Student {student.student_number} enrolled in {course.course_code}")
        return enrollment

    async def create_assignment(
        self,
        course_id: UUID,
        title: str,
        description: str,
        due_date: datetime,
        max_marks: int,
        attachment_url: Optional[str] = None,
    ) -> Assignment:
        """Create a new assignment for a course."""
        # Verify course exists
        result = await self.db.execute(
            select(Course).where(Course.id == course_id)
        )
        course = result.scalar_one_or_none()
        if not course:
            raise ValueError(f"Course {course_id} not found")

        assignment = Assignment(
            course_id=course_id,
            title=title,
            description=description,
            due_date=due_date,
            max_marks=max_marks,
            attachment_url=attachment_url,
        )

        self.db.add(assignment)
        await self.db.commit()
        await self.db.refresh(assignment)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Assignment",
            entity_id=assignment.id,
            details={
                "course_id": str(course_id),
                "title": title,
                "due_date": due_date.isoformat()
            }
        )

        logger.info(f"Assignment created: {title} for course {course.course_code}")
        return assignment

    async def submit_assignment(
        self,
        assignment_id: UUID,
        student_id: UUID,
        submission_text: Optional[str] = None,
        attachment_url: Optional[str] = None,
    ) -> AssignmentSubmission:
        """Submit an assignment."""
        # Verify assignment exists
        assignment_result = await self.db.execute(
            select(Assignment).where(Assignment.id == assignment_id)
        )
        assignment = assignment_result.scalar_one_or_none()
        if not assignment:
            raise ValueError(f"Assignment {assignment_id} not found")

        # Verify student is enrolled in course
        enrollment_result = await self.db.execute(
            select(Enrollment).where(
                and_(
                    Enrollment.student_id == student_id,
                    Enrollment.course_id == assignment.course_id,
                    Enrollment.status == "active"
                )
            )
        )
        if not enrollment_result.scalar_one_or_none():
            raise ValueError("Student not enrolled in this course")

        # Check if already submitted
        existing_result = await self.db.execute(
            select(AssignmentSubmission).where(
                and_(
                    AssignmentSubmission.assignment_id == assignment_id,
                    AssignmentSubmission.student_id == student_id
                )
            )
        )
        existing_submission = existing_result.scalar_one_or_none()

        if existing_submission:
            # Update existing submission
            existing_submission.submission_text = submission_text
            existing_submission.attachment_url = attachment_url
            existing_submission.submitted_at = datetime.utcnow()
            existing_submission.status = "submitted"
            submission = existing_submission
        else:
            # Create new submission
            submission = AssignmentSubmission(
                assignment_id=assignment_id,
                student_id=student_id,
                submission_text=submission_text,
                attachment_url=attachment_url,
                submitted_at=datetime.utcnow(),
                status="submitted"
            )
            self.db.add(submission)

        await self.db.commit()
        await self.db.refresh(submission)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="AssignmentSubmission",
            entity_id=submission.id,
            user_id=student_id,
            details={
                "assignment_id": str(assignment_id),
                "student_id": str(student_id)
            }
        )

        logger.info(f"Assignment submitted by student {student_id}")
        return submission

    async def grade_assignment(
        self,
        submission_id: UUID,
        marks_obtained: int,
        feedback: Optional[str] = None,
        graded_by: Optional[UUID] = None,
    ) -> AssignmentSubmission:
        """Grade an assignment submission."""
        result = await self.db.execute(
            select(AssignmentSubmission)
            .options(selectinload(AssignmentSubmission.assignment))
            .where(AssignmentSubmission.id == submission_id)
        )
        submission = result.scalar_one_or_none()
        
        if not submission:
            raise ValueError(f"Submission {submission_id} not found")

        if marks_obtained > submission.assignment.max_marks:
            raise ValueError("Marks obtained cannot exceed maximum marks")

        submission.marks_obtained = marks_obtained
        submission.feedback = feedback
        submission.graded_at = datetime.utcnow()
        submission.graded_by = graded_by
        submission.status = "graded"

        await self.db.commit()
        await self.db.refresh(submission)

        await log_audit(
            self.db,
            action=AuditAction.UPDATE,
            entity_type="AssignmentSubmission",
            entity_id=submission.id,
            user_id=graded_by,
            details={
                "marks_obtained": marks_obtained,
                "max_marks": submission.assignment.max_marks
            }
        )

        logger.info(f"Assignment graded: {submission_id}")
        return submission

    async def get_course_students(self, course_id: UUID) -> List[Student]:
        """Get all students enrolled in a course."""
        result = await self.db.execute(
            select(Student)
            .join(Enrollment)
            .where(
                and_(
                    Enrollment.course_id == course_id,
                    Enrollment.status == "active"
                )
            )
        )
        return list(result.scalars().all())

    async def get_student_courses(self, student_id: UUID, academic_year: Optional[str] = None) -> List[Course]:
        """Get all courses a student is enrolled in."""
        query = (
            select(Course)
            .join(Enrollment)
            .where(
                and_(
                    Enrollment.student_id == student_id,
                    Enrollment.status == "active"
                )
            )
        )

        if academic_year:
            query = query.where(Course.academic_year == academic_year)

        result = await self.db.execute(query)
        return list(result.scalars().all())
