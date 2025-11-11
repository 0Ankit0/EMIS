from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, DatabaseError
from pydantic import BaseModel

from src.lib.logging import get_logger


logger = get_logger(__name__)


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure exception handlers for the application."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle request validation errors."""
        errors = {}
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"][1:])
            errors[field] = error["msg"]

        logger.warning(
            f"Validation error on {request.method} {request.url.path}: {errors}"
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "detail": "Request validation failed",
                "fields": errors,
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        """Handle database integrity errors."""
        logger.error(f"Database integrity error: {exc}", exc_info=True)

        detail = "A database constraint was violated"
        if "unique" in str(exc).lower():
            detail = "A record with this value already exists"
        elif "foreign key" in str(exc).lower():
            detail = "Referenced record does not exist"

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Integrity Error",
                "detail": detail,
                "code": "INTEGRITY_ERROR",
            },
        )

    @app.exception_handler(DatabaseError)
    async def database_exception_handler(
        request: Request, exc: DatabaseError
    ) -> JSONResponse:
        """Handle general database errors."""
        logger.error(f"Database error: {exc}", exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Database Error",
                "detail": "An error occurred while accessing the database",
                "code": "DATABASE_ERROR",
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all unhandled exceptions."""
        logger.error(
            f"Unhandled exception on {request.method} {request.url.path}: {exc}",
            exc_info=True,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "detail": "An unexpected error occurred",
                "code": "INTERNAL_ERROR",
            },
        )
