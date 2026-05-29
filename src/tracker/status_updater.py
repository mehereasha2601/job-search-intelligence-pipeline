"""
Status updater module.

Updates job application status based on email classification.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class StatusUpdater:
    """Update application status based on email intelligence."""
    
    def __init__(self, database):
        """
        Initialize status updater.
        
        Args:
            database: TrackerDatabase instance
        """
        self.database = database
    
    def update_from_email(self, email: Dict) -> Optional[str]:
        """
        Update application status based on email classification.
        
        Args:
            email: Email dict with 'category', 'company', 'role'
            
        Returns:
            New status or None if not found
        """
        category = email.get("category")
        company = email.get("company")
        role = email.get("role")
        
        if not company:
            logger.warning("No company extracted from email - cannot update status")
            return None
        
        # Map email category to application status
        status_mapping = {
            "applied": "applied",
            "rejected": "rejected",
            "interview": "interview",
            "assessment": "assessment",
            "follow_up": "discovered",  # Keep as discovered
        }
        
        new_status = status_mapping.get(category)
        if not new_status:
            logger.debug(f"No status mapping for category: {category}")
            return None
        
        # Update in database
        if role:
            self.database.update_status(company, role, new_status)
        else:
            # If no role, try to find any job from this company
            jobs = self.database.get_all_jobs()
            for job in jobs:
                if job["company"].lower() == company.lower():
                    self.database.update_status(job["company"], job["title"], new_status)
                    logger.info(f"Updated {job['company']} - {job['title']} to {new_status}")
                    return new_status
        
        return new_status
    
    def update_from_emails_batch(self, emails: List[Dict]) -> Dict:
        """
        Update statuses from a batch of emails.
        
        Args:
            emails: List of classified and extracted emails
            
        Returns:
            Summary dict with update counts
        """
        updates = {
            "applied": 0,
            "rejected": 0,
            "interview": 0,
            "assessment": 0,
            "not_found": 0,
        }
        
        for email in emails:
            try:
                new_status = self.update_from_email(email)
                if new_status:
                    updates[new_status] = updates.get(new_status, 0) + 1
                else:
                    updates["not_found"] += 1
            except Exception as e:
                logger.error(f"Error updating from email: {e}")
                continue
        
        logger.info(f"Status updates: {updates}")
        return updates


def map_email_to_status(email_category: str) -> Optional[str]:
    """Map email category to application status."""
    mapping = {
        "applied": "applied",
        "rejected": "rejected",
        "interview": "interview",
        "assessment": "assessment",
    }
    return mapping.get(email_category)
