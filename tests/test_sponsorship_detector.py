"""
Tests for sponsorship detector.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.filters import SponsorshipDetector, detect_sponsorship_status


def test_detects_citizenship_requirement():
    """Test detection of citizenship requirements."""
    detector = SponsorshipDetector()
    
    description = "This position requires US citizenship and active security clearance."
    result = detector.analyze(description)
    
    assert result["status"] == "disqualified"
    assert result["confidence"] > 0.9


def test_detects_no_sponsorship():
    """Test detection of no sponsorship statements."""
    detector = SponsorshipDetector()
    
    # Use exact phrase from disqualifying list
    description = "We cannot provide sponsorship for this position."
    result = detector.analyze(description)
    
    assert result["status"] == "disqualified"
    assert len(result["signals"]) > 0


def test_detects_opt_friendly():
    """Test detection of OPT-friendly signals."""
    detector = SponsorshipDetector()
    
    description = "OPT students welcome. We provide H1B visa sponsorship."
    result = detector.analyze(description)
    
    assert result["status"] == "positive"
    assert result["sponsors_visa"] is True


def test_detects_international_students_welcome():
    """Test detection of international student friendly signals."""
    detector = SponsorshipDetector()
    
    description = "International students welcome to apply. Visa sponsorship available."
    result = detector.analyze(description)
    
    assert result["status"] == "positive"


def test_neutral_when_no_signals():
    """Test neutral status when no clear signals."""
    detector = SponsorshipDetector()
    
    description = "We're looking for a backend engineer with Python experience."
    result = detector.analyze(description)
    
    assert result["status"] == "neutral"
    assert result["sponsors_visa"] is None


def test_security_clearance_disqualifies():
    """Test that security clearance requirements disqualify."""
    detector = SponsorshipDetector()
    
    description = "Active Secret clearance required for this role."
    result = detector.analyze(description)
    
    assert result["status"] == "disqualified"


def test_requires_citizenship_helper():
    """Test requires_citizenship helper method."""
    detector = SponsorshipDetector()
    
    assert detector.requires_citizenship("US citizenship required")
    assert detector.requires_citizenship("Must be a US citizen")
    assert not detector.requires_citizenship("No citizenship requirements")


def test_requires_clearance_helper():
    """Test requires_clearance helper method."""
    detector = SponsorshipDetector()
    
    assert detector.requires_clearance("Active security clearance required")
    assert detector.requires_clearance("Top secret clearance needed")
    assert not detector.requires_clearance("No clearance required")
