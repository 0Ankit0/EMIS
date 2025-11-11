from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.lib.logging import get_logger, setup_logging
from src.middleware.errors import setup_exception_handlers
from src.routes.health import router as health_router
from src.routes.students import router as students_router
from src.routes.hr import router as hr_router
from src.routes.payroll import router as payroll_router
from src.routes.leave import router as leave_router
from src.routes.library import router as library_router
from src.routes.lms import router as lms_router
from src.routes.finance import router as finance_router
from src.routes.admissions import router as admissions_router
from src.routes.analytics import router as analytics_router
from src.routes.notifications import router as notifications_router
from src.routes.schedule import router as schedule_router
from src.routes.exams import router as exams_router
from src.routes.library_settings import router as library_settings_router
from src.routes.billing import router as billing_router
from src.routes.accounting import router as accounting_router
from src.routes.reports import router as reports_router
from src.routes.dashboard import router as dashboard_router
from src.routes.teacher_hierarchy import router as teacher_hierarchy_router
from src.routes.calendar import router as calendar_router
from src.routes.inventory import router as inventory_router
from src.routes.events import router as events_router
from src.routes.transport import router as transport_router
from src.routes.placement import router as placement_router
from src.lib.metrics import metrics_router


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Handle application startup and shutdown."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    setup_logging()
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
setup_exception_handlers(app)

# Health check routes
app.include_router(health_router)

# Metrics endpoint
app.include_router(metrics_router)

# API routes
app.include_router(students_router)
app.include_router(hr_router)
app.include_router(payroll_router)
app.include_router(leave_router)
app.include_router(library_router)
app.include_router(lms_router)
app.include_router(finance_router)
app.include_router(admissions_router)
app.include_router(analytics_router)
app.include_router(notifications_router)
app.include_router(schedule_router)
app.include_router(exams_router)
app.include_router(library_settings_router)
app.include_router(billing_router)
app.include_router(accounting_router)
app.include_router(reports_router)
app.include_router(dashboard_router)
app.include_router(teacher_hierarchy_router)
app.include_router(calendar_router)
app.include_router(inventory_router)
app.include_router(events_router)
app.include_router(transport_router)
app.include_router(placement_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }
