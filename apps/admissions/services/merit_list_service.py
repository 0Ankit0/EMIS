"""Merit list service for generating and managing merit lists"""
from typing import Dict, List, Optional
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from ..models import Application, MeritList
from apps.authentication.models import User


class MeritListService:
    """Service for generating and managing merit lists"""
    
    @classmethod
    def generate_merit_list(
        cls,
        name: str,
        program: str,
        admission_year: int,
        admission_semester: str,
        criteria: str,
        generated_by: User,
        cutoff_score: Optional[Decimal] = None,
        total_seats: Optional[int] = None
    ) -> MeritList:
        """Generate a new merit list with ranked applications"""
        
        with transaction.atomic():
            # Get all accepted applications for the program/year
            applications = Application.objects.filter(
                program=program,
                admission_year=admission_year,
                admission_semester=admission_semester,
                status='accepted',
                merit_score__isnull=False
            ).order_by('-merit_score', 'submitted_at')
            
            # Rank applications
            ranked_apps = cls.rank_applications(applications)
            
            # Apply cutoff if specified
            if cutoff_score:
                ranked_apps = [app for app in ranked_apps if app['merit_score'] >= cutoff_score]
            
            # Limit to total seats if specified
            if total_seats:
                ranked_apps = ranked_apps[:total_seats]
            
            # Get latest version for this program/year
            latest_version = MeritList.objects.filter(
                program=program,
                admission_year=admission_year,
                admission_semester=admission_semester
            ).order_by('-version').first()
            
            next_version = (latest_version.version + 1) if latest_version else 1
            
            # Create merit list
            merit_list = MeritList.objects.create(
                name=name,
                program=program,
                admission_year=admission_year,
                admission_semester=admission_semester,
                criteria=criteria,
                version=next_version,
                cutoff_score=cutoff_score,
                total_seats=total_seats or len(ranked_apps),
                generated_by=generated_by,
                generation_timestamp=timezone.now(),
                merit_list_data={'applications': ranked_apps}
            )
            
            # Update application ranks
            for rank, app_data in enumerate(ranked_apps, start=1):
                Application.objects.filter(id=app_data['id']).update(rank=rank)
            
            return merit_list
    
    @classmethod
    def rank_applications(cls, applications) -> List[Dict]:
        """Rank applications based on merit score"""
        ranked = []
        
        for rank, application in enumerate(applications, start=1):
            ranked.append({
                'id': str(application.id),
                'application_number': application.application_number,
                'name': f"{application.first_name} {application.last_name}",
                'email': application.email,
                'merit_score': float(application.merit_score),
                'rank': rank,
                'submitted_at': application.submitted_at.isoformat(),
            })
        
        return ranked
    
    @classmethod
    def publish_merit_list(cls, merit_list: MeritList) -> MeritList:
        """Publish a merit list (make it publicly visible)"""
        merit_list.is_published = True
        merit_list.save()
        return merit_list
    
    @classmethod
    def get_merit_lists(cls, program: Optional[str] = None, 
                       admission_year: Optional[int] = None,
                       is_published: Optional[bool] = None) -> List[MeritList]:
        """Get merit lists with filters"""
        queryset = MeritList.objects.all()
        
        if program:
            queryset = queryset.filter(program=program)
        
        if admission_year:
            queryset = queryset.filter(admission_year=admission_year)
        
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published)
        
        return queryset.order_by('-generation_timestamp')
    
    @classmethod
    def recalculate_ranks(cls, merit_list: MeritList) -> MeritList:
        """Recalculate ranks for a merit list (idempotent)"""
        applications = Application.objects.filter(
            program=merit_list.program,
            admission_year=merit_list.admission_year,
            admission_semester=merit_list.admission_semester,
            status='accepted',
            merit_score__isnull=False
        ).order_by('-merit_score', 'submitted_at')
        
        ranked_apps = cls.rank_applications(applications)
        
        # Update application ranks
        for rank, app_data in enumerate(ranked_apps, start=1):
            Application.objects.filter(id=app_data['id']).update(rank=rank)
        
        # Update merit list data
        merit_list.merit_list_data = {'applications': ranked_apps}
        merit_list.generation_timestamp = timezone.now()
        merit_list.save()
        
        return merit_list
