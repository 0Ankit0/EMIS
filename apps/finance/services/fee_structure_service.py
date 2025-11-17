"""Fee structure service for managing fee structures"""
from typing import List, Optional, Dict, Any
from django.db.models import Q, QuerySet
from apps.finance.models.fee_structure import FeeStructure
from apps.core.exceptions import EMISException
from decimal import Decimal
from datetime import date


class FeeStructureService:
    """Service for fee structure management"""
    
    @staticmethod
    def create_fee_structure(data: Dict[str, Any]) -> FeeStructure:
        """
        Create a new fee structure
        
        Args:
            data: Fee structure data including components, rules, and policy
        
        Returns:
            Created fee structure
        
        Raises:
            EMISException: If validation fails
        """
        # Calculate total from components
        if data.get('components'):
            total = sum(float(v) for v in data['components'].values())
            data['total_amount'] = Decimal(str(total))
        
        fee_structure = FeeStructure.objects.create(**data)
        return fee_structure
    
    @staticmethod
    def update_fee_structure(
        fee_structure_id: int,
        data: Dict[str, Any]
    ) -> FeeStructure:
        """
        Update fee structure
        
        Args:
            fee_structure_id: Fee structure ID
            data: Updated data
        
        Returns:
            Updated fee structure
        
        Raises:
            EMISException: If fee structure not found
        """
        try:
            fee_structure = FeeStructure.objects.get(id=fee_structure_id)
        except FeeStructure.DoesNotExist:
            raise EMISException(
                code="FINANCE_101",
                message=f"Fee structure with id {fee_structure_id} not found"
            )
        
        # Recalculate total if components changed
        if data.get('components'):
            total = sum(float(v) for v in data['components'].values())
            data['total_amount'] = Decimal(str(total))
        
        for key, value in data.items():
            setattr(fee_structure, key, value)
        
        fee_structure.save()
        return fee_structure
    
    @staticmethod
    def get_fee_structure(fee_structure_id: int) -> FeeStructure:
        """
        Get fee structure by ID
        
        Args:
            fee_structure_id: Fee structure ID
        
        Returns:
            Fee structure
        
        Raises:
            EMISException: If fee structure not found
        """
        try:
            return FeeStructure.objects.get(id=fee_structure_id)
        except FeeStructure.DoesNotExist:
            raise EMISException(
                code="FINANCE_101",
                message=f"Fee structure with id {fee_structure_id} not found"
            )
    
    @staticmethod
    def list_fee_structures(
        program: Optional[str] = None,
        academic_year: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> QuerySet[FeeStructure]:
        """
        List fee structures with optional filters
        
        Args:
            program: Filter by program
            academic_year: Filter by academic year
            is_active: Filter by active status
            search: Search in name or code
        
        Returns:
            QuerySet of fee structures
        """
        queryset = FeeStructure.objects.all()
        
        if program:
            queryset = queryset.filter(program__icontains=program)
        
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def delete_fee_structure(fee_structure_id: int) -> None:
        """
        Delete fee structure (soft delete by setting is_active=False)
        
        Args:
            fee_structure_id: Fee structure ID
        
        Raises:
            EMISException: If fee structure not found or has associated invoices
        """
        try:
            fee_structure = FeeStructure.objects.get(id=fee_structure_id)
        except FeeStructure.DoesNotExist:
            raise EMISException(
                code="FINANCE_101",
                message=f"Fee structure with id {fee_structure_id} not found"
            )
        
        # Check if has associated invoices
        if fee_structure.invoices.exists():
            raise EMISException(
                code="FINANCE_102",
                message="Cannot delete fee structure with associated invoices"
            )
        
        # Soft delete
        fee_structure.is_active = False
        fee_structure.save()
    
    @staticmethod
    def get_active_fee_structure_for_program(
        program: str,
        academic_year: Optional[str] = None
    ) -> Optional[FeeStructure]:
        """
        Get active fee structure for a program
        
        Args:
            program: Program name
            academic_year: Academic year (optional)
        
        Returns:
            Active fee structure or None
        """
        queryset = FeeStructure.objects.filter(
            program=program,
            is_active=True,
            valid_from__lte=date.today(),
            valid_to__gte=date.today()
        )
        
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        return queryset.first()
