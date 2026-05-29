"""Email intelligence package."""

from .classifier import EmailClassifier, is_rejection_email, is_interview_email
from .extractors import (
    EmailExtractor,
    extract_company_from_sender,
    extract_role_from_subject,
    normalize_company_name,
)
from .sample_loader import load_sample_emails, load_sample_jobs

__all__ = [
    "EmailClassifier",
    "is_rejection_email",
    "is_interview_email",
    "EmailExtractor",
    "extract_company_from_sender",
    "extract_role_from_subject",
    "normalize_company_name",
    "load_sample_emails",
    "load_sample_jobs",
]
