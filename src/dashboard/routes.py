"""
Dashboard routes.
"""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..tracker import TrackerDatabase

router = APIRouter()

# Setup templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Database path
DB_PATH = Path("output/demo_tracker.db")


def get_database():
    """Get database instance."""
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database not found. Run demo first: python main.py --demo")
    return TrackerDatabase(DB_PATH)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard."""
    try:
        db = get_database()
        stats = db.get_stats()
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "stats": stats,
        })
    except HTTPException:
        # Database doesn't exist yet
        return templates.TemplateResponse("index.html", {
            "request": request,
            "stats": {
                "total": 0,
                "discovered": 0,
                "approved": 0,
                "applied": 0,
                "rejected": 0,
                "interview": 0,
                "filtered_out": 0,
            },
            "no_data": True,
        })


@router.get("/jobs", response_class=HTMLResponse)
async def jobs_list(request: Request, status: Optional[str] = None):
    """Jobs list page."""
    try:
        db = get_database()
        
        if status:
            jobs = db.get_jobs_by_status(status)
            page_title = f"{status.replace('_', ' ').title()} Jobs"
        else:
            jobs = db.get_all_jobs()
            page_title = "All Jobs"
        
        return templates.TemplateResponse("jobs.html", {
            "request": request,
            "jobs": jobs,
            "page_title": page_title,
            "status_filter": status,
        })
    except HTTPException:
        return templates.TemplateResponse("jobs.html", {
            "request": request,
            "jobs": [],
            "page_title": "All Jobs",
            "no_data": True,
        })


@router.get("/emails", response_class=HTMLResponse)
async def emails_page(request: Request):
    """Email classifications page."""
    import csv
    
    emails = []
    csv_path = Path("output/email_classifications.csv")
    
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            emails = list(reader)
    
    return templates.TemplateResponse("emails.html", {
        "request": request,
        "emails": emails,
        "no_data": len(emails) == 0,
    })


@router.get("/api/stats")
async def api_stats():
    """API endpoint for statistics."""
    try:
        db = get_database()
        return db.get_stats()
    except HTTPException:
        return {
            "total": 0,
            "discovered": 0,
            "approved": 0,
            "applied": 0,
            "rejected": 0,
            "interview": 0,
            "filtered_out": 0,
        }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database_exists": DB_PATH.exists(),
    }
