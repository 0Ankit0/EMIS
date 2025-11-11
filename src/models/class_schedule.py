"""Class Schedule Models for EMIS"""
from datetime import time, date
from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class DayOfWeek(str, enum.Enum):
    """Enumeration for days of the week"""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class ClassSchedule(Base):
    """Class Schedule model for managing course timetables"""
    __tablename__ = "class_schedules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    room_number = Column(String(50), nullable=True)
    building = Column(String(100), nullable=True)
    
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(String(500), nullable=True)
    
    # Relationships
    course = relationship("Course", back_populates="schedules")
    instructor = relationship("Employee", foreign_keys=[instructor_id])
    
    def __repr__(self):
        return f"<ClassSchedule(id={self.id}, course_id={self.course_id}, day={self.day_of_week}, time={self.start_time}-{self.end_time})>"
