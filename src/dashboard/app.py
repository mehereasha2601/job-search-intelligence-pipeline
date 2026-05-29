"""
FastAPI dashboard application.
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes import router

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def initialize_demo_data():
    """Initialize demo data on startup if database is empty."""
    from src.filters import PreferenceFilter, SponsorshipDetector, RelevanceScorer
    from src.email_intelligence import (
        EmailClassifier,
        EmailExtractor,
        load_sample_emails,
        load_sample_jobs,
    )
    from src.tracker import TrackerDatabase, StatusUpdater, export_demo_results
    
    # Check if we should initialize demo data
    db_path = Path("output/demo_tracker.db")
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if database exists and has data
    if db_path.exists():
        db = TrackerDatabase(db_path)
        stats = db.get_stats()
        if stats.get("total", 0) > 0:
            print(f"✓ Database already initialized with {stats['total']} jobs")
            return
    
    print("🔄 Initializing demo data...")
    
    # Setup paths
    sample_dir = Path("sample_data")
    
    # Initialize components
    preference_filter = PreferenceFilter()
    sponsorship_detector = SponsorshipDetector()
    relevance_scorer = RelevanceScorer(
        target_skills=["python", "machine learning", "backend", "distributed systems"],
        preferred_companies=["google", "stripe", "meta"],
    )
    email_classifier = EmailClassifier()
    email_extractor = EmailExtractor()
    
    # Load sample data
    jobs = load_sample_jobs(sample_dir)
    emails = load_sample_emails(sample_dir)
    
    # Filter jobs by preferences
    accepted_jobs, rejected_jobs = preference_filter.filter_jobs(jobs)
    
    # Detect sponsorship signals
    for job in accepted_jobs:
        result = sponsorship_detector.analyze(job.get("description", ""), job.get("title", ""))
        job["sponsorship_status"] = result["status"]
        job["sponsorship_signals"] = result["signals"]
    
    # Calculate relevance scores
    accepted_jobs = relevance_scorer.score_jobs(accepted_jobs)
    
    # Classify emails
    classified_emails = email_classifier.classify_batch(emails)
    extracted_emails = email_extractor.extract_from_batch(classified_emails)
    
    # Export results
    export_demo_results(
        filtered_jobs=accepted_jobs,
        rejected_jobs=rejected_jobs,
        email_classifications=extracted_emails,
        output_dir=output_dir
    )
    
    # Create demo database
    db = TrackerDatabase(db_path)
    
    # Add accepted jobs to database
    for job in accepted_jobs:
        job["status"] = "approved"
        db.add_job(job)
    
    # Add rejected jobs as filtered_out
    for job in rejected_jobs:
        job["status"] = "filtered_out"
        db.add_job(job)
    
    # Update statuses from emails
    status_updater = StatusUpdater(db)
    status_updater.update_from_emails_batch(extracted_emails)
    
    stats = db.get_stats()
    print(f"✓ Demo data initialized: {stats['total']} jobs, {stats['approved']} approved, {stats['interview']} interviews")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Job Search Intelligence Pipeline",
        description="Demo dashboard for job application tracking",
        version="1.0.0"
    )
    
    # Startup event to initialize demo data
    @app.on_event("startup")
    async def startup_event():
        """Run on application startup."""
        try:
            initialize_demo_data()
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize demo data: {e}")
    
    # Include routes
    app.include_router(router)
    
    return app


# For direct uvicorn usage
app = create_app()
