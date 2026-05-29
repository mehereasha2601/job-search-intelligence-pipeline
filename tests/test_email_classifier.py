"""
Tests for email classifier.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.email_intelligence import EmailClassifier, is_rejection_email, is_interview_email


def test_classifies_application_confirmation():
    """Test classification of application confirmation emails."""
    classifier = EmailClassifier()
    
    subject = "Application Received - Software Engineer"
    body = "Thank you for your application. We have successfully received your resume."
    
    result = classifier.classify(subject, body)
    
    assert result["category"] == "applied"
    assert result["confidence"] > 0


def test_classifies_rejection():
    """Test classification of rejection emails."""
    classifier = EmailClassifier()
    
    subject = "Application Status Update"
    body = "Unfortunately, we have decided to move forward with other candidates."
    
    result = classifier.classify(subject, body)
    
    assert result["category"] == "rejected"
    assert len(result["matched_keywords"]) > 0


def test_classifies_interview_request():
    """Test classification of interview request emails."""
    classifier = EmailClassifier()
    
    subject = "Interview Request - Backend Engineer"
    body = "We'd like to schedule a phone screen to discuss the role."
    
    result = classifier.classify(subject, body)
    
    assert result["category"] == "interview"


def test_classifies_assessment():
    """Test classification of assessment emails."""
    classifier = EmailClassifier()
    
    subject = "Coding Assessment - Next Steps"
    body = "Please complete the following HackerRank coding challenge."
    
    result = classifier.classify(subject, body)
    
    assert result["category"] == "assessment"


def test_classifies_follow_up():
    """Test classification of recruiter follow-up emails."""
    classifier = EmailClassifier()
    
    subject = "Opportunity at TechCorp"
    body = "I wanted to follow up and see if you're interested in this role."
    
    result = classifier.classify(subject, body)
    
    assert result["category"] == "follow_up"


def test_unknown_classification():
    """Test unknown classification for unrecognized emails."""
    classifier = EmailClassifier()
    
    subject = "Company Newsletter"
    body = "Check out our latest blog post about engineering culture."
    
    result = classifier.classify(subject, body)
    
    assert result["category"] == "unknown"


def test_is_rejection_helper():
    """Test is_rejection_email helper function."""
    assert is_rejection_email("", "Unfortunately, we are not moving forward")
    assert is_rejection_email("", "decided to pursue other candidates")
    assert not is_rejection_email("", "We'd like to interview you")


def test_is_interview_helper():
    """Test is_interview_email helper function."""
    assert is_interview_email("Interview Request", "Would you like to schedule")
    assert is_interview_email("Next Steps", "phone screen")
    assert not is_interview_email("", "Thank you for applying")
