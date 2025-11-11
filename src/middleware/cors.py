"""CORS middleware configuration for EMIS."""
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings


def setup_cors(app):
    """Configure CORS middleware."""
    origins = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Add additional origins from settings if available
    if hasattr(settings, "CORS_ORIGINS"):
        origins.extend(settings.CORS_ORIGINS.split(","))
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-RateLimit-Limit-Minute", "X-RateLimit-Remaining-Minute"],
    )
