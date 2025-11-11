# Transport API Documentation

## Base URL
`/api/transport`

## Overview
The Transport API manages college transport system including vehicles, routes, student allocations, and maintenance.

## Authentication
All endpoints require authentication.

---

## Endpoints

### Vehicle Management

#### Create Vehicle
```http
POST /api/transport/vehicles
```

**Request Body:**
```json
{
  "vehicle_number": "DL-1234",
  "vehicle_type": "Bus",
  "capacity": 50,
  "driver_name": "Ram Kumar",
  "driver_contact": "+91-9876543210",
  "driver_license": "DL1234567890"
}
```

#### Get All Vehicles
```http
GET /api/transport/vehicles?is_active=true
```

#### Get Vehicle Details
```http
GET /api/transport/vehicles/{vehicle_id}
```

### Route Management

#### Create Route
```http
POST /api/transport/routes
```

**Request Body:**
```json
{
  "route_name": "North Campus Route",
  "route_code": "NC-01",
  "vehicle_id": 1,
  "start_location": "Main Gate",
  "end_location": "College",
  "estimated_duration_minutes": 45
}
```

#### Add Route Stop
```http
POST /api/transport/routes/{route_id}/stops
```

**Request Body:**
```json
{
  "stop_name": "Connaught Place",
  "sequence_number": 1,
  "arrival_time": "07:30:00",
  "departure_time": "07:32:00",
  "distance_from_start": 5.2
}
```

#### Optimize Route
```http
GET /api/transport/routes/{route_id}/optimize
```

**Response:**
```json
{
  "route_id": 1,
  "total_stops": 8,
  "total_distance_km": 25.5,
  "estimated_time_minutes": 45,
  "students_per_stop": {
    "1": 15,
    "2": 12
  },
  "total_students": 75,
  "capacity_utilization": 75.0
}
```

### Student Allocation

#### Allocate Transport
```http
POST /api/transport/allocations
```

**Request Body:**
```json
{
  "student_id": 1001,
  "route_id": 1,
  "pickup_stop_id": 2,
  "drop_stop_id": 2,
  "academic_year_id": 1
}
```

#### Get Student Transport
```http
GET /api/transport/students/{student_id}/allocation
```

**Response:**
```json
{
  "id": 1,
  "route_name": "North Campus Route",
  "pickup_stop": "Connaught Place",
  "drop_stop": "Connaught Place",
  "status": "active"
}
```

#### Deallocate Transport
```http
DELETE /api/transport/allocations/{allocation_id}
```

### Vehicle Maintenance

#### Create Maintenance Record
```http
POST /api/transport/maintenance
```

**Request Body:**
```json
{
  "vehicle_id": 1,
  "maintenance_date": "2024-01-15",
  "maintenance_type": "Regular Service",
  "description": "Oil change and tire rotation",
  "cost": 5000.00,
  "next_maintenance_date": "2024-04-15"
}
```

#### Get Vehicle Maintenance History
```http
GET /api/transport/vehicles/{vehicle_id}/maintenance
```

#### Get Upcoming Maintenance
```http
GET /api/transport/maintenance/upcoming
```

### Reports

#### Get Transport Statistics
```http
GET /api/transport/statistics
```

**Response:**
```json
{
  "total_vehicles": 10,
  "total_routes": 5,
  "total_students": 450,
  "total_capacity": 500,
  "capacity_utilization": 90.0,
  "available_seats": 50
}
```

#### Get Route Report
```http
GET /api/transport/routes/{route_id}/report
```

---

## Data Models

### Vehicle
```json
{
  "id": 1,
  "vehicle_number": "DL-1234",
  "vehicle_type": "Bus",
  "capacity": 50,
  "driver_name": "Ram Kumar",
  "driver_contact": "+91-9876543210",
  "is_active": true
}
```

### Route
```json
{
  "id": 1,
  "route_name": "North Campus Route",
  "route_code": "NC-01",
  "vehicle_id": 1,
  "start_location": "Main Gate",
  "end_location": "College",
  "is_active": true
}
```

### Student Transport
```json
{
  "id": 1,
  "student_id": 1001,
  "route_id": 1,
  "pickup_stop_id": 2,
  "drop_stop_id": 2,
  "status": "active",
  "allocation_date": "2024-01-01"
}
```
