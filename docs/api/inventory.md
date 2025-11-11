# Inventory API Documentation

## Base URL
`/api/inventory`

## Overview
The Inventory API manages college inventory, assets, purchase orders, and stock transactions.

## Authentication
All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Endpoints

### Inventory Management

#### Create Inventory Item
```http
POST /api/inventory/items
```

**Request Body:**
```json
{
  "name": "Projector",
  "description": "HD Projector for classrooms",
  "category_id": 1,
  "quantity": 10,
  "unit_price": 25000.00,
  "reorder_level": 2,
  "location": "Store Room A"
}
```

**Response:**
```json
{
  "message": "Inventory item created successfully",
  "item_id": 123
}
```

#### Get All Inventory Items
```http
GET /api/inventory/items?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 123,
    "name": "Projector",
    "category_name": "Electronics",
    "quantity": 10,
    "unit_price": 25000.00,
    "total_value": 250000.00,
    "reorder_level": 2
  }
]
```

#### Get Inventory Item
```http
GET /api/inventory/items/{item_id}
```

#### Update Inventory Item
```http
PUT /api/inventory/items/{item_id}
```

#### Delete Inventory Item
```http
DELETE /api/inventory/items/{item_id}
```

### Categories

#### Create Category
```http
POST /api/inventory/categories
```

**Request Body:**
```json
{
  "name": "Electronics",
  "description": "Electronic equipment and devices"
}
```

#### Get Categories
```http
GET /api/inventory/categories
```

### Purchase Orders

#### Create Purchase Order
```http
POST /api/inventory/purchase-orders
```

**Request Body:**
```json
{
  "vendor_id": 1,
  "order_date": "2024-01-15",
  "expected_delivery": "2024-01-30",
  "items": [
    {
      "item_id": 123,
      "quantity": 5,
      "unit_price": 25000.00
    }
  ]
}
```

#### Get Purchase Orders
```http
GET /api/inventory/purchase-orders?status=pending
```

#### Approve Purchase Order
```http
POST /api/inventory/purchase-orders/{po_id}/approve
```

#### Receive Purchase Order
```http
POST /api/inventory/purchase-orders/{po_id}/receive
```

### Stock Transactions

#### Create Stock Transaction
```http
POST /api/inventory/transactions
```

**Request Body:**
```json
{
  "item_id": 123,
  "transaction_type": "IN",
  "quantity": 5,
  "reference": "PO-2024-001",
  "remarks": "New stock received"
}
```

#### Get Stock Transactions
```http
GET /api/inventory/transactions?item_id=123
```

### Vendors

#### Create Vendor
```http
POST /api/inventory/vendors
```

**Request Body:**
```json
{
  "name": "ABC Electronics Pvt Ltd",
  "contact_person": "John Doe",
  "email": "john@abcelectronics.com",
  "phone": "+91-9876543210",
  "address": "123 Market Street, Delhi"
}
```

#### Get Vendors
```http
GET /api/inventory/vendors
```

### Reports

#### Get Low Stock Items
```http
GET /api/inventory/reports/low-stock
```

**Response:**
```json
[
  {
    "id": 123,
    "name": "Projector",
    "quantity": 1,
    "reorder_level": 2,
    "status": "Below reorder level"
  }
]
```

#### Get Inventory Summary
```http
GET /api/inventory/reports/summary
```

**Response:**
```json
{
  "total_items": 150,
  "total_value": 5000000.00,
  "low_stock_items": 5,
  "categories": 10
}
```

#### Get Stock Movement Report
```http
GET /api/inventory/reports/stock-movement?start_date=2024-01-01&end_date=2024-01-31
```

---

## Data Models

### Inventory Item
```json
{
  "id": 123,
  "name": "Projector",
  "description": "HD Projector",
  "category_id": 1,
  "quantity": 10,
  "unit_price": 25000.00,
  "reorder_level": 2,
  "location": "Store Room A",
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z"
}
```

### Purchase Order
```json
{
  "id": 1,
  "po_number": "PO-2024-001",
  "vendor_id": 1,
  "order_date": "2024-01-15",
  "expected_delivery": "2024-01-30",
  "status": "pending",
  "total_amount": 125000.00,
  "items": []
}
```

### Stock Transaction
```json
{
  "id": 1,
  "item_id": 123,
  "transaction_type": "IN",
  "quantity": 5,
  "reference": "PO-2024-001",
  "transaction_date": "2024-01-15",
  "performed_by": 1,
  "remarks": "New stock received"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Item not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
