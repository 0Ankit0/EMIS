"""Result Service for generating and managing result sheets"""
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from src.models.result_sheet import ResultSheet, ResultStatus, ResultType
from src.models.marks import Marks, MarksStatus
from src.lib.audit import audit_log


class ResultService:
    """Service for generating and managing result sheets"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def calculate_result_data(self, enrollment_id: int) -> Dict:
        """Calculate aggregated result data for an enrollment"""
        result = await self.db.execute(
            select(Marks).where(
                and_(
                    Marks.enrollment_id == enrollment_id,
                    Marks.status == MarksStatus.PUBLISHED,
                    Marks.is_absent == False
                )
            )
        )
        marks_list = list(result.scalars().all())
        
        if not marks_list:
            return {
                "total_marks_obtained": 0.0,
                "total_max_marks": 0.0,
                "percentage": 0.0,
                "cgpa": 0.0,
                "sgpa": 0.0,
                "is_passed": False,
                "has_backlogs": False,
                "backlog_count": 0,
                "internal_marks_total": 0.0,
                "external_marks_total": 0.0,
                "marks_breakdown": [],
                "subject_wise_details": []
            }
        
        total_obtained = sum(m.marks_obtained or 0 for m in marks_list)
        total_max = sum(m.max_marks for m in marks_list)
        percentage = (total_obtained / total_max * 100) if total_max > 0 else 0
        
        total_grade_points = sum(m.grade_points or 0 for m in marks_list)
        cgpa = total_grade_points / len(marks_list) if marks_list else 0
        sgpa = cgpa
        
        backlog_count = sum(1 for m in marks_list if (m.marks_obtained or 0) < (m.max_marks * 0.4))
        has_backlogs = backlog_count > 0
        is_passed = not has_backlogs and percentage >= 40
        
        marks_breakdown = [
            {
                "exam_id": m.exam_id,
                "marks_obtained": m.marks_obtained,
                "max_marks": m.max_marks,
                "grade": m.grade.value if m.grade else None,
                "grade_points": m.grade_points
            }
            for m in marks_list
        ]
        
        return {
            "total_marks_obtained": total_obtained,
            "total_max_marks": total_max,
            "percentage": round(percentage, 2),
            "cgpa": round(cgpa, 2),
            "sgpa": round(sgpa, 2),
            "is_passed": is_passed,
            "has_backlogs": has_backlogs,
            "backlog_count": backlog_count,
            "internal_marks_total": 0.0,
            "external_marks_total": total_obtained,
            "marks_breakdown": marks_breakdown,
            "subject_wise_details": []
        }
    
    async def generate_result_sheet(
        self,
        student_id: int,
        enrollment_id: int,
        result_type: ResultType,
        academic_year: str,
        semester: Optional[int] = None,
        generated_by: Optional[int] = None
    ) -> ResultSheet:
        """Generate a result sheet for a student"""
        result_data = await self.calculate_result_data(enrollment_id)
        
        result_sheet = ResultSheet(
            student_id=student_id,
            enrollment_id=enrollment_id,
            result_type=result_type,
            academic_year=academic_year,
            semester=semester,
            **result_data,
            status=ResultStatus.GENERATED,
            generated_by=generated_by,
            generated_at=datetime.utcnow()
        )
        
        self.db.add(result_sheet)
        await self.db.commit()
        await self.db.refresh(result_sheet)
        
        await audit_log(
            self.db,
            action="generate_result_sheet",
            entity_type="result_sheet",
            entity_id=result_sheet.id,
            user_id=generated_by,
            details={"student_id": student_id, "enrollment_id": enrollment_id, "type": result_type.value}
        )
        
        return result_sheet
    
    async def get_result_by_id(self, result_id: int) -> Optional[ResultSheet]:
        """Get a result sheet by ID"""
        result = await self.db.execute(
            select(ResultSheet).where(ResultSheet.id == result_id)
        )
        return result.scalar_one_or_none()
    
    async def get_results_by_student(
        self,
        student_id: int,
        published_only: bool = False
    ) -> List[ResultSheet]:
        """Get all result sheets for a student"""
        query = select(ResultSheet).where(ResultSheet.student_id == student_id)
        
        if published_only:
            query = query.where(ResultSheet.status == ResultStatus.PUBLISHED)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_results_by_enrollment(
        self,
        enrollment_id: int,
        published_only: bool = False
    ) -> List[ResultSheet]:
        """Get all result sheets for an enrollment"""
        query = select(ResultSheet).where(ResultSheet.enrollment_id == enrollment_id)
        
        if published_only:
            query = query.where(ResultSheet.status == ResultStatus.PUBLISHED)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def verify_result(
        self,
        result_id: int,
        verifier_id: int
    ) -> Optional[ResultSheet]:
        """Verify a result sheet"""
        result_sheet = await self.get_result_by_id(result_id)
        if not result_sheet or result_sheet.status != ResultStatus.GENERATED:
            return None
        
        result_sheet.status = ResultStatus.VERIFIED
        result_sheet.verified_by = verifier_id
        result_sheet.verified_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(result_sheet)
        
        await audit_log(
            self.db,
            action="verify_result",
            entity_type="result_sheet",
            entity_id=result_id,
            user_id=verifier_id
        )
        
        return result_sheet
    
    async def publish_result(
        self,
        result_id: int,
        publisher_id: int
    ) -> Optional[ResultSheet]:
        """Publish a result sheet"""
        result_sheet = await self.get_result_by_id(result_id)
        if not result_sheet or result_sheet.status != ResultStatus.VERIFIED:
            return None
        
        result_sheet.status = ResultStatus.PUBLISHED
        result_sheet.published_by = publisher_id
        result_sheet.published_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(result_sheet)
        
        await audit_log(
            self.db,
            action="publish_result",
            entity_type="result_sheet",
            entity_id=result_id,
            user_id=publisher_id
        )
        
        return result_sheet
    
    async def bulk_generate_results(
        self,
        enrollment_ids: List[int],
        result_type: ResultType,
        academic_year: str,
        semester: Optional[int] = None,
        generated_by: Optional[int] = None
    ) -> List[ResultSheet]:
        """Generate result sheets for multiple enrollments"""
        result_sheets = []
        
        for enrollment_id in enrollment_ids:
            result = await self.db.execute(
                select(Marks).where(Marks.enrollment_id == enrollment_id).limit(1)
            )
            marks = result.scalar_one_or_none()
            
            if marks:
                result_sheet = await self.generate_result_sheet(
                    student_id=marks.student_id,
                    enrollment_id=enrollment_id,
                    result_type=result_type,
                    academic_year=academic_year,
                    semester=semester,
                    generated_by=generated_by
                )
                result_sheets.append(result_sheet)
        
        return result_sheets
    
    async def update_result_sheet(
        self,
        result_id: int,
        updates: dict,
        user_id: Optional[int] = None
    ) -> Optional[ResultSheet]:
        """Update a result sheet"""
        result_sheet = await self.get_result_by_id(result_id)
        if not result_sheet:
            return None
        
        for key, value in updates.items():
            if hasattr(result_sheet, key) and key not in ['id', 'created_at']:
                setattr(result_sheet, key, value)
        
        await self.db.commit()
        await self.db.refresh(result_sheet)
        
        await audit_log(
            self.db,
            action="update_result_sheet",
            entity_type="result_sheet",
            entity_id=result_id,
            user_id=user_id,
            details=updates
        )
        
        return result_sheet
