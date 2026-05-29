"""
Tests for preference filter.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.filters import PreferenceFilter, is_entry_level, is_full_time


def test_entry_level_filter():
    """Test that entry-level jobs pass filter."""
    filter = PreferenceFilter()
    
    job = {
        "title": "Software Engineer - New Grad",
        "description": "Entry level position for recent graduates",
        "company": "TechCorp",
        "location": "San Francisco, CA",
    }
    
    passes, reason = filter.passes_filters(job)
    assert passes is True


def test_senior_role_rejected():
    """Test that senior roles are rejected."""
    filter = PreferenceFilter()
    
    job = {
        "title": "Senior Software Engineer",
        "description": "5+ years of experience required",
        "company": "TechCorp",
        "location": "San Francisco, CA",
    }
    
    passes, reason = filter.passes_filters(job)
    assert passes is False
    assert "keyword" in reason.lower()


def test_internship_rejected():
    """Test that internships are rejected."""
    filter = PreferenceFilter()
    
    job = {
        "title": "Software Engineering Intern",
        "description": "Summer internship for undergraduate students",
        "company": "TechCorp",
        "location": "San Francisco, CA",
    }
    
    passes, reason = filter.passes_filters(job)
    assert passes is False


def test_part_time_rejected():
    """Test that part-time roles are rejected."""
    filter = PreferenceFilter()
    
    job = {
        "title": "Part-Time Developer",
        "description": "Part-time contract position",
        "company": "TechCorp",
        "location": "San Francisco, CA",
    }
    
    passes, reason = filter.passes_filters(job)
    assert passes is False


def test_company_blacklist():
    """Test company blacklist filter."""
    filter = PreferenceFilter(company_blacklist=["BadCorp"])
    
    job = {
        "title": "Software Engineer - New Grad",
        "description": "Entry level position",
        "company": "BadCorp",
        "location": "San Francisco, CA",
    }
    
    passes, reason = filter.passes_filters(job)
    assert passes is False
    assert "blacklist" in reason.lower()


def test_is_entry_level():
    """Test entry level detection helper."""
    assert is_entry_level("Software Engineer - New Grad", "Entry level role")
    assert is_entry_level("Junior Developer", "")
    assert is_entry_level("Associate Engineer", "")
    assert not is_entry_level("Senior Engineer", "")
    assert not is_entry_level("Staff Engineer", "")


def test_is_full_time():
    """Test full-time detection helper."""
    assert is_full_time("Software Engineer", "Full-time position")
    assert is_full_time("Backend Developer", "")
    assert not is_full_time("Part-Time Developer", "")
    assert not is_full_time("Contract Position", "")
