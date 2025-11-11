"""
Transport Management Models for EMIS
"""
from datetime import datetime, date, time
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Time, Numeric, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class VehicleStatus(str, Enum):
    """Vehicle status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    BREAKDOWN = "breakdown"
    DISPOSED = "disposed"


class Vehicle(Base):
    """Vehicle model"""
    __tablename__ = "vehicles"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Vehicle details
    vehicle_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    vehicle_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Bus, Van, Car
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer)
    
    # Capacity
    seating_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Status
    status: Mapped[VehicleStatus] = mapped_column(String(50), default=VehicleStatus.ACTIVE, index=True)
    
    # Driver
    driver_name: Mapped[Optional[str]] = mapped_column(String(255))
    driver_phone: Mapped[Optional[str]] = mapped_column(String(20))
    driver_license: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Registration & Insurance
    registration_number: Mapped[str] = mapped_column(String(50), nullable=False)
    registration_expiry: Mapped[Optional[date]] = mapped_column(Date)
    insurance_number: Mapped[Optional[str]] = mapped_column(String(100))
    insurance_expiry: Mapped[Optional[date]] = mapped_column(Date)
    
    # Maintenance
    last_service_date: Mapped[Optional[date]] = mapped_column(Date)
    next_service_date: Mapped[Optional[date]] = mapped_column(Date)
    last_service_km: Mapped[Optional[int]] = mapped_column(Integer)
    current_km: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    routes = relationship("RouteVehicle", back_populates="vehicle")
    maintenance_records = relationship("VehicleMaintenance", back_populates="vehicle", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Vehicle(number='{self.vehicle_number}', type='{self.vehicle_type}')>"


class Route(Base):
    """Transport route model"""
    __tablename__ = "routes"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Route details
    route_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    route_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Distance and timing
    total_distance_km: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    estimated_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Fees
    monthly_fee: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stops = relationship("RouteStop", back_populates="route", cascade="all, delete-orphan", order_by="RouteStop.stop_order")
    vehicles = relationship("RouteVehicle", back_populates="route")
    student_transports = relationship("StudentTransport", back_populates="route")
    
    def __repr__(self) -> str:
        return f"<Route(number='{self.route_number}', name='{self.route_name}')>"


class RouteStop(Base):
    """Route stop model"""
    __tablename__ = "route_stops"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    route_id: Mapped[UUID] = mapped_column(ForeignKey("routes.id"), nullable=False)
    
    # Stop details
    stop_name: Mapped[str] = mapped_column(String(255), nullable=False)
    stop_address: Mapped[Optional[str]] = mapped_column(Text)
    stop_order: Mapped[int] = mapped_column(Integer, nullable=False)  # Sequence in route
    
    # Location
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 8))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(11, 8))
    
    # Timing
    arrival_time: Mapped[Optional[time]] = mapped_column(Time)
    departure_time: Mapped[Optional[time]] = mapped_column(Time)
    
    # Distance from previous stop
    distance_from_previous_km: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    route = relationship("Route", back_populates="stops")
    
    def __repr__(self) -> str:
        return f"<RouteStop(route='{self.route_id}', stop='{self.stop_name}', order={self.stop_order})>"


class RouteVehicle(Base):
    """Route vehicle assignment"""
    __tablename__ = "route_vehicles"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    route_id: Mapped[UUID] = mapped_column(ForeignKey("routes.id"), nullable=False)
    vehicle_id: Mapped[UUID] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    
    # Assignment details
    assigned_from: Mapped[date] = mapped_column(Date, nullable=False)
    assigned_to: Mapped[Optional[date]] = mapped_column(Date)
    
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    route = relationship("Route", back_populates="vehicles")
    vehicle = relationship("Vehicle", back_populates="routes")
    
    def __repr__(self) -> str:
        return f"<RouteVehicle(route='{self.route_id}', vehicle='{self.vehicle_id}')>"


class StudentTransport(Base):
    """Student transport assignment"""
    __tablename__ = "student_transport"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    route_id: Mapped[UUID] = mapped_column(ForeignKey("routes.id"), nullable=False)
    stop_id: Mapped[UUID] = mapped_column(ForeignKey("route_stops.id"), nullable=False)
    
    # Subscription details
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Payment
    monthly_fee: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    route = relationship("Route", back_populates="student_transports")
    stop = relationship("RouteStop")
    
    def __repr__(self) -> str:
        return f"<StudentTransport(student='{self.student_id}', route='{self.route_id}')>"


class MaintenanceType(str, Enum):
    """Maintenance types"""
    ROUTINE = "routine"
    REPAIR = "repair"
    BREAKDOWN = "breakdown"
    INSPECTION = "inspection"
    OTHER = "other"


class VehicleMaintenance(Base):
    """Vehicle maintenance record"""
    __tablename__ = "vehicle_maintenance"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    vehicle_id: Mapped[UUID] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    
    # Maintenance details
    maintenance_type: Mapped[MaintenanceType] = mapped_column(String(50), nullable=False)
    maintenance_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Cost
    cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Odometer
    odometer_reading: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Service provider
    service_provider: Mapped[Optional[str]] = mapped_column(String(255))
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Downtime
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Status
    is_completed: Mapped[bool] = mapped_column(default=False)
    
    # Tracking
    performed_by: Mapped[UUID] = mapped_column(nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="maintenance_records")
    
    def __repr__(self) -> str:
        return f"<VehicleMaintenance(vehicle='{self.vehicle_id}', type='{self.maintenance_type}')>"
