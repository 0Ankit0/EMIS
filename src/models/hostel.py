"""Hostel Management Models for EMIS"""
from datetime import datetime, date, time
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time, Float, Boolean, Enum, Text
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class RoomType(str, enum.Enum):
    """Room types in hostel"""
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    QUAD = "quad"
    DORMITORY = "dormitory"


class RoomStatus(str, enum.Enum):
    """Room status"""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    RESERVED = "reserved"


# T133: Hostel model
class Hostel(Base):
    """Hostel/Dormitory model"""
    __tablename__ = "hostels"

    id = Column(Integer, primary_key=True, index=True)
    
    # Basic details
    hostel_name = Column(String(200), nullable=False)
    hostel_code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Type and capacity
    gender = Column(String(20), nullable=False)  # male, female, co-ed
    total_capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, default=0, nullable=False)
    
    # Location
    building = Column(String(100), nullable=True)
    floor_count = Column(Integer, nullable=True)
    address = Column(Text, nullable=True)
    
    # Facilities
    has_mess = Column(Boolean, default=False, nullable=False)
    has_gym = Column(Boolean, default=False, nullable=False)
    has_common_room = Column(Boolean, default=False, nullable=False)
    has_laundry = Column(Boolean, default=False, nullable=False)
    has_wifi = Column(Boolean, default=True, nullable=False)
    
    # Warden details
    warden_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    assistant_warden_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    
    # Fees
    monthly_fee = Column(Float, nullable=False)
    security_deposit = Column(Float, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Hostel rules
    check_in_time = Column(Time, nullable=True)
    check_out_time = Column(Time, nullable=True)
    visitor_hours_start = Column(Time, nullable=True)
    visitor_hours_end = Column(Time, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    warden = relationship("Employee", foreign_keys=[warden_id])
    assistant_warden = relationship("Employee", foreign_keys=[assistant_warden_id])
    rooms = relationship("Room", back_populates="hostel", cascade="all, delete-orphan")
    allocations = relationship("RoomAllocation", back_populates="hostel")
    
    def __repr__(self):
        return f"<Hostel(id={self.id}, name={self.hostel_name}, code={self.hostel_code})>"


# T134: Room model
class Room(Base):
    """Room model for hostel rooms"""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    
    # Room details
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False)
    room_number = Column(String(50), nullable=False)
    floor = Column(Integer, nullable=False)
    
    # Room type and capacity
    room_type = Column(Enum(RoomType), nullable=False)
    bed_capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, default=0, nullable=False)
    
    # Facilities
    has_ac = Column(Boolean, default=False, nullable=False)
    has_attached_bathroom = Column(Boolean, default=True, nullable=False)
    has_balcony = Column(Boolean, default=False, nullable=False)
    
    # Status and fees
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE, nullable=False)
    monthly_rent = Column(Float, nullable=False)
    
    # Maintenance
    last_maintenance_date = Column(Date, nullable=True)
    next_maintenance_date = Column(Date, nullable=True)
    maintenance_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    hostel = relationship("Hostel", back_populates="rooms")
    allocations = relationship("RoomAllocation", back_populates="room")
    
    def __repr__(self):
        return f"<Room(id={self.id}, number={self.room_number}, hostel_id={self.hostel_id})>"


# T135: RoomAllocation model
class RoomAllocation(Base):
    """Room allocation to students"""
    __tablename__ = "room_allocations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Allocation details
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    bed_number = Column(Integer, nullable=False)
    
    # Period
    allocation_date = Column(Date, default=date.today, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    check_in_date = Column(DateTime, nullable=True)
    check_out_date = Column(DateTime, nullable=True)
    
    # Fees
    monthly_fee = Column(Float, nullable=False)
    security_deposit_paid = Column(Float, default=0.0, nullable=False)
    security_deposit_refunded = Column(Boolean, default=False, nullable=False)
    
    # Academic context
    academic_year = Column(String(20), nullable=False)
    semester = Column(Integer, nullable=True)
    
    # Notes
    special_requirements = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Approval
    allocated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    hostel = relationship("Hostel", back_populates="allocations")
    room = relationship("Room", back_populates="allocations")
    student = relationship("Student", back_populates="hostel_allocations")
    allocator = relationship("User", foreign_keys=[allocated_by])
    
    def __repr__(self):
        return f"<RoomAllocation(id={self.id}, student_id={self.student_id}, room_id={self.room_id})>"


# T136: MessMenu model
class MessMenu(Base):
    """Mess menu for hostel dining"""
    __tablename__ = "mess_menus"

    id = Column(Integer, primary_key=True, index=True)
    
    # Menu details
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(String(20), nullable=False)  # Monday, Tuesday, etc.
    meal_type = Column(String(20), nullable=False)  # breakfast, lunch, dinner, snacks
    
    # Menu items
    menu_items = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    # Effective period
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    # Nutritional info (optional)
    calories = Column(Integer, nullable=True)
    is_vegetarian = Column(Boolean, default=True, nullable=False)
    is_vegan = Column(Boolean, default=False, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    hostel = relationship("Hostel")
    
    def __repr__(self):
        return f"<MessMenu(id={self.id}, hostel_id={self.hostel_id}, day={self.day_of_week}, meal={self.meal_type})>"


# T137: HostelVisitor model
class HostelVisitor(Base):
    """Hostel visitor tracking"""
    __tablename__ = "hostel_visitors"

    id = Column(Integer, primary_key=True, index=True)
    
    # Visitor details
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Visitor information
    visitor_name = Column(String(200), nullable=False)
    visitor_phone = Column(String(20), nullable=True)
    relationship = Column(String(100), nullable=True)  # parent, relative, friend
    
    # Visit details
    visit_date = Column(Date, default=date.today, nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=True)
    
    # Purpose and approval
    purpose = Column(String(200), nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # ID proof
    id_proof_type = Column(String(50), nullable=True)  # aadhar, license, etc.
    id_proof_number = Column(String(100), nullable=True)
    
    # Status
    is_checked_out = Column(Boolean, default=False, nullable=False)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    hostel = relationship("Hostel")
    student = relationship("Student")
    approver = relationship("User", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<HostelVisitor(id={self.id}, visitor={self.visitor_name}, student_id={self.student_id})>"


# T138: HostelComplaint model
class HostelComplaint(Base):
    """Hostel complaints and issues"""
    __tablename__ = "hostel_complaints"

    id = Column(Integer, primary_key=True, index=True)
    
    # Complaint details
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Complaint information
    complaint_number = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False)  # maintenance, cleanliness, noise, etc.
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    
    # Priority
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    
    # Status
    status = Column(String(50), default="open", nullable=False)  # open, in_progress, resolved, closed
    
    # Dates
    complaint_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    acknowledged_date = Column(DateTime, nullable=True)
    resolved_date = Column(DateTime, nullable=True)
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    
    # Resolution
    resolution_notes = Column(Text, nullable=True)
    resolved_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    
    # Feedback
    student_feedback = Column(Text, nullable=True)
    satisfaction_rating = Column(Integer, nullable=True)  # 1-5 scale
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    hostel = relationship("Hostel")
    room = relationship("Room")
    student = relationship("Student")
    assignee = relationship("Employee", foreign_keys=[assigned_to])
    resolver = relationship("Employee", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<HostelComplaint(id={self.id}, number={self.complaint_number}, status={self.status})>"
