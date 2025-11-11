"""
Transport Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from src.database import get_db
from src.services.transport_service import TransportService
from src.middleware.rbac import get_current_user
from src.models.auth import User

router = APIRouter(prefix="/api/transport", tags=["Transport"])


# Pydantic Models
class VehicleCreate(BaseModel):
    vehicle_number: str
    vehicle_type: str
    capacity: int
    driver_name: Optional[str] = None
    driver_contact: Optional[str] = None
    driver_license: Optional[str] = None


class RouteCreate(BaseModel):
    route_name: str
    route_code: Optional[str] = None
    vehicle_id: Optional[int] = None
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None


class RouteStopCreate(BaseModel):
    stop_name: str
    sequence_number: int
    arrival_time: Optional[str] = None
    departure_time: Optional[str] = None
    distance_from_start: Optional[float] = None


class TransportAllocationCreate(BaseModel):
    student_id: int
    route_id: int
    stop_id: int
    start_date: date
    monthly_fee: float


class MaintenanceCreate(BaseModel):
    vehicle_id: int
    maintenance_date: date
    maintenance_type: str
    description: Optional[str] = None
    cost: Optional[float] = None
    next_maintenance_date: Optional[date] = None


# Vehicle Endpoints
@router.post("/vehicles", response_model=dict)
def create_vehicle(
    vehicle_data: VehicleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new vehicle"""
    service = TransportService(db)
    vehicle = service.create_vehicle(vehicle_data.dict())
    return {"message": "Vehicle created successfully", "vehicle_id": vehicle.id}


@router.get("/vehicles", response_model=List[dict])
def get_vehicles(
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all vehicles"""
    service = TransportService(db)
    vehicles = service.get_vehicles(is_active=is_active, skip=skip, limit=limit)
    return [
        {
            "id": v.id,
            "vehicle_number": v.vehicle_number,
            "vehicle_type": v.vehicle_type,
            "capacity": v.capacity,
            "driver_name": v.driver_name,
            "is_active": v.is_active
        }
        for v in vehicles
    ]


@router.get("/vehicles/{vehicle_id}", response_model=dict)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Get vehicle details"""
    service = TransportService(db)
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return {
        "id": vehicle.id,
        "vehicle_number": vehicle.vehicle_number,
        "vehicle_type": vehicle.vehicle_type,
        "capacity": vehicle.capacity,
        "driver_name": vehicle.driver_name,
        "driver_contact": vehicle.driver_contact,
        "is_active": vehicle.is_active
    }


# Route Endpoints
@router.post("/routes", response_model=dict)
def create_route(
    route_data: RouteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new route"""
    service = TransportService(db)
    route = service.create_route(route_data.dict())
    return {"message": "Route created successfully", "route_id": route.id}


@router.get("/routes", response_model=List[dict])
def get_routes(
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all routes"""
    service = TransportService(db)
    routes = service.get_routes(is_active=is_active, skip=skip, limit=limit)
    return [
        {
            "id": r.id,
            "route_name": r.route_name,
            "route_code": r.route_code,
            "vehicle_number": r.vehicle.vehicle_number if r.vehicle else None,
            "is_active": r.is_active
        }
        for r in routes
    ]


@router.get("/routes/{route_id}", response_model=dict)
def get_route(route_id: int, db: Session = Depends(get_db)):
    """Get route details"""
    service = TransportService(db)
    route = service.get_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return {
        "id": route.id,
        "route_name": route.route_name,
        "route_code": route.route_code,
        "vehicle_id": route.vehicle_id,
        "start_location": route.start_location,
        "end_location": route.end_location,
        "is_active": route.is_active
    }


@router.post("/routes/{route_id}/stops", response_model=dict)
def add_route_stop(
    route_id: int,
    stop_data: RouteStopCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a stop to route"""
    service = TransportService(db)
    stop = service.add_route_stop(route_id, stop_data.dict())
    return {"message": "Route stop added", "stop_id": stop.id}


@router.get("/routes/{route_id}/optimize", response_model=dict)
def optimize_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get route optimization details"""
    service = TransportService(db)
    try:
        return service.optimize_route(route_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Student Allocation Endpoints
@router.post("/allocations", response_model=dict)
def allocate_transport(
    allocation_data: TransportAllocationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Allocate transport to student"""
    service = TransportService(db)
    try:
        allocation = service.allocate_transport(**allocation_data.dict())
        return {"message": "Transport allocated successfully", "allocation_id": allocation.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/allocations/{allocation_id}", response_model=dict)
def deallocate_transport(
    allocation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deallocate transport from student"""
    service = TransportService(db)
    try:
        allocation = service.deallocate_transport(allocation_id)
        return {"message": "Transport deallocated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/students/{student_id}/allocation", response_model=dict)
def get_student_transport(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get student's transport allocation"""
    service = TransportService(db)
    allocation = service.get_student_transport(student_id)
    if not allocation:
        return {"message": "No active transport allocation"}
    
    return {
        "id": allocation.id,
        "route_name": allocation.route.route_name,
        "stop": allocation.stop.stop_name,
        "start_date": allocation.start_date,
        "monthly_fee": float(allocation.monthly_fee),
        "is_active": allocation.is_active
    }


@router.get("/routes/{route_id}/students", response_model=List[dict])
def get_route_students(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get students allocated to route"""
    service = TransportService(db)
    allocations = service.get_route_students(route_id)
    return [
        {
            "student_id": a.student_id,
            "student_name": a.student.full_name if a.student else None,
            "stop": a.stop.stop_name
        }
        for a in allocations
    ]


# Maintenance Endpoints
@router.post("/maintenance", response_model=dict)
def create_maintenance_record(
    maintenance_data: MaintenanceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create vehicle maintenance record"""
    service = TransportService(db)
    maintenance = service.create_maintenance_record(maintenance_data.dict())
    return {"message": "Maintenance record created", "maintenance_id": maintenance.id}


@router.get("/vehicles/{vehicle_id}/maintenance", response_model=List[dict])
def get_vehicle_maintenance(
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get vehicle maintenance history"""
    service = TransportService(db)
    records = service.get_vehicle_maintenance_history(vehicle_id)
    return [
        {
            "id": m.id,
            "maintenance_date": m.maintenance_date,
            "maintenance_type": m.maintenance_type,
            "cost": float(m.cost) if m.cost else 0,
            "next_maintenance_date": m.next_maintenance_date
        }
        for m in records
    ]


@router.get("/maintenance/upcoming", response_model=List[dict])
def get_upcoming_maintenance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get upcoming maintenance"""
    service = TransportService(db)
    records = service.get_upcoming_maintenance()
    return [
        {
            "id": m.id,
            "vehicle_number": m.vehicle.vehicle_number,
            "next_maintenance_date": m.next_maintenance_date,
            "maintenance_type": m.maintenance_type
        }
        for m in records
    ]


# Statistics
@router.get("/statistics", response_model=dict)
def get_transport_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get transport statistics"""
    service = TransportService(db)
    return service.get_transport_statistics()


@router.get("/routes/{route_id}/report", response_model=dict)
def get_route_report(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed route report"""
    service = TransportService(db)
    return service.get_route_report(route_id)
