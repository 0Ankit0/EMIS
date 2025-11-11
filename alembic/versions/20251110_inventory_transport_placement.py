"""Add inventory, transport and placement models

Revision ID: 20251110_inventory_transport_placement
Revises: add_billing_enhancements_20251110_133417
Create Date: 2025-11-10 08:48:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251110_inventory_transport_placement'
down_revision = 'add_billing_enhancements_20251110_133417'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Inventory Category
    op.create_table(
        'inventory_categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('code', sa.String(50), unique=True, index=True),
        sa.Column('description', sa.Text),
        sa.Column('parent_category_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('inventory_categories.id')),
        sa.Column('requires_approval', sa.Boolean, default=False),
        sa.Column('is_consumable', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Inventory Item
    op.create_table(
        'inventory_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('code', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('description', sa.Text),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('inventory_categories.id'), nullable=False),
        sa.Column('quantity', sa.Integer, default=0),
        sa.Column('min_quantity', sa.Integer, default=0),
        sa.Column('max_quantity', sa.Integer),
        sa.Column('unit', sa.String(50), nullable=False),
        sa.Column('location', sa.String(255)),
        sa.Column('unit_cost', sa.Numeric(10, 2)),
        sa.Column('total_value', sa.Numeric(15, 2)),
        sa.Column('status', sa.String(50), default='available', index=True),
        sa.Column('is_asset', sa.Boolean, default=False),
        sa.Column('asset_tag', sa.String(100), unique=True, index=True),
        sa.Column('serial_number', sa.String(100)),
        sa.Column('model', sa.String(255)),
        sa.Column('manufacturer', sa.String(255)),
        sa.Column('purchase_date', sa.Date),
        sa.Column('warranty_expiry', sa.Date),
        sa.Column('last_inspection_date', sa.Date),
        sa.Column('next_inspection_date', sa.Date),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Vendor
    op.create_table(
        'vendors',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('code', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('contact_person', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('phone', sa.String(20)),
        sa.Column('address', sa.Text),
        sa.Column('gstin', sa.String(50)),
        sa.Column('pan', sa.String(20)),
        sa.Column('bank_name', sa.String(255)),
        sa.Column('account_number', sa.String(50)),
        sa.Column('ifsc_code', sa.String(20)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('rating', sa.Integer),
        sa.Column('notes', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Purchase Order
    op.create_table(
        'purchase_orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('po_number', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('vendor_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('vendors.id'), nullable=False),
        sa.Column('order_date', sa.Date, nullable=False, index=True),
        sa.Column('expected_delivery_date', sa.Date),
        sa.Column('actual_delivery_date', sa.Date),
        sa.Column('total_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('tax_amount', sa.Numeric(15, 2), default=0),
        sa.Column('discount_amount', sa.Numeric(15, 2), default=0),
        sa.Column('final_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('status', sa.String(50), default='draft', index=True),
        sa.Column('requested_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True)),
        sa.Column('approved_at', sa.DateTime(timezone=True)),
        sa.Column('delivery_address', sa.Text),
        sa.Column('shipping_method', sa.String(100)),
        sa.Column('tracking_number', sa.String(100)),
        sa.Column('notes', sa.Text),
        sa.Column('terms_and_conditions', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Purchase Order Items
    op.create_table(
        'purchase_order_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('purchase_order_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('purchase_orders.id'), nullable=False),
        sa.Column('inventory_item_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('inventory_items.id'), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('total_price', sa.Numeric(15, 2), nullable=False),
        sa.Column('received_quantity', sa.Integer, default=0),
        sa.Column('description', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Stock Transaction
    op.create_table(
        'stock_transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('inventory_items.id'), nullable=False, index=True),
        sa.Column('transaction_type', sa.String(50), nullable=False, index=True),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('unit_cost', sa.Numeric(10, 2)),
        sa.Column('total_cost', sa.Numeric(15, 2)),
        sa.Column('balance_quantity', sa.Integer, nullable=False),
        sa.Column('reference_type', sa.String(50)),
        sa.Column('reference_id', postgresql.UUID(as_uuid=True)),
        sa.Column('from_location', sa.String(255)),
        sa.Column('to_location', sa.String(255)),
        sa.Column('issued_to', postgresql.UUID(as_uuid=True)),
        sa.Column('reason', sa.Text),
        sa.Column('notes', sa.Text),
        sa.Column('transaction_date', sa.Date, nullable=False, index=True),
        sa.Column('performed_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, index=True)
    )
    
    # Transport - Vehicle
    op.create_table(
        'vehicles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('vehicle_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('vehicle_type', sa.String(50), nullable=False),
        sa.Column('model', sa.String(255), nullable=False),
        sa.Column('manufacturer', sa.String(255), nullable=False),
        sa.Column('year', sa.Integer),
        sa.Column('seating_capacity', sa.Integer, nullable=False),
        sa.Column('status', sa.String(50), default='active', index=True),
        sa.Column('driver_name', sa.String(255)),
        sa.Column('driver_phone', sa.String(20)),
        sa.Column('driver_license', sa.String(50)),
        sa.Column('registration_number', sa.String(50), nullable=False),
        sa.Column('registration_expiry', sa.Date),
        sa.Column('insurance_number', sa.String(100)),
        sa.Column('insurance_expiry', sa.Date),
        sa.Column('last_service_date', sa.Date),
        sa.Column('next_service_date', sa.Date),
        sa.Column('last_service_km', sa.Integer),
        sa.Column('current_km', sa.Integer),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Route
    op.create_table(
        'routes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('route_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('route_name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('total_distance_km', sa.Numeric(10, 2)),
        sa.Column('estimated_duration_minutes', sa.Integer),
        sa.Column('monthly_fee', sa.Numeric(10, 2)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Route Stop
    op.create_table(
        'route_stops',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('route_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('routes.id'), nullable=False),
        sa.Column('stop_name', sa.String(255), nullable=False),
        sa.Column('stop_address', sa.Text),
        sa.Column('stop_order', sa.Integer, nullable=False),
        sa.Column('latitude', sa.Numeric(10, 8)),
        sa.Column('longitude', sa.Numeric(11, 8)),
        sa.Column('arrival_time', sa.Time),
        sa.Column('departure_time', sa.Time),
        sa.Column('distance_from_previous_km', sa.Numeric(10, 2)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Route Vehicle
    op.create_table(
        'route_vehicles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('route_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('routes.id'), nullable=False),
        sa.Column('vehicle_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('vehicles.id'), nullable=False),
        sa.Column('assigned_from', sa.Date, nullable=False),
        sa.Column('assigned_to', sa.Date),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Student Transport
    op.create_table(
        'student_transport',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('students.id'), nullable=False, index=True),
        sa.Column('route_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('routes.id'), nullable=False),
        sa.Column('stop_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('route_stops.id'), nullable=False),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('monthly_fee', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Vehicle Maintenance
    op.create_table(
        'vehicle_maintenance',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('vehicle_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('vehicles.id'), nullable=False),
        sa.Column('maintenance_type', sa.String(50), nullable=False),
        sa.Column('maintenance_date', sa.Date, nullable=False, index=True),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('cost', sa.Numeric(10, 2), nullable=False),
        sa.Column('odometer_reading', sa.Integer),
        sa.Column('service_provider', sa.String(255)),
        sa.Column('invoice_number', sa.String(100)),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date),
        sa.Column('is_completed', sa.Boolean, default=False),
        sa.Column('performed_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Placement - Company
    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('industry', sa.String(100)),
        sa.Column('website', sa.String(255)),
        sa.Column('contact_person', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('phone', sa.String(20)),
        sa.Column('address', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('logo_url', sa.String(500)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Job Posting
    op.create_table(
        'job_postings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False, index=True),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('job_type', sa.String(50), nullable=False),
        sa.Column('required_cgpa', sa.Numeric(3, 2)),
        sa.Column('eligible_programs', sa.Text),
        sa.Column('eligible_departments', sa.Text),
        sa.Column('salary_min', sa.Numeric(12, 2)),
        sa.Column('salary_max', sa.Numeric(12, 2)),
        sa.Column('currency', sa.String(10), default='INR'),
        sa.Column('location', sa.String(255)),
        sa.Column('is_remote', sa.Boolean, default=False),
        sa.Column('total_positions', sa.Integer, default=1),
        sa.Column('filled_positions', sa.Integer, default=0),
        sa.Column('posted_date', sa.Date, nullable=False),
        sa.Column('application_deadline', sa.Date, nullable=False),
        sa.Column('interview_date', sa.Date),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_published', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Placement Application
    op.create_table(
        'placement_applications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('students.id'), nullable=False, index=True),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('job_postings.id'), nullable=False, index=True),
        sa.Column('cover_letter', sa.Text),
        sa.Column('resume_url', sa.String(500)),
        sa.Column('status', sa.String(50), default='submitted', index=True),
        sa.Column('applied_at', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Interview
    op.create_table(
        'interviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('application_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('placement_applications.id'), nullable=False),
        sa.Column('interview_type', sa.String(50), nullable=False),
        sa.Column('interview_date', sa.Date, nullable=False, index=True),
        sa.Column('interview_time', sa.String(20)),
        sa.Column('location', sa.String(255)),
        sa.Column('is_online', sa.Boolean, default=False),
        sa.Column('meeting_link', sa.String(500)),
        sa.Column('feedback', sa.Text),
        sa.Column('rating', sa.Integer),
        sa.Column('is_completed', sa.Boolean, default=False),
        sa.Column('is_cleared', sa.Boolean),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Placement Offer
    op.create_table(
        'placement_offers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('application_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('placement_applications.id'), nullable=False, unique=True),
        sa.Column('job_title', sa.String(255), nullable=False),
        sa.Column('salary', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.String(10), default='INR'),
        sa.Column('joining_date', sa.Date),
        sa.Column('location', sa.String(255)),
        sa.Column('offer_letter_url', sa.String(500)),
        sa.Column('is_accepted', sa.Boolean),
        sa.Column('accepted_at', sa.DateTime(timezone=True)),
        sa.Column('offered_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('placement_offers')
    op.drop_table('interviews')
    op.drop_table('placement_applications')
    op.drop_table('job_postings')
    op.drop_table('companies')
    op.drop_table('vehicle_maintenance')
    op.drop_table('student_transport')
    op.drop_table('route_vehicles')
    op.drop_table('route_stops')
    op.drop_table('routes')
    op.drop_table('vehicles')
    op.drop_table('stock_transactions')
    op.drop_table('purchase_order_items')
    op.drop_table('purchase_orders')
    op.drop_table('vendors')
    op.drop_table('inventory_items')
    op.drop_table('inventory_categories')
