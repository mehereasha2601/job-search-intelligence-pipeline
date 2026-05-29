"""
Preference-based job filtering module.

Filters jobs based on:
- Role level (new grad, entry-level, junior, associate)
- Employment type (full-time only)
- Location (US-based)
- Company blacklist
- Custom preferences
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# Configuration
TARGET_LEVELS = [
    "new grad",
    "new graduate",
    "entry level",
    "entry-level",
    "junior",
    "associate",
    "l3",
    "l4",
    "swe i",
    "swe1",
    "swe 1",
    "early career",
    "0-2 years",
]

SKIP_KEYWORDS = [
    "internship",
    "intern",
    "co-op",
    "coop",
    "contract",
    "part-time",
    "part time",
    "senior",
    "staff",
    "principal",
    "lead",
    "manager",
    "director",
    "vp",
    "vice president",
    "head of",
    "3+ years",
    "5+ years",
]

TARGET_ROLES = [
    "software engineer",
    "software developer",
    "ml engineer",
    "machine learning",
    "ai engineer",
    "backend engineer",
    "data engineer",
    "research engineer",
    "full stack",
    "fullstack",
]


class PreferenceFilter:
    """Filter jobs based on user preferences."""
    
    def __init__(
        self,
        target_levels: Optional[List[str]] = None,
        skip_keywords: Optional[List[str]] = None,
        target_roles: Optional[List[str]] = None,
        company_blacklist: Optional[List[str]] = None,
        location_us_only: bool = True,
    ):
        """
        Initialize preference filter.
        
        Args:
            target_levels: List of acceptable role levels
            skip_keywords: List of keywords that disqualify jobs
            target_roles: List of target role types
            company_blacklist: List of companies to exclude
            location_us_only: Only accept US-based jobs
        """
        self.target_levels = target_levels or TARGET_LEVELS
        self.skip_keywords = skip_keywords or SKIP_KEYWORDS
        self.target_roles = target_roles or TARGET_ROLES
        self.company_blacklist = company_blacklist or []
        self.location_us_only = location_us_only
        
    def passes_filters(self, job: Dict) -> tuple[bool, Optional[str]]:
        """
        Check if job passes all preference filters.
        
        Args:
            job: Job dictionary with keys: title, description, company, location
            
        Returns:
            Tuple of (passes: bool, reason: str if rejected)
        """
        title_lower = job.get("title", "").lower()
        description_lower = job.get("description", "").lower()
        company_lower = job.get("company", "").lower()
        location_lower = job.get("location", "").lower()
        
        # Filter 1: Full-time only
        for keyword in self.skip_keywords:
            if keyword in title_lower:
                return False, f"Excluded keyword in title: {keyword}"
        
        # Filter 2: Role level (must match at least one target level)
        if not any(level in title_lower or level in description_lower 
                   for level in self.target_levels):
            return False, "Not new grad/entry-level role"
        
        # Filter 3: US location (if enabled)
        if self.location_us_only:
            us_indicators = ["united states", "usa", "u.s.", "remote"]
            if not any(indicator in location_lower for indicator in us_indicators):
                # Check for US states
                us_states = ["ca", "ny", "ma", "tx", "wa", "il", "ga", "fl", "pa", "nc", "va", "co"]
                if not any(state in location_lower for state in us_states):
                    return False, "Non-US location"
        
        # Filter 4: Company blacklist
        for blacklisted in self.company_blacklist:
            if blacklisted.lower() in company_lower:
                return False, f"Blacklisted company: {blacklisted}"
        
        # Filter 5: Role relevance (should match target roles)
        if self.target_roles:
            if not any(role in title_lower for role in self.target_roles):
                return False, "Role type not in target list"
        
        return True, None
    
    def filter_jobs(self, jobs: List[Dict]) -> tuple[List[Dict], List[Dict]]:
        """
        Filter a list of jobs.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            Tuple of (accepted_jobs, rejected_jobs)
        """
        accepted = []
        rejected = []
        
        for job in jobs:
            passes, reason = self.passes_filters(job)
            if passes:
                accepted.append(job)
                logger.debug(f"✓ Accepted: {job.get('title')} at {job.get('company')}")
            else:
                job_with_reason = job.copy()
                job_with_reason["rejection_reason"] = reason
                rejected.append(job_with_reason)
                logger.debug(f"✗ Rejected: {job.get('title')} at {job.get('company')} - {reason}")
        
        logger.info(f"Filtering complete: {len(accepted)} accepted, {len(rejected)} rejected")
        return accepted, rejected


def is_full_time(title: str, description: str = "") -> bool:
    """Check if job is full-time."""
    text = (title + " " + description).lower()
    part_time_indicators = ["part-time", "part time", "contract", "freelance", "temporary"]
    return not any(indicator in text for indicator in part_time_indicators)


def is_entry_level(title: str, description: str = "") -> bool:
    """Check if job is entry-level or new grad."""
    text = (title + " " + description).lower()
    return any(level in text for level in TARGET_LEVELS)
