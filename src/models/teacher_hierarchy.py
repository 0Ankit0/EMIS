"""Teacher hierarchy models for organizational structure"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, ARRAY
from sqlalchemy.orm import relationship
from datetime import date
from typing import Optional, List

from src.database import Base


class TeacherHierarchy(Base):
    """Teacher organizational hierarchy and reporting structure"""
    
    __tablename__ = "teacher_hierarchy"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    designation = Column(String(100), nullable=False)  # HOD, Professor, Associate Prof, etc.
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    reports_to = Column(Integer, ForeignKey("employees.id"), nullable=True)  # Supervisor
    hierarchy_level = Column(Integer, nullable=False, default=3)  # 1=Top, 5=Bottom
    
    # Special roles
    is_department_head = Column(Boolean, default=False)
    is_program_coordinator = Column(Boolean, default=False)
    program_id = Column(Integer, nullable=True)
    subject_coordinator_ids = Column(ARRAY(Integer), nullable=True)
    
    # Validity period
    effective_from = Column(Date, nullable=False, default=date.today)
    effective_to = Column(Date, nullable=True)
    
    # Relationships
    teacher = relationship("Employee", foreign_keys=[teacher_id], backref="hierarchy_info")
    supervisor = relationship("Employee", foreign_keys=[reports_to], backref="subordinates")
    department = relationship("Department", backref="hierarchy_members")
    
    def __repr__(self):
        return f"<TeacherHierarchy(teacher={self.teacher_id}, designation={self.designation}, level={self.hierarchy_level})>"
    
    @property
    def is_active(self) -> bool:
        """Check if hierarchy entry is currently active"""
        today = date.today()
        if self.effective_to and self.effective_to < today:
            return False
        return self.effective_from <= today
    
    def get_designation_level(self) -> int:
        """Get numerical level based on designation"""
        designation_levels = {
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
        return designation_levels.get(self.designation, 5)
    
    def get_permissions(self) -> List[str]:
        """Get permissions based on role and designation"""
        permissions = ["view_own_salary", "submit_expense_claim"]
        
        if self.is_department_head:
            permissions.extend([
                "view_department_reports",
                "view_department_salary",
                "approve_department_expenses",
                "view_department_students",
                "view_department_analytics"
            ])
        
        if self.is_program_coordinator:
            permissions.extend([
                "view_program_reports",
                "view_program_students",
                "view_program_analytics"
            ])
        
        if self.subject_coordinator_ids:
            permissions.extend([
                "view_subject_reports",
                "view_subject_students"
            ])
        
        if self.hierarchy_level <= 3:  # Senior roles
            permissions.extend([
                "view_student_reports",
                "access_advanced_analytics"
            ])
        
        return list(set(permissions))


class DepartmentHierarchy(Base):
    """Department structure and parent-child relationships"""
    
    __tablename__ = "department_hierarchy"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, unique=True)
    parent_department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    hierarchy_level = Column(Integer, nullable=False, default=1)
    head_of_department_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Budget allocation
    annual_budget = Column(Integer, nullable=True)  # For expense tracking
    
    # Relationships
    department = relationship("Department", foreign_keys=[department_id], backref="hierarchy")
    parent_department = relationship("Department", foreign_keys=[parent_department_id])
    hod = relationship("Employee", backref="headed_department")
    
    def __repr__(self):
        return f"<DepartmentHierarchy(dept={self.department_id}, level={self.hierarchy_level})>"
