"""
Transport Service for EMIS
Handles transport management, routes, and vehicle tracking
"""
from typing import List, Optional, Dict
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from src.models.transport import Vehicle, Route, RouteStop, StudentTransport, VehicleMaintenance
from src.models.billing import Bill, BillItem, BillType
from src.lib.logging import get_logger

logger = get_logger(__name__)


class TransportService:
    """Service for transport management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Vehicle Management
    def create_vehicle(self, vehicle_data: dict) -> Vehicle:
        """Create a new vehicle"""
        try:
            vehicle = Vehicle(**vehicle_data)
            self.db.add(vehicle)
            self.db.commit()
            self.db.refresh(vehicle)
            logger.info(f"Vehicle created: {vehicle.id} - {vehicle.vehicle_number}")
            return vehicle
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating vehicle: {str(e)}")
            raise
    
    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        """Get vehicle by ID"""
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    def get_vehicles(
        self,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Vehicle]:
        """Get all vehicles"""
        query = self.db.query(Vehicle)
        
        if is_active is not None:
            query = query.filter(Vehicle.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def update_vehicle(self, vehicle_id: int, vehicle_data: dict) -> Optional[Vehicle]:
        """Update vehicle"""
        try:
            vehicle = self.get_vehicle(vehicle_id)
            if not vehicle:
                return None
            
            for key, value in vehicle_data.items():
                setattr(vehicle, key, value)
            
            self.db.commit()
            self.db.refresh(vehicle)
            logger.info(f"Vehicle updated: {vehicle_id}")
            return vehicle
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating vehicle: {str(e)}")
            raise
    
    # Route Management
    def create_route(self, route_data: dict, stops_data: List[dict] = None) -> Route:
        """Create a new route with stops"""
        try:
            route = Route(**route_data)
            self.db.add(route)
            self.db.flush()
            
            if stops_data:
                for stop_data in stops_data:
                    stop = RouteStop(route_id=route.id, **stop_data)
                    self.db.add(stop)
            
            self.db.commit()
            self.db.refresh(route)
            logger.info(f"Route created: {route.id} - {route.route_name}")
            return route
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating route: {str(e)}")
            raise
    
    def get_route(self, route_id: int) -> Optional[Route]:
        """Get route by ID"""
        return self.db.query(Route).filter(Route.id == route_id).first()
    
    def get_routes(
        self,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Route]:
        """Get all routes"""
        query = self.db.query(Route)
        
        if is_active is not None:
            query = query.filter(Route.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def add_route_stop(self, route_id: int, stop_data: dict) -> RouteStop:
        """Add a stop to a route"""
        try:
            stop = RouteStop(route_id=route_id, **stop_data)
            self.db.add(stop)
            self.db.commit()
            self.db.refresh(stop)
            logger.info(f"Route stop added: {stop.id} to route {route_id}")
            return stop
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding route stop: {str(e)}")
            raise
    
    def optimize_route(self, route_id: int) -> Dict:
        """Optimize route based on stops (basic implementation)"""
        route = self.get_route(route_id)
        if not route:
            raise ValueError("Route not found")
        
        stops = self.db.query(RouteStop).filter(
            RouteStop.route_id == route_id
        ).order_by(RouteStop.sequence_number).all()
        
        # Calculate total distance and estimated time
        total_distance = sum(stop.distance_from_start or 0 for stop in stops)
        total_time_minutes = sum(stop.time_from_start or 0 for stop in stops)
        
        # Count students per stop
        students_per_stop = {}
        for stop in stops:
            count = self.db.query(func.count(StudentTransport.id)).filter(
                StudentTransport.route_id == route_id,
                StudentTransport.stop_id == stop.id,
                StudentTransport.status == True
            ).scalar()
            students_per_stop[stop.id] = count
        
        return {
            "route_id": route_id,
            "total_stops": len(stops),
            "total_distance_km": total_distance,
            "estimated_time_minutes": total_time_minutes,
            "students_per_stop": students_per_stop,
            "total_students": sum(students_per_stop.values()),
            "capacity_utilization": (sum(students_per_stop.values()) / route.vehicle.capacity * 100) if route.vehicle else 0
        }
    
    # Student Transport Allocation
    def allocate_transport(
        self,
        student_id: int,
        route_id: int,
        stop_id: int,
        start_date: date,
        monthly_fee: float
    ) -> StudentTransport:
        """Allocate transport to a student"""
        try:
            # Check if student already has active allocation
            existing = self.db.query(StudentTransport).filter(
                StudentTransport.student_id == student_id,
                StudentTransport.is_active == True
            ).first()
            
            if existing:
                raise ValueError("Student already has active transport allocation")
            
            allocation = StudentTransport(
                student_id=student_id,
                route_id=route_id,
                stop_id=stop_id,
                start_date=start_date,
                monthly_fee=monthly_fee,
                is_active=True
            )
            
            self.db.add(allocation)
            self.db.commit()
            self.db.refresh(allocation)
            
            logger.info(f"Transport allocated: Student {student_id} to Route {route_id}")
            return allocation
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error allocating transport: {str(e)}")
            raise
    
    def deallocate_transport(self, allocation_id: int) -> StudentTransport:
        """Deallocate transport from student"""
        try:
            allocation = self.db.query(StudentTransport).filter(
                StudentTransport.id == allocation_id
            ).first()
            
            if not allocation:
                raise ValueError("Allocation not found")
            
            allocation.is_active = False
            allocation.end_date = date.today()
            
            self.db.commit()
            self.db.refresh(allocation)
            logger.info(f"Transport deallocated: {allocation_id}")
            return allocation
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deallocating transport: {str(e)}")
            raise
    
    def get_student_transport(self, student_id: int) -> Optional[StudentTransport]:
        """Get active transport allocation for student"""
        return self.db.query(StudentTransport).filter(
            StudentTransport.student_id == student_id,
            StudentTransport.is_active == True
        ).first()
    
    def get_route_students(self, route_id: int) -> List[StudentTransport]:
        """Get all students allocated to a route"""
        return self.db.query(StudentTransport).filter(
            StudentTransport.route_id == route_id,
            StudentTransport.is_active == True
        ).all()
    
    # Vehicle Maintenance
    def create_maintenance_record(self, maintenance_data: dict) -> VehicleMaintenance:
        """Create maintenance record"""
        try:
            maintenance = VehicleMaintenance(**maintenance_data)
            self.db.add(maintenance)
            self.db.commit()
            self.db.refresh(maintenance)
            logger.info(f"Maintenance record created: {maintenance.id}")
            return maintenance
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating maintenance record: {str(e)}")
            raise
    
    def get_vehicle_maintenance_history(
        self,
        vehicle_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[VehicleMaintenance]:
        """Get maintenance history for vehicle"""
        query = self.db.query(VehicleMaintenance).filter(
            VehicleMaintenance.vehicle_id == vehicle_id
        )
        
        if start_date:
            query = query.filter(VehicleMaintenance.maintenance_date >= start_date)
        if end_date:
            query = query.filter(VehicleMaintenance.maintenance_date <= end_date)
        
        return query.order_by(VehicleMaintenance.maintenance_date.desc()).all()
    
    def get_upcoming_maintenance(self) -> List[VehicleMaintenance]:
        """Get scheduled maintenance"""
        return self.db.query(VehicleMaintenance).filter(
            VehicleMaintenance.next_maintenance_date != None,
            VehicleMaintenance.next_maintenance_date >= date.today()
        ).order_by(VehicleMaintenance.next_maintenance_date).all()
    
    # Statistics and Reports
    def get_transport_statistics(self) -> Dict:
        """Get overall transport statistics"""
        total_vehicles = self.db.query(func.count(Vehicle.id)).filter(
            Vehicle.is_active == True
        ).scalar()
        
        total_routes = self.db.query(func.count(Route.id)).filter(
            Route.is_active == True
        ).scalar()
        
        total_students = self.db.query(func.count(StudentTransport.id)).filter(
            StudentTransport.is_active == True
        ).scalar()
        
        total_capacity = self.db.query(func.sum(Vehicle.capacity)).filter(
            Vehicle.is_active == True
        ).scalar() or 0
        
        utilization = (total_students / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            "total_vehicles": total_vehicles,
            "total_routes": total_routes,
            "total_students": total_students,
            "total_capacity": total_capacity,
            "capacity_utilization": round(utilization, 2),
            "available_seats": total_capacity - total_students
        }
    
    def get_route_report(self, route_id: int) -> Dict:
        """Get detailed report for a route"""
        route = self.get_route(route_id)
        if not route:
            return {}
        
        students = self.get_route_students(route_id)
        stops = self.db.query(RouteStop).filter(
            RouteStop.route_id == route_id
        ).order_by(RouteStop.sequence_number).all()
        
        optimization = self.optimize_route(route_id)
        
        return {
            "route": {
                "id": route.id,
                "name": route.route_name,
                "vehicle": route.vehicle.vehicle_number if route.vehicle else None,
                "is_active": route.is_active
            },
            "students": {
                "total": len(students),
                "list": students
            },
            "stops": {
                "total": len(stops),
                "list": stops
            },
            "optimization": optimization
        }
