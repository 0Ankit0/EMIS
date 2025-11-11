"""
Placement Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel
from src.database import get_db
from src.services.placement_service import PlacementService
from src.models.placement import ApplicationStatus
from src.middleware.rbac import get_current_user
from src.models.auth import User

router = APIRouter(prefix="/api/placement", tags=["Placement"])


# Pydantic Models
class CompanyCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


class JobPostingCreate(BaseModel):
    company_id: int
    job_title: str
    job_description: Optional[str] = None
    job_type: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    required_skills: Optional[str] = None
    min_cgpa: Optional[float] = None
    eligible_programs: Optional[str] = None
    vacancies: Optional[int] = None
    application_deadline: Optional[date] = None


class PlacementApplicationCreate(BaseModel):
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    additional_documents: Optional[str] = None


class InterviewSchedule(BaseModel):
    application_id: int
    scheduled_date: datetime
    interview_type: Optional[str] = None
    venue: Optional[str] = None
    interviewer_name: Optional[str] = None
    notes: Optional[str] = None


class InterviewUpdate(BaseModel):
    status: str
    feedback: Optional[str] = None
    rating: Optional[int] = None


class OfferCreate(BaseModel):
    application_id: int
    offer_date: date
    joining_date: Optional[date] = None
    package_amount: Optional[float] = None
    designation: Optional[str] = None
    location: Optional[str] = None
    offer_letter_url: Optional[str] = None


# Company Endpoints
@router.post("/companies", response_model=dict)
def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company"""
    service = PlacementService(db)
    company = service.create_company(company_data.dict())
    return {"message": "Company created successfully", "company_id": company.id}


