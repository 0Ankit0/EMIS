"""Prometheus metrics for EMIS application."""
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import APIRouter, Response
from typing import Callable
from functools import wraps
import time

# Create metrics router
metrics_router = APIRouter()

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Database metrics
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)

db_connections_active = Gauge(
    'db_connections_active',
    'Number of active database connections'
)

# Student-specific metrics
student_enrollment_total = Counter(
    'student_enrollment_total',
    'Total student enrollments',
    ['status']
)

student_enrollment_failures_total = Counter(
    'student_enrollment_failures_total',
    'Total student enrollment failures',
    ['reason']
)

student_graduation_total = Counter(
    'student_graduation_total',
    'Total student graduations'
)

# HR-specific metrics
payroll_processing_total = Counter(
    'payroll_processing_total',
    'Total payroll processing attempts',
    ['status']
)

payroll_processing_failures_total = Counter(
    'payroll_processing_failures_total',
    'Total payroll processing failures'
)

leave_requests_total = Counter(
    'leave_requests_total',
    'Total leave requests',
    ['type', 'status']
)

# Library metrics
book_transactions_total = Counter(
    'book_transactions_total',
    'Total book transactions',
    ['transaction_type']
)

books_overdue = Gauge(
    'books_overdue',
    'Number of overdue books'
)

# Financial metrics
payments_total = Counter(
    'payments_total',
    'Total payments processed',
    ['status']
)

payments_amount_total = Counter(
    'payments_amount_total',
    'Total payment amount processed'
)

# Notification metrics
notification_delivery_total = Counter(
    'notification_delivery_total',
    'Total notification deliveries',
    ['channel', 'status']
)

notification_delivery_failures_total = Counter(
    'notification_delivery_failures_total',
    'Total notification delivery failures',
    ['channel']
)

# Cache metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits'
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses'
)

# Celery task metrics
celery_tasks_total = Counter(
    'celery_tasks_total',
    'Total Celery tasks',
    ['task_name', 'status']
)

celery_task_duration_seconds = Histogram(
    'celery_task_duration_seconds',
    'Celery task duration in seconds',
    ['task_name']
)


@metrics_router.get("/metrics")
async def metrics():
    """Expose Prometheus metrics."""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )


def track_request_metrics(func: Callable) -> Callable:
    """Decorator to track HTTP request metrics."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            response = await func(*args, **kwargs)
            status_code = getattr(response, 'status_code', 200)
            
            # Track metrics
            http_requests_total.labels(
                method=kwargs.get('method', 'GET'),
                endpoint=kwargs.get('path', '/'),
                status=status_code
            ).inc()
            
            duration = time.time() - start_time
            http_request_duration_seconds.labels(
                method=kwargs.get('method', 'GET'),
                endpoint=kwargs.get('path', '/')
            ).observe(duration)
            
            return response
            
        except Exception as e:
            http_requests_total.labels(
                method=kwargs.get('method', 'GET'),
                endpoint=kwargs.get('path', '/'),
                status=500
            ).inc()
            raise
    
    return wrapper


def track_db_query(query_type: str):
    """Decorator to track database query metrics."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                db_query_duration_seconds.labels(query_type=query_type).observe(duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                db_query_duration_seconds.labels(query_type=f"{query_type}_failed").observe(duration)
                raise
        
        return wrapper
    return decorator
