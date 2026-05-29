"""
FastAPI dashboard application.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes import router


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Job Search Intelligence Pipeline",
        description="Demo dashboard for job application tracking",
        version="1.0.0"
    )
    
    # Include routes
    app.include_router(router)
    
    return app


# For direct uvicorn usage
app = create_app()
