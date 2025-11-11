"""Exam and Marks API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

from src.database import get_db
from src.services.exam_service import ExamService
from src.services.marks_service import MarksService
from src.services.result_service import ResultService
from src.models.exam import ExamType, ExamStatus
from src.models.marks import MarksStatus, GradeType
from src.models.result_sheet import ResultType, ResultStatus
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/exams", tags=["exams"])


# Exam Schemas
class ExamCreate(BaseModel):
    course_id: int
    exam_name: str
    exam_type: ExamType
    exam_code: str
    exam_date: date
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    max_marks: float
    passing_marks: float
    weightage_percentage: float = 100.0
    venue: Optional[str] = None
    room_number: Optional[str] = None
    instructions: Optional[str] = None
    syllabus_topics: Optional[str] = None


class ExamResponse(BaseModel):
    id: int
    course_id: int
    exam_name: str
    exam_type: ExamType
    exam_code: str
    exam_date: date
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    max_marks: float
    passing_marks: float
    status: ExamStatus
    
    class Config:
        from_attributes = True


# Marks Schemas
class MarksCreate(BaseModel):
    student_id: int
    exam_id: int
    enrollment_id: int
    marks_obtained: Optional[float] = None
    max_marks: float
    is_absent: bool = False
    remarks: Optional[str] = None


class MarksUpdate(BaseModel):
    marks_obtained: float
    evaluator_comments: Optional[str] = None


class MarksResponse(BaseModel):
    id: int
    student_id: int
    exam_id: int
    enrollment_id: int
    marks_obtained: Optional[float]
    max_marks: float
    grade: Optional[GradeType]
    grade_points: Optional[float]
    status: MarksStatus
    is_absent: bool
    
    class Config:
        from_attributes = True


# Result Schemas
class ResultSheetResponse(BaseModel):
    id: int
    student_id: int
    enrollment_id: int
    result_type: ResultType
    academic_year: str
    semester: Optional[int]
    total_marks_obtained: float
    total_max_marks: float
    percentage: Optional[float]
    cgpa: Optional[float]
    sgpa: Optional[float]
    is_passed: bool
    has_backlogs: bool
    status: ResultStatus
    
    class Config:
        from_attributes = True


# Exam Endpoints
@router.post("/", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
async def create_exam(
    exam_data: ExamCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:create"]))
):
    """Create a new exam"""
    service = ExamService(db)
    
    existing = await service.get_exam_by_code(exam_data.exam_code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exam code already exists"
        )
    
    exam = await service.create_exam(**exam_data.dict(), created_by=current_user.get("id"))
    return exam


@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:read"]))
):
    """Get an exam by ID"""
    service = ExamService(db)
    exam = await service.get_exam_by_id(exam_id)
    
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    
    return exam


@router.get("/course/{course_id}", response_model=List[ExamResponse])
async def get_exams_by_course(
    course_id: int,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:read"]))
):
    """Get all exams for a course"""
    service = ExamService(db)
    exams = await service.get_exams_by_course(course_id, active_only)
    return exams


@router.get("/upcoming", response_model=List[ExamResponse])
async def get_upcoming_exams(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:read"]))
):
    """Get upcoming exams"""
    service = ExamService(db)
    exams = await service.get_upcoming_exams(days)
    return exams


# Marks Endpoints
@router.post("/{exam_id}/marks", response_model=MarksResponse, status_code=status.HTTP_201_CREATED)
async def create_marks(
    exam_id: int,
    marks_data: MarksCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:create"]))
):
    """Create marks entry for a student"""
    if marks_data.exam_id != exam_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exam ID mismatch")
    
    service = MarksService(db)
    marks = await service.create_marks(**marks_data.dict(), evaluator_id=current_user.get("id"))
    return marks


@router.put("/marks/{marks_id}", response_model=MarksResponse)
async def update_marks(
    marks_id: int,
    marks_data: MarksUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:update"]))
):
    """Update marks for a student"""
    service = MarksService(db)
    marks = await service.update_marks(
        marks_id,
        marks_data.marks_obtained,
        marks_data.evaluator_comments,
        current_user.get("id")
    )
    
    if not marks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marks not found")
    
    return marks


@router.post("/marks/{marks_id}/verify", response_model=MarksResponse)
async def verify_marks(
    marks_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:verify"]))
):
    """Verify marks"""
    service = MarksService(db)
    marks = await service.verify_marks(marks_id, current_user.get("id"))
    
    if not marks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marks not found or not submitted")
    
    return marks


@router.post("/marks/{marks_id}/publish", response_model=MarksResponse)
async def publish_marks(
    marks_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:publish"]))
):
    """Publish marks"""
    service = MarksService(db)
    marks = await service.publish_marks(marks_id, current_user.get("id"))
    
    if not marks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marks not found or not verified")
    
    return marks


@router.post("/{exam_id}/marks/publish-all")
async def bulk_publish_marks(
    exam_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:publish"]))
):
    """Publish all verified marks for an exam"""
    service = MarksService(db)
    count = await service.bulk_publish_marks(exam_id, current_user.get("id"))
    return {"published_count": count}


@router.get("/{exam_id}/marks", response_model=List[MarksResponse])
async def get_exam_marks(
    exam_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:read"]))
):
    """Get all marks for an exam"""
    service = MarksService(db)
    marks = await service.get_marks_by_exam(exam_id)
    return marks


@router.get("/student/{student_id}/marks", response_model=List[MarksResponse])
async def get_student_marks(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:read"]))
):
    """Get all marks for a student"""
    service = MarksService(db)
    marks = await service.get_marks_by_student(student_id)
    return marks


# Result Sheet Endpoints
@router.post("/results/generate", response_model=ResultSheetResponse, status_code=status.HTTP_201_CREATED)
async def generate_result(
    student_id: int,
    enrollment_id: int,
    result_type: ResultType,
    academic_year: str,
    semester: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["result:generate"]))
):
    """Generate result sheet for a student"""
    service = ResultService(db)
    result = await service.generate_result_sheet(
        student_id, enrollment_id, result_type, academic_year, semester,
        generated_by=current_user.get("id")
    )
    return result


@router.get("/results/{result_id}", response_model=ResultSheetResponse)
async def get_result(
    result_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["result:read"]))
):
    """Get a result sheet by ID"""
    service = ResultService(db)
    result = await service.get_result_by_id(result_id)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")
    
    return result


@router.get("/student/{student_id}/results", response_model=List[ResultSheetResponse])
async def get_student_results(
    student_id: int,
    published_only: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["result:read"]))
):
    """Get all results for a student"""
    service = ResultService(db)
    results = await service.get_results_by_student(student_id, published_only)
    return results


@router.post("/results/{result_id}/verify", response_model=ResultSheetResponse)
async def verify_result(
    result_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["result:verify"]))
):
    """Verify a result sheet"""
    service = ResultService(db)
    result = await service.verify_result(result_id, current_user.get("id"))
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found or not generated")
    
    return result


@router.post("/results/{result_id}/publish", response_model=ResultSheetResponse)
async def publish_result(
    result_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["result:publish"]))
):
    """Publish a result sheet"""
    service = ResultService(db)
    result = await service.publish_result(result_id, current_user.get("id"))
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found or not verified")
    
    return result


# T062: Exam routine endpoints
class ExamRoutineCreate(BaseModel):
    routine_name: str
    routine_code: str
    academic_year: str
    semester: int
    exam_type: str
    start_date: date
    end_date: date
    general_instructions: Optional[str] = None


class ExamSlotCreate(BaseModel):
    routine_id: int
    exam_id: int
    exam_date: date
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    venue: str
    room_numbers: Optional[str] = None


@router.post("/routines", status_code=status.HTTP_201_CREATED)
async def create_exam_routine(
    routine_data: ExamRoutineCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:admin"]))
):
    """Create exam routine/timetable (T053)"""
    service = ExamService(db)
    
    routine = await service.create_exam_routine(
        **routine_data.dict(),
        created_by=current_user.get("id")
    )
    
    return {
        "id": routine.id,
        "routine_name": routine.routine_name,
        "routine_code": routine.routine_code,
        "academic_year": routine.academic_year,
        "semester": routine.semester
    }


@router.post("/routines/slots", status_code=status.HTTP_201_CREATED)
async def add_exam_slot_to_routine(
    slot_data: ExamSlotCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:admin"]))
):
    """Add exam slot to routine (T053)"""
    service = ExamService(db)
    
    slot = await service.add_exam_to_routine(**slot_data.dict())
    
    return {
        "id": slot.id,
        "routine_id": slot.routine_id,
        "exam_id": slot.exam_id,
        "exam_date": slot.exam_date,
        "venue": slot.venue
    }


@router.post("/routines/{routine_id}/publish")
async def publish_exam_routine(
    routine_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:admin"]))
):
    """Publish exam routine for students (T053)"""
    service = ExamService(db)
    
    routine = await service.publish_exam_routine(
        routine_id=routine_id,
        published_by=current_user.get("id")
    )
    
    return {
        "id": routine.id,
        "is_published": routine.is_published,
        "published_at": routine.published_at,
        "message": "Exam routine published successfully"
    }


@router.get("/routines")
async def get_exam_routines(
    academic_year: str,
    semester: int,
    exam_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:read"]))
):
    """Get exam routines (T053)"""
    service = ExamService(db)
    
    routines = await service.get_exam_routine(
        academic_year=academic_year,
        semester=semester,
        exam_type=exam_type
    )
    
    return {
        "routines": [
            {
                "id": r.id,
                "routine_name": r.routine_name,
                "routine_code": r.routine_code,
                "exam_type": r.exam_type,
                "start_date": r.start_date,
                "end_date": r.end_date,
                "is_published": r.is_published
            }
            for r in routines
        ]
    }


# T063: Exam form endpoints
class ExamFormCreate(BaseModel):
    routine_id: int
    academic_year: str
    semester: int
    registered_courses: List[int]
    program_id: Optional[int] = None


@router.post("/forms", status_code=status.HTTP_201_CREATED)
async def create_exam_form(
    form_data: ExamFormCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:apply"]))
):
    """Student creates exam form (T054)"""
    service = ExamService(db)
    
    exam_form = await service.create_exam_form(
        student_id=current_user.get("student_id"),
        **form_data.dict()
    )
    
    return {
        "id": exam_form.id,
        "form_number": exam_form.form_number,
        "status": exam_form.status,
        "message": "Exam form created. Please complete and submit it."
    }


@router.post("/forms/{form_id}/submit")
async def submit_exam_form(
    form_id: int,
    declaration_accepted: bool,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:apply"]))
):
    """Student submits exam form (T054)"""
    service = ExamService(db)
    
    try:
        exam_form = await service.submit_exam_form(
            form_id=form_id,
            declaration_accepted=declaration_accepted
        )
        return {
            "id": exam_form.id,
            "form_number": exam_form.form_number,
            "status": exam_form.status,
            "submitted_at": exam_form.submitted_at,
            "message": "Exam form submitted successfully. Pending verification."
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/forms/{form_id}/verify")
async def verify_exam_form(
    form_id: int,
    verification_remarks: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:verify"]))
):
    """Verify exam form (T054)"""
    service = ExamService(db)
    
    exam_form = await service.verify_exam_form(
        form_id=form_id,
        verified_by=current_user.get("id"),
        verification_remarks=verification_remarks
    )
    
    return {
        "id": exam_form.id,
        "status": exam_form.status,
        "verified_at": exam_form.verified_at
    }


@router.post("/forms/{form_id}/approve")
async def approve_exam_form(
    form_id: int,
    exam_fee_amount: float,
    approval_remarks: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["exam:approve"]))
):
    """Approve exam form and generate hall ticket (T054)"""
    service = ExamService(db)
    
    exam_form = await service.approve_exam_form(
        form_id=form_id,
        approved_by=current_user.get("id"),
        exam_fee_amount=exam_fee_amount,
        approval_remarks=approval_remarks
    )
    
    return {
        "id": exam_form.id,
        "status": exam_form.status,
        "hall_ticket_number": exam_form.hall_ticket_number,
        "exam_fee_amount": exam_form.exam_fee_amount,
        "message": "Exam form approved. Hall ticket generated."
    }


# T057: Teacher marks entry endpoints
class MarksEntry(BaseModel):
    student_id: int
    enrollment_id: int
    marks_obtained: Optional[float]
    max_marks: float
    is_absent: bool = False
    comments: Optional[str] = None


class BulkMarksEntry(BaseModel):
    exam_id: int
    marks_data: List[MarksEntry]


@router.post("/marks/bulk", status_code=status.HTTP_201_CREATED)
async def enter_marks_bulk(
    marks_data: BulkMarksEntry,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:enter"]))
):
    """Teacher enters marks for multiple students (T057)"""
    service = MarksService(db)
    
    marks_list = await service.enter_marks_bulk(
        exam_id=marks_data.exam_id,
        marks_data=[m.dict() for m in marks_data.marks_data],
        evaluated_by=current_user.get("id")
    )
    
    return {
        "total_entries": len(marks_list),
        "exam_id": marks_data.exam_id,
        "message": f"Marks entered for {len(marks_list)} students"
    }


@router.post("/marks/single", status_code=status.HTTP_201_CREATED)
async def enter_marks_single(
    exam_id: int,
    marks_entry: MarksEntry,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:enter"]))
):
    """Teacher enters marks for single student (T057)"""
    service = MarksService(db)
    
    marks = await service.enter_marks_single(
        exam_id=exam_id,
        **marks_entry.dict(),
        evaluated_by=current_user.get("id")
    )
    
    return {
        "id": marks.id,
        "student_id": marks.student_id,
        "marks_obtained": marks.marks_obtained,
        "max_marks": marks.max_marks,
        "grade": marks.grade,
        "grade_points": marks.grade_points,
        "status": marks.status
    }


@router.post("/marks/{marks_id}/verify")
async def verify_marks(
    marks_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:verify"]))
):
    """Verify marks (T057)"""
    service = MarksService(db)
    
    marks = await service.verify_marks(
        marks_id=marks_id,
        verified_by=current_user.get("id")
    )
    
    return {
        "id": marks.id,
        "status": marks.status,
        "verified_at": marks.verified_at
    }


@router.post("/marks/exam/{exam_id}/publish")
async def publish_exam_marks(
    exam_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:publish"]))
):
    """Publish marks for an exam (T057)"""
    service = MarksService(db)
    
    marks_list = await service.publish_marks(exam_id=exam_id)
    
    return {
        "exam_id": exam_id,
        "total_published": len(marks_list),
        "message": "Marks published successfully"
    }


@router.get("/marks/exam/{exam_id}")
async def get_exam_marks(
    exam_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["marks:read"]))
):
    """Get all marks for an exam (T057)"""
    service = MarksService(db)
    
    marks_list = await service.get_marks_by_exam(
        exam_id=exam_id,
        status=status
    )
    
    return {
        "exam_id": exam_id,
        "total_entries": len(marks_list),
        "marks": [
            {
                "id": m.id,
                "student_id": m.student_id,
                "marks_obtained": m.marks_obtained,
                "max_marks": m.max_marks,
                "grade": m.grade,
                "is_absent": m.is_absent,
                "status": m.status
            }
            for m in marks_list
        ]
    }
