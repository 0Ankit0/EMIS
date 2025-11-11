# EMIS Monitoring Setup

## Overview

Comprehensive monitoring setup for the EMIS application using Prometheus, Grafana, and Alertmanager.

## Components

### 1. Prometheus
- **Port**: 9090
- **Purpose**: Metrics collection and storage
- **Scrapes**:
  - EMIS API (every 10s)
  - PostgreSQL (every 15s)
  - Redis (every 15s)
  - System metrics (every 15s)
  - Celery workers (every 15s)

### 2. Grafana
- **Port**: 3000
- **Default credentials**: admin/admin
- **Purpose**: Metrics visualization and dashboards
- **Pre-configured**:
  - Prometheus datasource
  - Dashboard provisioning

### 3. Alertmanager
- **Port**: 9093
- **Purpose**: Alert routing and notification
- **Channels**:
  - Email
  - Slack
  - Webhook

### 4. Exporters
- **PostgreSQL Exporter** (9187): Database metrics
- **Redis Exporter** (9121): Redis metrics
- **Node Exporter** (9100): System metrics

## Setup

### 1. Start Monitoring Stack

```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

### 2. Access UIs

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
- **Alertmanager**: http://localhost:9093

### 3. Configure Alertmanager

Edit `alertmanager.yml` to configure your notification channels:

```yaml
receivers:
  - name: 'critical-alerts'
    email_configs:
      - to: 'your-email@example.com'
        from: 'alertmanager@emis.local'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'your-email@gmail.com'
        auth_password: 'your-app-password'
```

### 4. Enable Metrics in FastAPI

Update `src/app.py`:

```python
from src.lib.metrics import metrics_router

app.include_router(metrics_router)
```

## Available Metrics

### HTTP Metrics
- `http_requests_total` - Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds` - Request duration histogram

### Database Metrics
- `db_query_duration_seconds` - Query duration by type
- `db_connections_active` - Active database connections
- `pg_stat_database_numbackends` - PostgreSQL connections
- `pg_stat_statements_mean_time_seconds` - Average query time

### Redis Metrics
- `redis_memory_used_bytes` - Redis memory usage
- `redis_connected_clients` - Connected clients
- `redis_commands_processed_total` - Total commands processed

### Application Metrics
- `student_enrollment_total` - Student enrollments
- `student_enrollment_failures_total` - Enrollment failures
- `payroll_processing_total` - Payroll processing attempts
- `notification_delivery_total` - Notification deliveries
- `book_transactions_total` - Library transactions

### System Metrics
- `node_cpu_seconds_total` - CPU usage
- `node_memory_MemAvailable_bytes` - Available memory
- `node_filesystem_avail_bytes` - Available disk space

## Alerts

### Critical Alerts
- API Down
- PostgreSQL Down
- Redis Down
- Disk Space Low
- Payroll Processing Failed

### Warning Alerts
- High Error Rate
- Slow Response Time
- High Database Connections
- High CPU/Memory Usage
- High Notification Failures

## Custom Dashboards

### API Dashboard
Monitor API health and performance:
- Request rate
- Error rate
- Response time (p50, p95, p99)
- Active connections

### Database Dashboard
Monitor database performance:
- Query duration
- Connection pool usage
- Slow queries
- Database size

### System Dashboard
Monitor system resources:
- CPU usage
- Memory usage
- Disk I/O
- Network I/O

### Business Metrics Dashboard
Monitor application KPIs:
- Student enrollments per day
- Payroll processing status
- Library transactions
- Notification delivery rates

## Grafana Dashboard Import

Pre-built dashboards available:
1. FastAPI Application Dashboard (ID: 14693)
2. PostgreSQL Database Dashboard (ID: 9628)
3. Redis Dashboard (ID: 11835)
4. Node Exporter Full Dashboard (ID: 1860)

Import via: Grafana UI → Dashboards → Import → Enter Dashboard ID

## Alert Testing

Test alerts manually:

```bash
# Trigger test alert
curl -H "Content-Type: application/json" -d '[{
  "labels": {
    "alertname": "TestAlert",
    "severity": "warning"
  },
  "annotations": {
    "summary": "Test alert"
  }
}]' http://localhost:9093/api/v1/alerts
```

## Production Recommendations

1. **Retention**: Configure Prometheus retention (default: 15 days)
2. **High Availability**: Run multiple Prometheus instances
3. **Secure Access**: Enable authentication for Grafana
4. **Backup**: Regular backup of Grafana dashboards
5. **Alert Channels**: Configure multiple notification channels
6. **SLA Monitoring**: Set up SLA dashboards
7. **Capacity Planning**: Monitor resource trends

## Troubleshooting

### Prometheus not scraping targets

Check targets status:
```bash
curl http://localhost:9090/api/v1/targets
```

### Grafana not showing data

1. Verify Prometheus datasource connection
2. Check time range in dashboard
3. Verify metrics are being collected

### Alerts not firing

1. Check alert rules syntax
2. Verify Alertmanager configuration
3. Test alert routing

## Performance Tuning

### Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s  # Adjust based on load
  evaluation_interval: 15s
```

### Retention
```bash
# Set retention to 30 days
--storage.tsdb.retention.time=30d
```

## Integration with Application

Add metrics to your endpoints:

```python
from src.lib.metrics import student_enrollment_total

@router.post("/enrollments")
async def create_enrollment(...):
    # Your logic
    student_enrollment_total.labels(status="success").inc()
    return enrollment
```

## Monitoring Checklist

- [ ] Prometheus collecting metrics
- [ ] Grafana dashboards configured
- [ ] Alertmanager routing working
- [ ] Email notifications configured
- [ ] Slack notifications configured
- [ ] Critical alerts tested
- [ ] Dashboard access secured
- [ ] Metrics retention configured
- [ ] Backup strategy in place
- [ ] Documentation updated