@router.get("/companies", response_model=List[dict])
def get_companies(
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all companies"""
    service = PlacementService(db)
    companies = service.get_companies(is_active=is_active, skip=skip, limit=limit)
    return [
        {
            "id": c.id,
            "name": c.name,
            "industry": c.industry,
            "website": c.website,
            "is_active": c.is_active
        }
        for c in companies
    ]


@router.get("/companies/{company_id}", response_model=dict)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get company details"""
    service = PlacementService(db)
    company = service.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {
        "id": company.id,
        "name": company.name,
        "industry": company.industry,
        "website": company.website,
        "description": company.description,
        "contact_person": company.contact_person,
        "contact_email": company.contact_email,
        "is_active": company.is_active
    }


# Job Posting Endpoints
@router.post("/jobs", response_model=dict)
def create_job_posting(
    job_data: JobPostingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job posting"""
    service = PlacementService(db)
    job = service.create_job_posting(job_data.dict())
    return {"message": "Job posting created successfully", "job_id": job.id}


@router.get("/jobs", response_model=List[dict])
def get_job_postings(
    company_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all job postings"""
    service = PlacementService(db)
    jobs = service.get_job_postings(company_id=company_id, is_active=is_active, skip=skip, limit=limit)
    return [
        {
            "id": j.id,
            "company_name": j.company.name,
            "job_title": j.job_title,
            "location": j.location,
            "salary_min": float(j.salary_min) if j.salary_min else None,
            "salary_max": float(j.salary_max) if j.salary_max else None,
            "application_deadline": j.application_deadline,
            "applications_count": j.applications_count,
            "is_active": j.is_active
        }
        for j in jobs
    ]


@router.get("/jobs/{job_id}", response_model=dict)
def get_job_posting(job_id: int, db: Session = Depends(get_db)):
    """Get job posting details"""
    service = PlacementService(db)
    job = service.get_job_posting(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    return {
        "id": job.id,
        "company_name": job.company.name,
        "job_title": job.job_title,
        "job_description": job.job_description,
        "job_type": job.job_type,
        "location": job.location,
        "salary_min": float(job.salary_min) if job.salary_min else None,
        "salary_max": float(job.salary_max) if job.salary_max else None,
        "required_skills": job.required_skills,
        "min_cgpa": float(job.min_cgpa) if job.min_cgpa else None,
        "vacancies": job.vacancies,
        "application_deadline": job.application_deadline,
        "is_active": job.is_active
    }


# Application Endpoints
@router.post("/jobs/{job_id}/apply", response_model=dict)
def apply_for_job(
    job_id: int,
    application_data: PlacementApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Apply for a job"""
    service = PlacementService(db)
    try:
        # Assuming current_user has student_id attribute
        student_id = getattr(current_user, 'student_id', None)
        if not student_id:
            raise HTTPException(status_code=400, detail="Only students can apply for jobs")
        
        application = service.create_application(student_id, job_id, application_data.dict())
        return {"message": "Application submitted successfully", "application_id": application.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/students/{student_id}/applications", response_model=List[dict])
def get_student_applications(
    student_id: int,
    status: Optional[ApplicationStatus] = None,
    db: Session = Depends(get_db)
):
    """Get student's applications"""
    service = PlacementService(db)
    applications = service.get_student_applications(student_id, status)
    return [
        {
            "id": a.id,
            "job_title": a.job_posting.job_title,
            "company_name": a.job_posting.company.name,
            "status": a.status,
            "applied_date": a.applied_date
        }
        for a in applications
    ]


@router.get("/jobs/{job_id}/applications", response_model=List[dict])
def get_job_applications(
    job_id: int,
    status: Optional[ApplicationStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get applications for a job"""
    service = PlacementService(db)
    applications = service.get_job_applications(job_id, status)
    return [
        {
            "id": a.id,
            "student_name": a.student.full_name if a.student else None,
            "status": a.status,
            "applied_date": a.applied_date
        }
        for a in applications
    ]


@router.put("/applications/{application_id}/status", response_model=dict)
def update_application_status(
    application_id: int,
    status: ApplicationStatus,
    remarks: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update application status"""
    service = PlacementService(db)
    try:
        application = service.update_application_status(application_id, status, remarks)
        return {"message": "Application status updated", "application_id": application.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Interview Endpoints
@router.post("/interviews", response_model=dict)
def schedule_interview(
    interview_data: InterviewSchedule,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Schedule an interview"""
    service = PlacementService(db)
    interview = service.schedule_interview(interview_data.dict())
    return {"message": "Interview scheduled successfully", "interview_id": interview.id}


@router.put("/interviews/{interview_id}", response_model=dict)
def update_interview(
    interview_id: int,
    interview_data: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update interview status and feedback"""
    service = PlacementService(db)
    try:
        interview = service.update_interview_status(
            interview_id,
            interview_data.status,
            interview_data.feedback,
            interview_data.rating
        )
        return {"message": "Interview updated successfully", "interview_id": interview.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/students/{student_id}/interviews", response_model=List[dict])
def get_student_interviews(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get student's interviews"""
    service = PlacementService(db)
    interviews = service.get_student_interviews(student_id)
    return [
        {
            "id": i.id,
            "job_title": i.application.job_posting.job_title,
            "company_name": i.application.job_posting.company.name,
            "scheduled_date": i.scheduled_date,
            "interview_type": i.interview_type,
            "status": i.status,
            "venue": i.venue
        }
        for i in interviews
    ]


# Offer Endpoints
@router.post("/offers", response_model=dict)
def create_offer(
    offer_data: OfferCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a placement offer"""
    service = PlacementService(db)
    offer = service.create_offer(offer_data.dict())
    return {"message": "Offer created successfully", "offer_id": offer.id}


@router.post("/offers/{offer_id}/accept", response_model=dict)
def accept_offer(
    offer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a placement offer"""
    service = PlacementService(db)
    try:
        offer = service.accept_offer(offer_id)
        return {"message": "Offer accepted successfully", "offer_id": offer.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/students/{student_id}/offers", response_model=List[dict])
def get_student_offers(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get student's offers"""
    service = PlacementService(db)
    offers = service.get_student_offers(student_id)
    return [
        {
            "id": o.id,
            "company_name": o.application.job_posting.company.name,
            "designation": o.designation,
            "package_amount": float(o.package_amount) if o.package_amount else None,
            "offer_date": o.offer_date,
            "joining_date": o.joining_date,
            "is_accepted": o.is_accepted
        }
        for o in offers
    ]


# Statistics
@router.get("/statistics", response_model=dict)
def get_placement_statistics(
    academic_year_id: Optional[int] = None,
    department_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get placement statistics"""
    service = PlacementService(db)
    return service.get_placement_statistics(academic_year_id, department_id)


@router.get("/companies/{company_id}/report", response_model=dict)
def get_company_report(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get company placement report"""
    service = PlacementService(db)
    return service.get_company_placement_report(company_id)
