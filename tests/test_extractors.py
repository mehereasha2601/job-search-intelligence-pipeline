"""
Tests for email extractors.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.email_intelligence import (
    extract_company_from_sender,
    extract_role_from_subject,
    normalize_company_name,
)


def test_extract_company_from_sender():
    """Test company name extraction from email sender."""
    assert extract_company_from_sender("recruiter@google.com") == "Google"
    assert extract_company_from_sender("Jane Doe <jane@stripe.com>") == "Stripe"
    assert extract_company_from_sender("noreply@meta.com") == "Meta"
    
    # Should not extract ATS names
    result = extract_company_from_sender("noreply@greenhouse.io")
    assert result is None


def test_extract_role_from_subject():
    """Test role extraction from email subject."""
    assert extract_role_from_subject("Software Engineer - Application Received") == "Software Engineer"
    assert extract_role_from_subject("Your Backend Developer application") == "Backend Developer"
    # Note: "ML Engineer Interview" doesn't match patterns (no "for", "your", or "-")
    assert extract_role_from_subject("ML Engineer - Interview") == "ML Engineer"


def test_normalize_company_name():
    """Test company name normalization."""
    assert normalize_company_name("Google Inc.") == "Google"
    assert normalize_company_name("Stripe LLC") == "Stripe"
    assert normalize_company_name("Meta Corporation") == "Meta"
    assert normalize_company_name("Microsoft Corp") == "Microsoft"


def test_extract_company_handles_edge_cases():
    """Test company extraction with edge cases."""
    # Empty string
    assert extract_company_from_sender("") is None
    
    # Invalid format
    assert extract_company_from_sender("not-an-email") is None
    
    # Common no-reply addresses
    company = extract_company_from_sender("no-reply@techcorp.com")
    assert company == "Techcorp"
