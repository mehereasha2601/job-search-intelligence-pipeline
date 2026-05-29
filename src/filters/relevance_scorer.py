"""
Relevance scoring for jobs based on keywords and preferences.
"""

import logging
from typing import Dict, List, Set, Optional

logger = logging.getLogger(__name__)


class RelevanceScorer:
    """Score job relevance based on keywords and preferences."""
    
    def __init__(
        self,
        target_skills: Optional[List[str]] = None,
        preferred_companies: Optional[List[str]] = None,
        preferred_locations: Optional[List[str]] = None,
    ):
        """
        Initialize relevance scorer.
        
        Args:
            target_skills: Skills to match against
            preferred_companies: Companies to boost score
            preferred_locations: Preferred locations
        """
        self.target_skills = set(skill.lower() for skill in (target_skills or []))
        self.preferred_companies = set(company.lower() for company in (preferred_companies or []))
        self.preferred_locations = set(loc.lower() for loc in (preferred_locations or []))
    
    def calculate_score(self, job: Dict) -> float:
        """
        Calculate relevance score (0.0 to 1.0).
        
        Args:
            job: Job dictionary with title, description, company, location
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.0
        max_score = 0.0
        
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        company = job.get("company", "").lower()
        location = job.get("location", "").lower()
        
        # Skill matching (weight: 0.6)
        if self.target_skills:
            max_score += 0.6
            skills_found = sum(1 for skill in self.target_skills if skill in title or skill in description)
            skill_score = min(skills_found / 5.0, 1.0) * 0.6  # Cap at 5 skills
            score += skill_score
        
        # Preferred company (weight: 0.2)
        if self.preferred_companies:
            max_score += 0.2
            if any(pref_company in company for pref_company in self.preferred_companies):
                score += 0.2
        
        # Preferred location (weight: 0.2)
        if self.preferred_locations:
            max_score += 0.2
            if any(pref_loc in location for pref_loc in self.preferred_locations):
                score += 0.2
        
        # Normalize score
        if max_score > 0:
            return score / max_score
        return 0.5  # Default score if no preferences set
    
    def score_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Score a list of jobs and add relevance_score field.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            Jobs with relevance_score field added
        """
        for job in jobs:
            job["relevance_score"] = self.calculate_score(job)
        
        # Sort by score (highest first)
        jobs_sorted = sorted(jobs, key=lambda j: j.get("relevance_score", 0), reverse=True)
        
        logger.info(f"Scored {len(jobs)} jobs. Top score: {jobs_sorted[0].get('relevance_score', 0):.2f}")
        return jobs_sorted


def calculate_keyword_match_score(text: str, keywords: Set[str]) -> float:
    """
    Calculate keyword match score for a text.
    
    Args:
        text: Text to analyze
        keywords: Set of keywords to match
        
    Returns:
        Match score (0.0 to 1.0)
    """
    if not keywords:
        return 0.5
    
    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword in text_lower)
    return min(matches / len(keywords), 1.0)
