"""
Structured logging configuration for EMIS
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from django.conf import settings


class StructuredLogger:
    """Structured logger with correlation ID support"""

    def __init__(self, name: str, correlation_id: Optional[str] = None):
        """
        Initialize structured logger

        Args:
            name: Logger name (typically __name__)
            correlation_id: Optional correlation ID for request tracing
        """
        self.logger = logging.getLogger(name)
        self.correlation_id = correlation_id or str(uuid.uuid4())

    def _format_log(self, level: str, message: str, **kwargs) -> Dict[str, Any]:
        """Format log entry as structured JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "correlation_id": self.correlation_id,
            "logger": self.logger.name,
        }

        # Add extra fields
        if kwargs:
            log_entry["extra"] = kwargs

        return log_entry

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        log_data = self._format_log("DEBUG", message, **kwargs)
        self.logger.debug(str(json.dumps(log_data)))

    def info(self, message: str, **kwargs):
        """Log info message"""
        log_data = self._format_log("INFO", message, **kwargs)
        self.logger.info(str(json.dumps(log_data)))

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        log_data = self._format_log("WARNING", message, **kwargs)
        self.logger.warning(str(json.dumps(log_data)))

    def error(self, message: str, **kwargs):
        """Log error message"""
        log_data = self._format_log("ERROR", message, **kwargs)
        self.logger.error(str(json.dumps(log_data)))

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        log_data = self._format_log("CRITICAL", message, **kwargs)
        self.logger.critical(str(json.dumps(log_data)))

    def exception(self, message: str, exc_info=True, **kwargs):
        """Log exception with traceback"""
        log_data = self._format_log("ERROR", message, **kwargs)
        self.logger.exception(str(json.dumps(log_data)), exc_info=exc_info)

    def set_correlation_id(self, correlation_id: str):
        """Update correlation ID"""
        self.correlation_id = correlation_id


class CorrelationIDFilter(logging.Filter):
    """Logging filter to add correlation ID to log records"""

    def filter(self, record):
        """Add correlation ID to log record"""
        if not hasattr(record, "correlation_id"):
            record.correlation_id = "N/A"
        return True


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record):
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", "N/A"),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra"):
            log_data["extra"] = record.extra

        return json.dumps(log_data)


def get_logger(name: str, correlation_id: Optional[str] = None) -> StructuredLogger:
    """
    Get a structured logger instance

    Args:
        name: Logger name (typically __name__)
        correlation_id: Optional correlation ID

    Returns:
        StructuredLogger instance

    Example:
        >>> from apps.core.logging import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info('User logged in', user_id=123)
    """
    return StructuredLogger(name, correlation_id)


# Configure Django logging
def configure_logging():
    """Configure structured logging for Django"""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "correlation_id": {
                "()": "apps.core.logging.CorrelationIDFilter",
            },
        },
        "formatters": {
            "json": {
                "()": "apps.core.logging.JSONFormatter",
            },
            "verbose": {
                "format": "[{levelname}] {asctime} {name} - {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "filters": ["correlation_id"],
                "formatter": "json" if not settings.DEBUG else "verbose",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": settings.BASE_DIR / "logs" / "emis.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "filters": ["correlation_id"],
                "formatter": "json",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "apps": {
                "handlers": ["console", "file"],
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "propagate": False,
            },
        },
    }
