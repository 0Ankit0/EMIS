from typing import List, Optional, Dict, Any
from django.db.models import Max
from apps.courses.models import Module, Course
from apps.core.exceptions import EMISException


class ModuleService:
    """Service for managing course modules"""
    
    @staticmethod
    def create_module(data: Dict[str, Any]) -> Module:
        """Create a new module"""
        course_id = data.get('course')
        
        # Verify course exists
        try:
            Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise EMISException(
                code="COURSES_003",
                message=f"Course {course_id} not found"
            )
        
        # Auto-assign sequence order if not provided
        if 'sequence_order' not in data or data['sequence_order'] is None:
            max_order = Module.objects.filter(
                course_id=course_id
            ).aggregate(Max('sequence_order'))['sequence_order__max']
            data['sequence_order'] = (max_order or 0) + 1
        
        module = Module.objects.create(**data)
        return module
    
    @staticmethod
    def get_module(module_id: str) -> Optional[Module]:
        """Get a module by ID"""
        try:
            return Module.objects.select_related('course').get(id=module_id)
        except Module.DoesNotExist:
            return None
    
    @staticmethod
    def list_modules_for_course(
        course_id: str,
        published_only: bool = False
    ) -> List[Module]:
        """List all modules for a course in sequence order"""
        queryset = Module.objects.filter(course_id=course_id)
        
        if published_only:
            queryset = queryset.filter(is_published=True)
        
        return list(queryset.order_by('sequence_order'))
    
    @staticmethod
    def update_module(module_id: str, data: Dict[str, Any]) -> Optional[Module]:
        """Update a module"""
        try:
            module = Module.objects.get(id=module_id)
            for key, value in data.items():
                setattr(module, key, value)
            module.save()
            return module
        except Module.DoesNotExist:
            return None
    
    @staticmethod
    def delete_module(module_id: str) -> bool:
        """Delete a module"""
        try:
            module = Module.objects.get(id=module_id)
            module.delete()
            return True
        except Module.DoesNotExist:
            return False
    
    @staticmethod
    def reorder_modules(course_id: str, module_order: List[str]) -> bool:
        """
        Reorder modules for a course
        
        Args:
            course_id: The course ID
            module_order: List of module IDs in desired order
        """
        try:
            Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise EMISException(
                code="COURSES_003",
                message=f"Course {course_id} not found"
            )
        
        # Update sequence order for each module
        for index, module_id in enumerate(module_order):
            try:
                module = Module.objects.get(id=module_id, course_id=course_id)
                module.sequence_order = index + 1
                module.save()
            except Module.DoesNotExist:
                raise EMISException(
                    code="COURSES_004",
                    message=f"Module {module_id} not found in course {course_id}"
                )
        
        return True
