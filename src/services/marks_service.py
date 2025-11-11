"""Marks Service for managing student marks and evaluations"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.marks import Marks, MarksStatus, GradeType
from src.lib.audit import audit_log


class MarksService:
    """Service for managing student marks and evaluations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def calculate_grade(self, marks_obtained: float, max_marks: float) -> tuple[GradeType, float]:
        """Calculate grade and grade points based on marks percentage"""
        percentage = (marks_obtained / max_marks) * 100 if max_marks > 0 else 0
        
        if percentage >= 90:
            return GradeType.A_PLUS, 10.0
        elif percentage >= 80:
            return GradeType.A, 9.0
        elif percentage >= 70:
            return GradeType.B_PLUS, 8.0
        elif percentage >= 60:
            return GradeType.B, 7.0
        elif percentage >= 50:
            return GradeType.C_PLUS, 6.0
        elif percentage >= 40:
            return GradeType.C, 5.0
        elif percentage >= 33:
            return GradeType.D, 4.0
        else:
            return GradeType.F, 0.0
    
    async def create_marks(
        self,
        student_id: int,
        exam_id: int,
        enrollment_id: int,
        max_marks: float,
        marks_obtained: Optional[float] = None,
        is_absent: bool = False,
        remarks: Optional[str] = None,
        evaluator_id: Optional[int] = None
    ) -> Marks:
        """Create a new marks entry"""
        grade = None
        grade_points = None
        
        if marks_obtained is not None and not is_absent:
            grade, grade_points = self.calculate_grade(marks_obtained, max_marks)
        
        marks = Marks(
            student_id=student_id,
            exam_id=exam_id,
            enrollment_id=enrollment_id,
            marks_obtained=marks_obtained,
            max_marks=max_marks,
            grade=grade,
            grade_points=grade_points,
            is_absent=is_absent,
            remarks=remarks,
            status=MarksStatus.PENDING if marks_obtained is None else MarksStatus.SUBMITTED,
            evaluated_by=evaluator_id,
            evaluated_at=datetime.utcnow() if marks_obtained is not None else None
        )
        
        self.db.add(marks)
        await self.db.commit()
        await self.db.refresh(marks)
        
        await audit_log(
            self.db,
            action="create_marks",
            entity_type="marks",
            entity_id=marks.id,
            user_id=evaluator_id,
            details={"student_id": student_id, "exam_id": exam_id, "marks": marks_obtained}
        )
        
        return marks
    
    async def get_marks_by_id(self, marks_id: int) -> Optional[Marks]:
        """Get marks by ID"""
        result = await self.db.execute(
            select(Marks).where(Marks.id == marks_id)
        )
        return result.scalar_one_or_none()
    
    async def get_marks_by_student_exam(self, student_id: int, exam_id: int) -> Optional[Marks]:
        """Get marks for a specific student and exam"""
        result = await self.db.execute(
            select(Marks).where(
                and_(
                    Marks.student_id == student_id,
                    Marks.exam_id == exam_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_marks_by_student(self, student_id: int) -> List[Marks]:
        """Get all marks for a student"""
        result = await self.db.execute(
            select(Marks).where(Marks.student_id == student_id)
        )
        return list(result.scalars().all())
    
    async def get_marks_by_exam(self, exam_id: int) -> List[Marks]:
        """Get all marks for an exam"""
        result = await self.db.execute(
            select(Marks).where(Marks.exam_id == exam_id)
        )
        return list(result.scalars().all())
    
    async def get_marks_by_enrollment(self, enrollment_id: int) -> List[Marks]:
        """Get all marks for an enrollment"""
        result = await self.db.execute(
            select(Marks).where(Marks.enrollment_id == enrollment_id)
        )
        return list(result.scalars().all())
    
    async def update_marks(
        self,
        marks_id: int,
        marks_obtained: float,
        evaluator_comments: Optional[str] = None,
        evaluator_id: Optional[int] = None
    ) -> Optional[Marks]:
        """Update marks for a student"""
        marks = await self.get_marks_by_id(marks_id)
        if not marks:
            return None
        
        grade, grade_points = self.calculate_grade(marks_obtained, marks.max_marks)
        
        marks.marks_obtained = marks_obtained
        marks.grade = grade
        marks.grade_points = grade_points
        marks.evaluator_comments = evaluator_comments
        marks.evaluated_by = evaluator_id
        marks.evaluated_at = datetime.utcnow()
        marks.status = MarksStatus.SUBMITTED
        marks.is_absent = False
        
        await self.db.commit()
        await self.db.refresh(marks)
        
        await audit_log(
            self.db,
            action="update_marks",
            entity_type="marks",
            entity_id=marks_id,
            user_id=evaluator_id,
            details={"marks_obtained": marks_obtained, "grade": grade.value}
        )
        
        return marks
    
    async def verify_marks(
        self,
        marks_id: int,
        verifier_id: int
    ) -> Optional[Marks]:
        """Verify marks"""
        marks = await self.get_marks_by_id(marks_id)
        if not marks or marks.status != MarksStatus.SUBMITTED:
            return None
        
        marks.status = MarksStatus.VERIFIED
        marks.verified_by = verifier_id
        marks.verified_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(marks)
        
        await audit_log(
            self.db,
            action="verify_marks",
            entity_type="marks",
            entity_id=marks_id,
            user_id=verifier_id
        )
        
        return marks
    
    async def publish_marks(self, marks_id: int, user_id: Optional[int] = None) -> Optional[Marks]:
        """Publish marks to make them visible to students"""
        marks = await self.get_marks_by_id(marks_id)
        if not marks or marks.status != MarksStatus.VERIFIED:
            return None
        
        marks.status = MarksStatus.PUBLISHED
        marks.published_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(marks)
        
        await audit_log(
            self.db,
            action="publish_marks",
            entity_type="marks",
            entity_id=marks_id,
            user_id=user_id
        )
        
        return marks
    
    async def bulk_publish_marks(self, exam_id: int, user_id: Optional[int] = None) -> int:
        """Publish all verified marks for an exam"""
        marks_list = await self.get_marks_by_exam(exam_id)
        published_count = 0
        
        for marks in marks_list:
            if marks.status == MarksStatus.VERIFIED:
                marks.status = MarksStatus.PUBLISHED
                marks.published_at = datetime.utcnow()
                published_count += 1
        
        await self.db.commit()
        
        await audit_log(
            self.db,
            action="bulk_publish_marks",
            entity_type="exam",
            entity_id=exam_id,
            user_id=user_id,
            details={"published_count": published_count}
        )
        
        return published_count
    
    async def mark_absent(
        self,
        student_id: int,
        exam_id: int,
        enrollment_id: int,
        max_marks: float,
        user_id: Optional[int] = None
    ) -> Marks:
        """Mark a student as absent for an exam"""
        existing_marks = await self.get_marks_by_student_exam(student_id, exam_id)
        
        if existing_marks:
            existing_marks.is_absent = True
            existing_marks.marks_obtained = None
            existing_marks.grade = None
            existing_marks.grade_points = None
            existing_marks.status = MarksStatus.ABSENT
            await self.db.commit()
            await self.db.refresh(existing_marks)
            return existing_marks
        
        marks = Marks(
            student_id=student_id,
            exam_id=exam_id,
            enrollment_id=enrollment_id,
            max_marks=max_marks,
            is_absent=True,
            status=MarksStatus.ABSENT
        )
        
        self.db.add(marks)
        await self.db.commit()
        await self.db.refresh(marks)
        
        await audit_log(
            self.db,
            action="mark_absent",
            entity_type="marks",
            entity_id=marks.id,
            user_id=user_id,
            details={"student_id": student_id, "exam_id": exam_id}
        )
        
        return marks


# T057: Teacher marks entry functionality
async def enter_marks_bulk(
    self,
    exam_id: int,
    marks_data: List[dict],
    evaluated_by: int
) -> List['Marks']:
    """Teacher enters marks for multiple students (bulk entry)"""
    from src.models.marks import Marks, MarksStatus
    
    marks_list = []
    
    for data in marks_data:
        # Check if marks already exist
        result = await self.db.execute(
            select(Marks).where(
                and_(
                    Marks.student_id == data['student_id'],
                    Marks.exam_id == exam_id
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing marks
            existing.marks_obtained = data.get('marks_obtained')
            existing.is_absent = data.get('is_absent', False)
            existing.evaluator_comments = data.get('comments')
            existing.evaluated_by = evaluated_by
            existing.evaluated_at = datetime.utcnow()
            existing.status = MarksStatus.SUBMITTED
            
            # Calculate grade if marks obtained
            if existing.marks_obtained is not None and not existing.is_absent:
                existing.grade, existing.grade_points = self.calculate_grade(
                    existing.marks_obtained,
                    existing.max_marks
                )
            
            marks_list.append(existing)
        else:
            # Create new marks entry
            marks = Marks(
                student_id=data['student_id'],
                exam_id=exam_id,
                enrollment_id=data.get('enrollment_id'),
                marks_obtained=data.get('marks_obtained'),
                max_marks=data['max_marks'],
                is_absent=data.get('is_absent', False),
                evaluator_comments=data.get('comments'),
                evaluated_by=evaluated_by,
                evaluated_at=datetime.utcnow(),
                status=MarksStatus.SUBMITTED
            )
            
            # Calculate grade if marks obtained
            if marks.marks_obtained is not None and not marks.is_absent:
                marks.grade, marks.grade_points = self.calculate_grade(
                    marks.marks_obtained,
                    marks.max_marks
                )
            
            self.db.add(marks)
            marks_list.append(marks)
    
    await self.db.commit()
    
    logger.info(f"Teacher {evaluated_by} entered marks for {len(marks_data)} students in exam {exam_id}")
    
    return marks_list


async def enter_marks_single(
    self,
    student_id: int,
    exam_id: int,
    marks_obtained: Optional[float],
    max_marks: float,
    enrollment_id: int,
    evaluated_by: int,
    is_absent: bool = False,
    comments: Optional[str] = None
) -> 'Marks':
    """Teacher enters marks for single student"""
    from src.models.marks import Marks, MarksStatus
    
    # Check if marks already exist
    result = await self.db.execute(
        select(Marks).where(
            and_(
                Marks.student_id == student_id,
                Marks.exam_id == exam_id
            )
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing marks
        existing.marks_obtained = marks_obtained
        existing.is_absent = is_absent
        existing.evaluator_comments = comments
        existing.evaluated_by = evaluated_by
        existing.evaluated_at = datetime.utcnow()
        existing.status = MarksStatus.SUBMITTED
        
        if marks_obtained is not None and not is_absent:
            existing.grade, existing.grade_points = self.calculate_grade(
                marks_obtained,
                max_marks
            )
        
        await self.db.commit()
        await self.db.refresh(existing)
        
        logger.info(f"Updated marks for student {student_id} in exam {exam_id}")
        return existing
    
    # Create new marks entry
    marks = Marks(
        student_id=student_id,
        exam_id=exam_id,
        enrollment_id=enrollment_id,
        marks_obtained=marks_obtained,
        max_marks=max_marks,
        is_absent=is_absent,
        evaluator_comments=comments,
        evaluated_by=evaluated_by,
        evaluated_at=datetime.utcnow(),
        status=MarksStatus.SUBMITTED
    )
    
    if marks_obtained is not None and not is_absent:
        marks.grade, marks.grade_points = self.calculate_grade(
            marks_obtained,
            max_marks
        )
    
    self.db.add(marks)
    await self.db.commit()
    await self.db.refresh(marks)
    
    logger.info(f"Entered marks for student {student_id} in exam {exam_id}: {marks_obtained}/{max_marks}")
    
    return marks


def calculate_grade(
    self,
    marks_obtained: float,
    max_marks: float
) -> tuple:
    """Calculate grade and grade points based on percentage"""
    from src.models.marks import GradeType
    
    percentage = (marks_obtained / max_marks) * 100
    
    if percentage >= 90:
        return GradeType.A_PLUS, 10.0
    elif percentage >= 80:
        return GradeType.A, 9.0
    elif percentage >= 70:
        return GradeType.B_PLUS, 8.0
    elif percentage >= 60:
        return GradeType.B, 7.0
    elif percentage >= 50:
        return GradeType.C_PLUS, 6.0
    elif percentage >= 40:
        return GradeType.C, 5.0
    elif percentage >= 33:
        return GradeType.D, 4.0
    else:
        return GradeType.F, 0.0


async def verify_marks(
    self,
    marks_id: int,
    verified_by: int
) -> 'Marks':
    """Verify marks entered by teacher"""
    from src.models.marks import Marks, MarksStatus
    
    result = await self.db.execute(
        select(Marks).where(Marks.id == marks_id)
    )
    marks = result.scalar_one_or_none()
    
    if not marks:
        raise ValueError(f"Marks {marks_id} not found")
    
    marks.status = MarksStatus.VERIFIED
    marks.verified_by = verified_by
    marks.verified_at = datetime.utcnow()
    
    await self.db.commit()
    await self.db.refresh(marks)
    
    logger.info(f"Marks {marks_id} verified by {verified_by}")
    
    return marks


async def publish_marks(
    self,
    exam_id: int
) -> List['Marks']:
    """Publish marks for an exam"""
    from src.models.marks import Marks, MarksStatus
    
    result = await self.db.execute(
        select(Marks).where(
            and_(
                Marks.exam_id == exam_id,
                Marks.status == MarksStatus.VERIFIED
            )
        )
    )
    marks_list = result.scalars().all()
    
    for marks in marks_list:
        marks.status = MarksStatus.PUBLISHED
        marks.published_at = datetime.utcnow()
    
    await self.db.commit()
    
    logger.info(f"Published marks for {len(marks_list)} students in exam {exam_id}")
    
    return marks_list


async def get_marks_by_exam(
    self,
    exam_id: int,
    status: Optional['MarksStatus'] = None
) -> List['Marks']:
    """Get all marks for an exam"""
    from src.models.marks import Marks
    
    query = select(Marks).where(Marks.exam_id == exam_id)
    
    if status:
        query = query.where(Marks.status == status)
    
    result = await self.db.execute(query)
    return result.scalars().all()
