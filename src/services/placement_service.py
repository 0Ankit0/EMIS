"""
Placement Service for EMIS
Handles placement management, job postings, applications, and offers
"""
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from src.models.placement import Company, JobPosting, PlacementApplication, Interview, PlacementOffer, ApplicationStatus
from src.lib.logging import get_logger

logger = get_logger(__name__)


class PlacementService:
    """Service for placement management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Company Management
    def create_company(self, company_data: dict) -> Company:
        """Create a new company"""
        try:
            company = Company(**company_data)
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)
            logger.info(f"Company created: {company.id} - {company.name}")
            return company
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating company: {str(e)}")
            raise
    
    def get_company(self, company_id: int) -> Optional[Company]:
        """Get company by ID"""
        return self.db.query(Company).filter(Company.id == company_id).first()
    
    def get_companies(
        self,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Company]:
        """Get all companies"""
        query = self.db.query(Company)
        
        if is_active is not None:
            query = query.filter(Company.is_active == is_active)
        
        return query.order_by(Company.name).offset(skip).limit(limit).all()
    
    # Job Posting Management
    def create_job_posting(self, job_data: dict) -> JobPosting:
        """Create a new job posting"""
        try:
            job = JobPosting(**job_data, is_active=True, applications_count=0)
            self.db.add(job)
            self.db.commit()
            self.db.refresh(job)
            logger.info(f"Job posting created: {job.id} - {job.job_title}")
            return job
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating job posting: {str(e)}")
            raise
    
    def get_job_posting(self, job_id: int) -> Optional[JobPosting]:
        """Get job posting by ID"""
        return self.db.query(JobPosting).filter(JobPosting.id == job_id).first()
    
    def get_job_postings(
        self,
        company_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[JobPosting]:
        """Get job postings"""
        query = self.db.query(JobPosting)
        
        if company_id:
            query = query.filter(JobPosting.company_id == company_id)
        if is_active is not None:
            query = query.filter(JobPosting.is_active == is_active)
        
        return query.order_by(JobPosting.posted_date.desc()).offset(skip).limit(limit).all()
    
    def update_job_posting(self, job_id: int, job_data: dict) -> Optional[JobPosting]:
        """Update job posting"""
        try:
            job = self.get_job_posting(job_id)
            if not job:
                return None
            
            for key, value in job_data.items():
                setattr(job, key, value)
            
            self.db.commit()
            self.db.refresh(job)
            logger.info(f"Job posting updated: {job_id}")
            return job
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating job posting: {str(e)}")
            raise
    
    # Application Management
    def create_application(
        self,
        student_id: int,
        job_posting_id: int,
        application_data: dict
    ) -> PlacementApplication:
        """Create a job application"""
        try:
            # Check if student already applied
            existing = self.db.query(PlacementApplication).filter(
                PlacementApplication.student_id == student_id,
                PlacementApplication.job_posting_id == job_posting_id
            ).first()
            
            if existing:
                raise ValueError("Student has already applied for this position")
            
            # Check eligibility
            job = self.get_job_posting(job_posting_id)
            if not job or not job.is_active:
                raise ValueError("Job posting not available")
            
            if job.application_deadline and datetime.utcnow().date() > job.application_deadline:
                raise ValueError("Application deadline has passed")
            
            application = PlacementApplication(
                student_id=student_id,
                job_posting_id=job_posting_id,
                status=ApplicationStatus.SUBMITTED,
                **application_data
            )
            
            self.db.add(application)
            
            # Update applications count
            job.applications_count = (job.applications_count or 0) + 1
            
            self.db.commit()
            self.db.refresh(application)
            logger.info(f"Application created: {application.id} for job {job_posting_id}")
            return application
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating application: {str(e)}")
            raise
    
    def update_application_status(
        self,
        application_id: int,
        status: ApplicationStatus,
        remarks: Optional[str] = None
    ) -> PlacementApplication:
        """Update application status"""
        try:
            application = self.db.query(PlacementApplication).filter(
                PlacementApplication.id == application_id
            ).first()
            
            if not application:
                raise ValueError("Application not found")
            
            application.status = status
            if remarks:
                application.remarks = remarks
            
            self.db.commit()
            self.db.refresh(application)
            logger.info(f"Application status updated: {application_id} to {status}")
            return application
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating application status: {str(e)}")
            raise
    
    def get_student_applications(
        self,
        student_id: int,
        status: Optional[ApplicationStatus] = None
    ) -> List[PlacementApplication]:
        """Get applications for a student"""
        query = self.db.query(PlacementApplication).filter(
            PlacementApplication.student_id == student_id
        )
        
        if status:
            query = query.filter(PlacementApplication.status == status)
        
        return query.order_by(PlacementApplication.applied_date.desc()).all()
    
    def get_job_applications(
        self,
        job_posting_id: int,
        status: Optional[ApplicationStatus] = None
    ) -> List[PlacementApplication]:
        """Get applications for a job posting"""
        query = self.db.query(PlacementApplication).filter(
            PlacementApplication.job_posting_id == job_posting_id
        )
        
        if status:
            query = query.filter(PlacementApplication.status == status)
        
        return query.order_by(PlacementApplication.applied_date.desc()).all()
    
    # Interview Management
    def schedule_interview(self, interview_data: dict) -> Interview:
        """Schedule an interview"""
        try:
            interview = Interview(**interview_data, status=InterviewStatus.SCHEDULED)
            self.db.add(interview)
            self.db.commit()
            self.db.refresh(interview)
            logger.info(f"Interview scheduled: {interview.id}")
            return interview
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error scheduling interview: {str(e)}")
            raise
    
    def update_interview_status(
        self,
        interview_id: int,
        status: str,
        feedback: Optional[str] = None,
        rating: Optional[int] = None
    ) -> Interview:
        """Update interview status"""
        try:
            interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
            
            if not interview:
                raise ValueError("Interview not found")
            
            interview.status = status
            if feedback:
                interview.feedback = feedback
            if rating:
                interview.rating = rating
            
            self.db.commit()
            self.db.refresh(interview)
            logger.info(f"Interview status updated: {interview_id} to {status}")
            return interview
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating interview status: {str(e)}")
            raise
    
    def get_student_interviews(self, student_id: int) -> List[Interview]:
        """Get interviews for a student"""
        return self.db.query(Interview).join(PlacementApplication).filter(
            PlacementApplication.student_id == student_id
        ).order_by(Interview.scheduled_date.desc()).all()
    
    # Placement Offer Management
    def create_offer(self, offer_data: dict) -> PlacementOffer:
        """Create a placement offer"""
        try:
            offer = PlacementOffer(**offer_data)
            self.db.add(offer)
            
            # Update application status
            application = self.db.query(PlacementApplication).filter(
                PlacementApplication.id == offer_data['application_id']
            ).first()
            if application:
                application.status = ApplicationStatus.OFFERED
            
            self.db.commit()
            self.db.refresh(offer)
            logger.info(f"Placement offer created: {offer.id}")
            return offer
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating offer: {str(e)}")
            raise
    
    def accept_offer(self, offer_id: int) -> PlacementOffer:
        """Accept a placement offer"""
        try:
            offer = self.db.query(PlacementOffer).filter(PlacementOffer.id == offer_id).first()
            
            if not offer:
                raise ValueError("Offer not found")
            
            offer.is_accepted = True
            offer.acceptance_date = datetime.utcnow()
            
            # Update application status
            application = offer.application
            if application:
                application.status = ApplicationStatus.PLACED
            
            self.db.commit()
            self.db.refresh(offer)
            logger.info(f"Offer accepted: {offer_id}")
            return offer
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error accepting offer: {str(e)}")
            raise
    
    def get_student_offers(self, student_id: int) -> List[PlacementOffer]:
        """Get offers for a student"""
        return self.db.query(PlacementOffer).join(PlacementApplication).filter(
            PlacementApplication.student_id == student_id
        ).order_by(PlacementOffer.offer_date.desc()).all()
    
    # Statistics
    def get_placement_statistics(
        self,
        academic_year_id: Optional[int] = None,
        department_id: Optional[int] = None
    ) -> Dict:
        """Get placement statistics"""
        query = self.db.query(PlacementApplication)
        
        if academic_year_id:
            query = query.join(JobPosting).filter(
                JobPosting.academic_year_id == academic_year_id
            )
        
        total_applications = query.count()
        
        placed_students = query.filter(
            PlacementApplication.status == ApplicationStatus.PLACED
        ).count()
        
        total_offers = self.db.query(func.count(PlacementOffer.id)).scalar()
        
        accepted_offers = self.db.query(func.count(PlacementOffer.id)).filter(
            PlacementOffer.is_accepted == True
        ).scalar()
        
        # Average package
        avg_package = self.db.query(func.avg(PlacementOffer.package_amount)).filter(
            PlacementOffer.is_accepted == True
        ).scalar()
        
        highest_package = self.db.query(func.max(PlacementOffer.package_amount)).filter(
            PlacementOffer.is_accepted == True
        ).scalar()
        
        # Companies participated
        companies_count = self.db.query(func.count(func.distinct(JobPosting.company_id))).scalar()
        
        placement_rate = (placed_students / total_applications * 100) if total_applications > 0 else 0
        
        return {
            "total_applications": total_applications,
            "placed_students": placed_students,
            "placement_rate": round(placement_rate, 2),
            "total_offers": total_offers,
            "accepted_offers": accepted_offers,
            "average_package": float(avg_package) if avg_package else 0,
            "highest_package": float(highest_package) if highest_package else 0,
            "companies_participated": companies_count
        }
    
    def get_company_placement_report(self, company_id: int) -> Dict:
        """Get placement report for a company"""
        company = self.get_company(company_id)
        if not company:
            return {}
        
        jobs = self.get_job_postings(company_id=company_id)
        total_applications = sum(job.applications_count or 0 for job in jobs)
        
        total_offers = self.db.query(func.count(PlacementOffer.id)).join(
            PlacementApplication
        ).join(JobPosting).filter(JobPosting.company_id == company_id).scalar()
        
        placed_students = self.db.query(func.count(PlacementApplication.id)).filter(
            PlacementApplication.status == ApplicationStatus.PLACED
        ).join(JobPosting).filter(JobPosting.company_id == company_id).scalar()
        
        return {
            "company": {
                "id": company.id,
                "name": company.name,
                "industry": company.industry
            },
            "job_postings": len(jobs),
            "total_applications": total_applications,
            "total_offers": total_offers,
            "placed_students": placed_students
        }
