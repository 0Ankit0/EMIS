"""
Prometheus metrics endpoints
"""

import time

from django.contrib.auth import get_user_model
from django.db import connection
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

User = get_user_model()


@api_view(["GET"])
@permission_classes([AllowAny])
def metrics(request):
    """
    Prometheus-compatible metrics endpoint
    Returns metrics in Prometheus text format
    """
    metrics_lines = []

    # Add HELP and TYPE comments
    metrics_lines.append("# HELP emis_users_total Total number of users")
    metrics_lines.append("# TYPE emis_users_total gauge")

    metrics_lines.append("# HELP emis_users_active Number of active users")
    metrics_lines.append("# TYPE emis_users_active gauge")

    metrics_lines.append(
        "# HELP emis_database_connections Number of database connections"
    )
    metrics_lines.append("# TYPE emis_database_connections gauge")

    # Collect metrics
    try:
        # User metrics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()

        metrics_lines.append(f"emis_users_total {total_users}")
        metrics_lines.append(f"emis_users_active {active_users}")

        # Database connection metrics
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT count(*)
                FROM pg_stat_activity
                WHERE datname = current_database()
            """
            )
            db_connections = cursor.fetchone()[0]
            metrics_lines.append(f"emis_database_connections {db_connections}")
    except Exception as e:
        metrics_lines.append(f"# Error collecting metrics: {str(e)}")

    # Application-specific metrics
    try:
        from apps.admissions.models import Application

        total_applications = Application.objects.count()
        metrics_lines.append(
            "# HELP emis_applications_total Total number of applications"
        )
        metrics_lines.append("# TYPE emis_applications_total gauge")
        metrics_lines.append(f"emis_applications_total {total_applications}")

        # Applications by status
        for status in ["submitted", "under_review", "accepted", "rejected"]:
            count = Application.objects.filter(status=status).count()
            metrics_lines.append(
                f'emis_applications_status{{status="{status}"}} {count}'
            )
    except Exception:
        pass

    try:
        from apps.courses.models import Course

        total_courses = Course.objects.count()
        metrics_lines.append("# HELP emis_courses_total Total number of courses")
        metrics_lines.append("# TYPE emis_courses_total gauge")
        metrics_lines.append(f"emis_courses_total {total_courses}")
    except Exception:
        pass

    try:
        from apps.finance.models import Invoice, Payment

        total_invoices = Invoice.objects.count()
        total_payments = Payment.objects.count()

        metrics_lines.append("# HELP emis_invoices_total Total number of invoices")
        metrics_lines.append("# TYPE emis_invoices_total gauge")
        metrics_lines.append(f"emis_invoices_total {total_invoices}")

        metrics_lines.append("# HELP emis_payments_total Total number of payments")
        metrics_lines.append("# TYPE emis_payments_total gauge")
        metrics_lines.append(f"emis_payments_total {total_payments}")
    except Exception:
        pass

    # System metrics
    metrics_lines.append("# HELP emis_uptime_seconds Application uptime in seconds")
    metrics_lines.append("# TYPE emis_uptime_seconds counter")
    metrics_lines.append(f"emis_uptime_seconds {int(time.time())}")

    # Join all metrics with newlines
    metrics_text = "\n".join(metrics_lines) + "\n"

    return HttpResponse(metrics_text, content_type="text/plain; version=0.0.4")
