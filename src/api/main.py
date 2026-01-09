"""FastAPI Application Entry Point.

This module creates and configures the FastAPI application.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import users
from src.domain.exceptions import DomainException
from src.infrastructure.config import settings
from src.infrastructure.logging.logger import configure_logging, get_logger

# Configure logging
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.
    
    Handles startup and shutdown events.
    
    Args:
        app: FastAPI application instance.
        
    Yields:
        None
    """
    # Startup
    logger.info("application_starting", app_name=settings.app.name, version=settings.app.version)
    yield
    # Shutdown
    logger.info("application_shutting_down")


# Create FastAPI application
app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description="TinyBigCorp Enterprise Backend - Clean Architecture with FastAPI",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for domain exceptions
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """Handle domain exceptions globally.
    
    Args:
        request: The incoming request.
        exc: The domain exception.
        
    Returns:
        JSON response with error details.
    """
    logger.error(
        "domain_exception",
        exception_type=type(exc).__name__,
        message=exc.message,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": type(exc).__name__, "message": exc.message},
    )


# Global exception handler for unexpected errors
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions globally.
    
    Args:
        request: The incoming request.
        exc: The exception.
        
    Returns:
        JSON response with error details.
    """
    logger.exception(
        "unexpected_exception",
        exception_type=type(exc).__name__,
        message=str(exc),
        path=request.url.path,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "environment": settings.app.environment
    }


def main():
    """Main entry point for running the application via console script."""
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.app.debug,
    )
