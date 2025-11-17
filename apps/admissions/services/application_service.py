"""Application service for admissions processing"""
from typing import Dict, List, Optional
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from ..models import Application
from apps.authentication.models import User


class ApplicationService:
    """Service for managing applications"""
    
    # Application status state machine
    STATUS_TRANSITIONS = {
        'draft': ['submitted', 'cancelled'],
        'submitted': ['under_review', 'cancelled'],
        'under_review': ['accepted', 'rejected', 'pending'],
        'pending': ['under_review', 'accepted', 'rejected'],
        'accepted': ['enrolled'],
        'rejected': [],
        'cancelled': [],
        'enrolled': []
    }
    
    @classmethod
    def submit_application(cls, application_data: Dict) -> Application:
        """Submit a new application"""
        with transaction.atomic():
            application = Application.objects.create(**application_data)
            application.submitted_at = timezone.now()
            application.status = 'submitted'
            application.save()
            return application
    
    @classmethod
    def validate_application(cls, application: Application) -> Dict:
        """Validate application data"""
        errors = {}
        
        # Required fields validation
        required_fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'program', 'admission_year', 'previous_school'
        ]
        
        for field in required_fields:
            if not getattr(application, field, None):
                errors[field] = f"{field} is required"
        
        # Email uniqueness for the same program/year
        if Application.objects.filter(
            email=application.email,
            program=application.program,
            admission_year=application.admission_year
        ).exclude(id=application.id).exists():
            errors['email'] = "Application with this email already exists for this program/year"
        
        return errors
    
    @classmethod
    def update_status(
        cls,
        application: Application,
        new_status: str,
        reviewer: Optional[User] = None,
        review_notes: Optional[str] = None,
        merit_score: Optional[float] = None,
        rank: Optional[int] = None
    ) -> Application:
        """Update application status with state machine validation"""
        
        # Validate status transition
        current_status = application.status
        allowed_transitions = cls.STATUS_TRANSITIONS.get(current_status, [])
        
        if new_status not in allowed_transitions:
            raise ValidationError(
                f"Cannot transition from '{current_status}' to '{new_status}'. "
                f"Allowed transitions: {', '.join(allowed_transitions)}"
            )
        
        with transaction.atomic():
            application.status = new_status
            
            if reviewer:
                application.reviewed_by = reviewer
                application.reviewed_at = timezone.now()
            
            if review_notes:
                application.review_notes = review_notes
            
            if merit_score is not None:
                application.merit_score = merit_score
            
            if rank is not None:
                application.rank = rank
            
            application.save()
            return application
    
    @classmethod
    def get_applications_by_status(cls, status: str, program: Optional[str] = None, 
                                   admission_year: Optional[int] = None,
                                   search: Optional[str] = None) -> List[Application]:
        """Get applications filtered by status with full-text search"""
        queryset = Application.objects.filter(status=status)
        
        if program:
            queryset = queryset.filter(program=program)
        
        if admission_year:
            queryset = queryset.filter(admission_year=admission_year)
        
        # Apply full-text search
        if search:
            search_vector = SearchVector('first_name', weight='A') + \
                          SearchVector('last_name', weight='A') + \
                          SearchVector('email', weight='B') + \
                          SearchVector('program', weight='B')
            search_query = SearchQuery(search)
            
            queryset = queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank', '-submitted_at')
        else:
            queryset = queryset.order_by('-submitted_at')
        
        return queryset
    
    @classmethod
    def bulk_update_status(cls, application_ids: List[int], new_status: str, 
                          reviewer: User) -> int:
        """Bulk update application status"""
        applications = Application.objects.filter(id__in=application_ids)
        updated_count = 0
        
        for application in applications:
            try:
                cls.update_status(application, new_status, reviewer)
                updated_count += 1
            except ValidationError:
                # Skip invalid transitions
                continue
        
        return updated_count
