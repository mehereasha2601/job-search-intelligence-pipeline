"""
Tests for tracker database.
"""

import pytest
import sys
from pathlib import Path
import tempfile
import os

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.tracker import TrackerDatabase


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_path = Path(f.name)
    
    db = TrackerDatabase(db_path)
    yield db
    
    # Cleanup
    if db_path.exists():
        os.unlink(db_path)


def test_database_initialization(temp_db):
    """Test database initialization."""
    assert temp_db.db_path.exists()


def test_add_job(temp_db):
    """Test adding a job to the database."""
    job = {
        "company": "Google",
        "title": "Software Engineer",
        "location": "Mountain View, CA",
        "url": "https://google.com/jobs/123",
        "source": "demo",
        "status": "discovered",
    }
    
    result = temp_db.add_job(job)
    assert result is not None


def test_duplicate_job_not_added(temp_db):
    """Test that duplicate jobs are not added."""
    job = {
        "company": "Google",
        "title": "Software Engineer",
        "location": "Mountain View, CA",
    }
    
    first = temp_db.add_job(job)
    second = temp_db.add_job(job)
    
    assert first is not None
    assert second is None


def test_update_status(temp_db):
    """Test updating job status."""
    job = {
        "company": "Google",
        "title": "Software Engineer",
        "location": "Mountain View, CA",
    }
    
    temp_db.add_job(job)
    temp_db.update_status("Google", "Software Engineer", "applied")
    
    jobs = temp_db.get_jobs_by_status("applied")
    assert len(jobs) == 1
    assert jobs[0]["status"] == "applied"


def test_get_stats(temp_db):
    """Test getting application statistics."""
    temp_db.add_job({"company": "A", "title": "Job1", "status": "approved"})
    temp_db.add_job({"company": "B", "title": "Job2", "status": "applied"})
    temp_db.add_job({"company": "C", "title": "Job3", "status": "rejected"})
    
    stats = temp_db.get_stats()
    
    assert stats["total"] == 3
    assert stats["approved"] == 1
    assert stats["applied"] == 1
    assert stats["rejected"] == 1


def test_get_jobs_by_status(temp_db):
    """Test getting jobs filtered by status."""
    temp_db.add_job({"company": "A", "title": "Job1", "status": "approved"})
    temp_db.add_job({"company": "B", "title": "Job2", "status": "approved"})
    temp_db.add_job({"company": "C", "title": "Job3", "status": "rejected"})
    
    approved_jobs = temp_db.get_jobs_by_status("approved")
    assert len(approved_jobs) == 2
