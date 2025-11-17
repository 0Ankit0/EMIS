"""
User service for CRUD operations
"""
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from apps.core.exceptions import NotFoundException, ValidationException, AuthorizationException
from apps.authentication.models import AuditLog

User = get_user_model()


class UserService:
    """Service for user management operations"""
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        try:
            return User.objects.select_related().prefetch_related('user_roles__role').get(id=user_id)
        except User.DoesNotExist:
            raise NotFoundException(f"User with ID {user_id} not found", code='AUTH_012')
    
    @staticmethod
    def get_users(page=1, page_size=20, search=None, is_active=None):
        """Get paginated list of users with optional filters and full-text search"""
        queryset = User.objects.select_related().prefetch_related('user_roles__role')
        
        # Apply full-text search using PostgreSQL tsvector
        if search:
            # Create search vector for relevant fields
            search_vector = SearchVector('username', weight='A') + \
                          SearchVector('email', weight='A') + \
                          SearchVector('first_name', weight='B') + \
                          SearchVector('last_name', weight='B')
            search_query = SearchQuery(search)
            
            # Annotate with search rank and filter
            queryset = queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank', '-created_at')
        else:
            # Default ordering when no search
            queryset = queryset.order_by('-created_at')
        
        # Apply other filters
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        # Pagination
        offset = (page - 1) * page_size
        total = queryset.count()
        users = list(queryset[offset:offset + page_size])
        
        return {
            'users': users,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }
    
    @staticmethod
    def update_user(user_id, data, actor=None):
        """Update user information"""
        user = UserService.get_user_by_id(user_id)
        
        allowed_fields = ['first_name', 'last_name', 'email', 'phone', 'is_active']
        
        for field, value in data.items():
            if field in allowed_fields:
                setattr(user, field, value)
        
        user.save()
        
        # Log the update
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='update',
                target_model='User',
                target_id=str(user.id),
                outcome='success',
                details={'updated_fields': list(data.keys())}
            )
        
        return user
    
    @staticmethod
    def delete_user(user_id, actor=None):
        """Soft delete a user"""
        user = UserService.get_user_by_id(user_id)
        
        # Don't allow deleting yourself
        if actor and actor.id == user.id:
            raise ValidationException("Cannot delete your own account", code='CORE_003')
        
        user.is_active = False
        user.save()
        
        # Log the deletion
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='delete',
                target_model='User',
                target_id=str(user.id),
                outcome='success'
            )
        
        return True
    
    @staticmethod
    def change_password(user, old_password, new_password):
        """Change user password"""
        if not user.check_password(old_password):
            raise ValidationException("Current password is incorrect", code='AUTH_001')
        
        user.set_password(new_password)
        user.save()
        
        # Log password change
        AuditLog.objects.create(
            actor=user,
            action='update',
            target_model='User',
            target_id=str(user.id),
            outcome='success',
            details={'action': 'password_change'}
        )
        
        return True
