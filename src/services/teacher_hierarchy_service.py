"""Teacher Hierarchy Service"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional, Dict
from datetime import date

from src.models.teacher_hierarchy import TeacherHierarchy, DepartmentHierarchy
from src.models.employee import Employee


class TeacherHierarchyService:
    """Service for managing teacher organizational hierarchy"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def set_teacher_hierarchy(
        self,
        teacher_id: int,
        designation: str,
        department_id: Optional[int] = None,
        reports_to: Optional[int] = None,
        is_department_head: bool = False,
        is_program_coordinator: bool = False,
        program_id: Optional[int] = None,
        subject_coordinator_ids: Optional[List[int]] = None,
        effective_from: Optional[date] = None
    ) -> TeacherHierarchy:
        """Set or update teacher hierarchy"""
        
        # Close any existing active hierarchy for this teacher
        stmt = select(TeacherHierarchy).where(
            and_(
                TeacherHierarchy.teacher_id == teacher_id,
                TeacherHierarchy.effective_to.is_(None)
            )
        )
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.effective_to = date.today()
            await self.db.commit()
        
        # Create new hierarchy entry
        hierarchy = TeacherHierarchy(
            teacher_id=teacher_id,
            designation=designation,
            department_id=department_id,
            reports_to=reports_to,
            is_department_head=is_department_head,
            is_program_coordinator=is_program_coordinator,
            program_id=program_id,
            subject_coordinator_ids=subject_coordinator_ids or [],
            effective_from=effective_from or date.today(),
            hierarchy_level=self._get_hierarchy_level(designation)
        )
        
        self.db.add(hierarchy)
        await self.db.commit()
        await self.db.refresh(hierarchy)
        
        return hierarchy
    
    def _get_hierarchy_level(self, designation: str) -> int:
        """Determine hierarchy level from designation"""
        levels = {
            "Director": 1,
            "Dean": 1,
            "Head of Department": 2,
            "HOD": 2,
            "Professor": 3,
            "Associate Professor": 4,
            "Assistant Professor": 5,
            "Senior Lecturer": 5,
            "Lecturer": 6,
            "Teaching Assistant": 7,
            "TA": 7
        }
        return levels.get(designation, 5)
    
    async def get_teacher_hierarchy(self, teacher_id: int) -> Optional[TeacherHierarchy]:
        """Get current active hierarchy for a teacher"""
        stmt = select(TeacherHierarchy).where(
            and_(
                TeacherHierarchy.teacher_id == teacher_id,
                TeacherHierarchy.effective_to.is_(None)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_department_hierarchy(self, department_id: int) -> List[Dict]:
        """Get all teachers in a department with hierarchy"""
        stmt = select(TeacherHierarchy).where(
            and_(
                TeacherHierarchy.department_id == department_id,
                TeacherHierarchy.effective_to.is_(None)
            )
        ).order_by(TeacherHierarchy.hierarchy_level)
        
        result = await self.db.execute(stmt)
        hierarchies = result.scalars().all()
        
        # Build hierarchy tree
        hierarchy_tree = []
        for h in hierarchies:
            hierarchy_tree.append({
                "teacher_id": h.teacher_id,
                "designation": h.designation,
                "level": h.hierarchy_level,
                "reports_to": h.reports_to,
                "is_hod": h.is_department_head,
                "is_coordinator": h.is_program_coordinator
            })
        
        return hierarchy_tree
    
    async def get_subordinates(self, teacher_id: int) -> List[TeacherHierarchy]:
        """Get all subordinates of a teacher"""
        stmt = select(TeacherHierarchy).where(
            and_(
                TeacherHierarchy.reports_to == teacher_id,
                TeacherHierarchy.effective_to.is_(None)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_org_chart(self) -> Dict:
        """Get complete organization chart"""
        stmt = select(TeacherHierarchy).where(
            TeacherHierarchy.effective_to.is_(None)
        ).order_by(TeacherHierarchy.hierarchy_level)
        
        result = await self.db.execute(stmt)
        all_hierarchies = result.scalars().all()
        
        # Build tree structure
        hierarchy_map = {}
        for h in all_hierarchies:
            hierarchy_map[h.teacher_id] = {
                "id": h.teacher_id,
                "designation": h.designation,
                "department_id": h.department_id,
                "level": h.hierarchy_level,
                "reports_to": h.reports_to,
                "is_hod": h.is_department_head,
                "subordinates": []
            }
        
        # Link subordinates
        for teacher_id, data in hierarchy_map.items():
            if data["reports_to"] and data["reports_to"] in hierarchy_map:
                hierarchy_map[data["reports_to"]]["subordinates"].append(data)
        
        # Find top-level (no supervisor)
        top_level = [data for data in hierarchy_map.values() if not data["reports_to"]]
        
        return {
            "organization": top_level,
            "total_teachers": len(hierarchy_map)
        }
    
    async def set_department_hierarchy(
        self,
        department_id: int,
        parent_department_id: Optional[int] = None,
        head_of_department_id: Optional[int] = None,
        annual_budget: Optional[float] = None
    ) -> DepartmentHierarchy:
        """Set or update department hierarchy"""
        
        stmt = select(DepartmentHierarchy).where(
            DepartmentHierarchy.department_id == department_id
        )
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.parent_department_id = parent_department_id
            existing.head_of_department_id = head_of_department_id
            if annual_budget is not None:
                existing.annual_budget = annual_budget
            existing.hierarchy_level = await self._calculate_dept_level(parent_department_id)
        else:
            existing = DepartmentHierarchy(
                department_id=department_id,
                parent_department_id=parent_department_id,
                head_of_department_id=head_of_department_id,
                annual_budget=annual_budget,
                hierarchy_level=await self._calculate_dept_level(parent_department_id)
            )
            self.db.add(existing)
        
        await self.db.commit()
        await self.db.refresh(existing)
        return existing
    
    async def _calculate_dept_level(self, parent_id: Optional[int]) -> int:
        """Calculate department hierarchy level"""
        if not parent_id:
            return 1
        
        stmt = select(DepartmentHierarchy).where(
            DepartmentHierarchy.department_id == parent_id
        )
        result = await self.db.execute(stmt)
        parent = result.scalar_one_or_none()
        
        return parent.hierarchy_level + 1 if parent else 1
    
    async def get_teachers_by_designation(self, designation: str) -> List[TeacherHierarchy]:
        """Get all teachers with a specific designation"""
        stmt = select(TeacherHierarchy).where(
            and_(
                TeacherHierarchy.designation == designation,
                TeacherHierarchy.effective_to.is_(None)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_department_heads(self) -> List[TeacherHierarchy]:
        """Get all department heads"""
        stmt = select(TeacherHierarchy).where(
            and_(
                TeacherHierarchy.is_department_head == True,
                TeacherHierarchy.effective_to.is_(None)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
