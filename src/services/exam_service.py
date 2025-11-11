"""Exam Service for managing examinations"""
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.exam import Exam, ExamType, ExamStatus
from src.lib.audit import audit_log


class ExamService:
    """Service for managing examinations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_exam(
        self,
        course_id: int,
        exam_name: str,
        exam_type: ExamType,
        exam_code: str,
        exam_date: date,
        start_time: datetime,
        end_time: datetime,
        duration_minutes: int,
        max_marks: float,
        passing_marks: float,
        weightage_percentage: float = 100.0,
        venue: Optional[str] = None,
        room_number: Optional[str] = None,
        instructions: Optional[str] = None,
        syllabus_topics: Optional[str] = None,
        created_by: Optional[int] = None
    ) -> Exam:
        """Create a new exam"""
        exam = Exam(
            course_id=course_id,
            exam_name=exam_name,
            exam_type=exam_type,
            exam_code=exam_code,
            exam_date=exam_date,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_minutes,
            max_marks=max_marks,
            passing_marks=passing_marks,
            weightage_percentage=weightage_percentage,
            venue=venue,
            room_number=room_number,
            instructions=instructions,
            syllabus_topics=syllabus_topics,
            created_by=created_by
        )
        
        self.db.add(exam)
        await self.db.commit()
        await self.db.refresh(exam)
        
        await audit_log(
            self.db,
            action="create_exam",
            entity_type="exam",
            entity_id=exam.id,
            user_id=created_by,
            details={"exam_code": exam_code, "exam_type": exam_type.value, "course_id": course_id}
        )
        
        return exam
    
    async def get_exam_by_id(self, exam_id: int) -> Optional[Exam]:
        """Get an exam by ID"""
        result = await self.db.execute(
            select(Exam).where(Exam.id == exam_id)
        )
        return result.scalar_one_or_none()
    
    async def get_exam_by_code(self, exam_code: str) -> Optional[Exam]:
        """Get an exam by code"""
        result = await self.db.execute(
            select(Exam).where(Exam.exam_code == exam_code)
        )
        return result.scalar_one_or_none()
    
    async def get_exams_by_course(self, course_id: int, active_only: bool = True) -> List[Exam]:
        """Get all exams for a course"""
        query = select(Exam).where(Exam.course_id == course_id)
        
        if active_only:
            query = query.where(Exam.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_exams_by_type(self, exam_type: ExamType, active_only: bool = True) -> List[Exam]:
        """Get all exams of a specific type"""
        query = select(Exam).where(Exam.exam_type == exam_type)
        
        if active_only:
            query = query.where(Exam.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_exams_by_date_range(
        self,
        start_date: date,
        end_date: date,
        active_only: bool = True
    ) -> List[Exam]:
        """Get all exams within a date range"""
        query = select(Exam).where(
            and_(
                Exam.exam_date >= start_date,
                Exam.exam_date <= end_date
            )
        )
        
        if active_only:
            query = query.where(Exam.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_upcoming_exams(self, days: int = 7, active_only: bool = True) -> List[Exam]:
        """Get upcoming exams within specified days"""
        today = date.today()
        from datetime import timedelta
        end_date = today + timedelta(days=days)
        
        return await self.get_exams_by_date_range(today, end_date, active_only)
    
    async def update_exam(
        self,
        exam_id: int,
        updates: dict,
        user_id: Optional[int] = None
    ) -> Optional[Exam]:
        """Update an exam"""
        exam = await self.get_exam_by_id(exam_id)
        if not exam:
            return None
        
        for key, value in updates.items():
            if hasattr(exam, key) and key not in ['id', 'exam_code', 'created_at', 'created_by']:
                setattr(exam, key, value)
        
        await self.db.commit()
        await self.db.refresh(exam)
        
        await audit_log(
            self.db,
            action="update_exam",
            entity_type="exam",
            entity_id=exam_id,
            user_id=user_id,
            details=updates
        )
        
        return exam
    
    async def update_exam_status(
        self,
        exam_id: int,
        status: ExamStatus,
        user_id: Optional[int] = None
    ) -> Optional[Exam]:
        """Update exam status"""
        return await self.update_exam(exam_id, {"status": status}, user_id)
    
    async def cancel_exam(self, exam_id: int, user_id: Optional[int] = None) -> bool:
        """Cancel an exam"""
        exam = await self.update_exam_status(exam_id, ExamStatus.CANCELLED, user_id)
        return exam is not None
    
    async def delete_exam(self, exam_id: int, user_id: Optional[int] = None) -> bool:
        """Delete an exam (soft delete by deactivating)"""
        exam = await self.get_exam_by_id(exam_id)
        if not exam:
            return False
        
        exam.is_active = False
        await self.db.commit()
        
        await audit_log(
            self.db,
            action="delete_exam",
            entity_type="exam",
            entity_id=exam_id,
            user_id=user_id
        )
        
        return True


# T053: Exam routine creation and management
async def create_exam_routine(
    self,
    routine_name: str,
    routine_code: str,
    academic_year: str,
    semester: int,
    exam_type: ExamType,
    start_date: date,
    end_date: date,
    created_by: int,
    **kwargs
) -> ExamRoutine:
    """Create exam routine/timetable"""
    from src.models.exam import ExamRoutine
    
    routine = ExamRoutine(
        routine_name=routine_name,
        routine_code=routine_code,
        academic_year=academic_year,
        semester=semester,
        exam_type=exam_type,
        start_date=start_date,
        end_date=end_date,
        created_by=created_by,
        **kwargs
    )
    
    self.db.add(routine)
    await self.db.commit()
    await self.db.refresh(routine)
    
    logger.info(f"Created exam routine: {routine_name} ({routine_code})")
    
    return routine


async def add_exam_to_routine(
    self,
    routine_id: int,
    exam_id: int,
    exam_date: date,
    start_time: datetime,
    end_time: datetime,
    duration_minutes: int,
    venue: str,
    **kwargs
) -> 'ExamRoutineSlot':
    """Add exam slot to routine"""
    from src.models.exam import ExamRoutineSlot
    
    slot = ExamRoutineSlot(
        routine_id=routine_id,
        exam_id=exam_id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        duration_minutes=duration_minutes,
        venue=venue,
        **kwargs
    )
    
    self.db.add(slot)
    await self.db.commit()
    await self.db.refresh(slot)
    
    logger.info(f"Added exam {exam_id} to routine {routine_id} on {exam_date}")
    
    return slot


async def publish_exam_routine(
    self,
    routine_id: int,
    published_by: int
) -> ExamRoutine:
    """Publish exam routine for students"""
    from src.models.exam import ExamRoutine
    
    result = await self.db.execute(
        select(ExamRoutine).where(ExamRoutine.id == routine_id)
    )
    routine = result.scalar_one_or_none()
    
    if not routine:
        raise ValueError(f"Exam routine {routine_id} not found")
    
    routine.is_published = True
    routine.published_at = datetime.utcnow()
    routine.published_by = published_by
    
    await self.db.commit()
    await self.db.refresh(routine)
    
    logger.info(f"Published exam routine {routine_id}")
    
    return routine


async def get_exam_routine(
    self,
    academic_year: str,
    semester: int,
    exam_type: Optional[ExamType] = None
) -> List[ExamRoutine]:
    """Get exam routines"""
    from src.models.exam import ExamRoutine
    
    query = select(ExamRoutine).where(
        and_(
            ExamRoutine.academic_year == academic_year,
            ExamRoutine.semester == semester
        )
    )
    
    if exam_type:
        query = query.where(ExamRoutine.exam_type == exam_type)
    
    result = await self.db.execute(query)
    return result.scalars().all()


# T054: Exam form submission workflow
async def create_exam_form(
    self,
    student_id: int,
    routine_id: int,
    academic_year: str,
    semester: int,
    registered_courses: List[int],
    program_id: Optional[int] = None
) -> 'ExamForm':
    """Student creates exam form"""
    from src.models.exam import ExamForm
    import json
    
    # Generate form number
    form_number = await self.generate_exam_form_number(academic_year, semester)
    
    exam_form = ExamForm(
        form_number=form_number,
        student_id=student_id,
        routine_id=routine_id,
        academic_year=academic_year,
        semester=semester,
        program_id=program_id,
        registered_courses=json.dumps(registered_courses)
    )
    
    self.db.add(exam_form)
    await self.db.commit()
    await self.db.refresh(exam_form)
    
    logger.info(f"Created exam form {form_number} for student {student_id}")
    
    return exam_form


async def generate_exam_form_number(
    self,
    academic_year: str,
    semester: int
) -> str:
    """Generate unique exam form number"""
    from src.models.exam import ExamForm
    
    year_code = academic_year.split("-")[0][-2:]  # Last 2 digits of year
    
    result = await self.db.execute(
        select(func.count(ExamForm.id)).where(
            ExamForm.form_number.like(f"EF{year_code}{semester}%")
        )
    )
    count = result.scalar() or 0
    sequence = str(count + 1).zfill(5)
    
    return f"EF{year_code}{semester}{sequence}"


async def submit_exam_form(
    self,
    form_id: int,
    declaration_accepted: bool
) -> 'ExamForm':
    """Student submits exam form for verification"""
    from src.models.exam import ExamForm, ExamFormStatus
    
    result = await self.db.execute(
        select(ExamForm).where(ExamForm.id == form_id)
    )
    exam_form = result.scalar_one_or_none()
    
    if not exam_form:
        raise ValueError(f"Exam form {form_id} not found")
    
    if not declaration_accepted:
        raise ValueError("Student must accept the declaration")
    
    exam_form.status = ExamFormStatus.SUBMITTED
    exam_form.declaration_accepted = declaration_accepted
    exam_form.declaration_date = datetime.utcnow()
    exam_form.submitted_at = datetime.utcnow()
    
    await self.db.commit()
    await self.db.refresh(exam_form)
    
    logger.info(f"Exam form {exam_form.form_number} submitted")
    
    return exam_form


async def verify_exam_form(
    self,
    form_id: int,
    verified_by: int,
    verification_remarks: Optional[str] = None
) -> 'ExamForm':
    """Verify exam form"""
    from src.models.exam import ExamForm, ExamFormStatus
    
    result = await self.db.execute(
        select(ExamForm).where(ExamForm.id == form_id)
    )
    exam_form = result.scalar_one_or_none()
    
    if not exam_form:
        raise ValueError(f"Exam form {form_id} not found")
    
    exam_form.status = ExamFormStatus.VERIFIED
    exam_form.verified_by = verified_by
    exam_form.verified_at = datetime.utcnow()
    exam_form.verification_remarks = verification_remarks
    
    await self.db.commit()
    await self.db.refresh(exam_form)
    
    logger.info(f"Exam form {exam_form.form_number} verified")
    
    return exam_form


async def approve_exam_form(
    self,
    form_id: int,
    approved_by: int,
    exam_fee_amount: float,
    approval_remarks: Optional[str] = None
) -> 'ExamForm':
    """Approve exam form and generate hall ticket"""
    from src.models.exam import ExamForm, ExamFormStatus
    
    result = await self.db.execute(
        select(ExamForm).where(ExamForm.id == form_id)
    )
    exam_form = result.scalar_one_or_none()
    
    if not exam_form:
        raise ValueError(f"Exam form {form_id} not found")
    
    exam_form.status = ExamFormStatus.APPROVED
    exam_form.approved_by = approved_by
    exam_form.approved_at = datetime.utcnow()
    exam_form.approval_remarks = approval_remarks
    exam_form.exam_fee_amount = exam_fee_amount
    
    # Generate hall ticket number
    exam_form.hall_ticket_number = await self.generate_hall_ticket_number(exam_form)
    exam_form.hall_ticket_generated_at = datetime.utcnow()
    
    await self.db.commit()
    await self.db.refresh(exam_form)
    
    logger.info(f"Exam form {exam_form.form_number} approved, hall ticket generated")
    
    return exam_form


async def generate_hall_ticket_number(
    self,
    exam_form: 'ExamForm'
) -> str:
    """Generate hall ticket number"""
    year_code = exam_form.academic_year.split("-")[0][-2:]
    return f"HT{year_code}{exam_form.semester}{str(exam_form.student_id).zfill(6)}"
