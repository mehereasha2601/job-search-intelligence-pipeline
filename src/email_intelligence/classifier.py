"""
Email classification module.

Classifies recruiting emails into categories:
- applied: Application confirmation
- rejected: Rejection notification
- interview: Interview request
- assessment: Technical assessment invite
- follow_up: Recruiter follow-up
- unknown: Unclassified
"""

import logging
import re
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# Email classification keywords
CLASSIFICATION_RULES = {
    "applied": {
        "keywords": [
            "application received",
            "thank you for applying",
            "we received your application",
            "application confirmation",
            "received your resume",
            "successfully submitted",
            "application has been submitted",
        ],
        "subject_keywords": ["confirmation", "received", "submitted"],
    },
    "rejected": {
        "keywords": [
            "unfortunately",
            "not moving forward",
            "not selected",
            "decided to move forward with other candidates",
            "will not be moving forward",
            "not be proceeding",
            "chosen to pursue other candidates",
            "have decided not to",
            "regret to inform",
        ],
        "subject_keywords": ["application status", "regarding your application", "update"],
    },
    "interview": {
        "keywords": [
            "interview",
            "would like to speak",
            "schedule a call",
            "phone screen",
            "technical interview",
            "next steps",
            "invite you to",
            "meet with",
            "conversation about",
            "hiring manager would like",
        ],
        "subject_keywords": [
            "interview",
            "next steps",
            "schedule",
            "phone screen",
            "conversation",
        ],
    },
    "assessment": {
        "keywords": [
            "assessment",
            "coding challenge",
            "technical test",
            "hackerrank",
            "codility",
            "coderpad",
            "take-home",
            "complete the following",
            "online assessment",
        ],
        "subject_keywords": [
            "assessment",
            "challenge",
            "test",
            "hackerrank",
            "coding",
        ],
    },
    "follow_up": {
        "keywords": [
            "following up",
            "checking in",
            "wanted to reach out",
            "saw your profile",
            "interested in your background",
            "opportunity that might interest",
        ],
        "subject_keywords": [
            "opportunity",
            "role",
            "position",
            "interested",
        ],
    },
}


class EmailClassifier:
    """Classify recruiting emails into status categories."""
    
    def __init__(self, classification_rules: Optional[Dict] = None):
        """
        Initialize email classifier.
        
        Args:
            classification_rules: Custom classification rules
        """
        self.rules = classification_rules or CLASSIFICATION_RULES
    
    def classify(self, subject: str, body: str) -> Dict:
        """
        Classify an email based on subject and body.
        
        Args:
            subject: Email subject line
            body: Email body text
            
        Returns:
            Dict with:
                - category: str (applied, rejected, interview, assessment, follow_up, unknown)
                - confidence: float (0-1)
                - matched_keywords: list of matched keywords
        """
        subject_lower = subject.lower()
        body_lower = body.lower()
        combined = subject_lower + " " + body_lower
        
        best_category = "unknown"
        best_confidence = 0.0
        best_matches = []
        
        for category, rules in self.rules.items():
            matches = []
            
            # Check body keywords
            body_keywords = rules.get("keywords", [])
            for keyword in body_keywords:
                if keyword.lower() in combined:
                    matches.append(keyword)
            
            # Check subject keywords (higher weight)
            subject_keywords = rules.get("subject_keywords", [])
            subject_matches = 0
            for keyword in subject_keywords:
                if keyword.lower() in subject_lower:
                    matches.append(f"[subject] {keyword}")
                    subject_matches += 1
            
            # Calculate confidence
            if matches:
                # Subject matches have higher weight
                confidence = (len(matches) + subject_matches) / (len(body_keywords) + len(subject_keywords))
                confidence = min(confidence, 1.0)
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_category = category
                    best_matches = matches
        
        return {
            "category": best_category,
            "confidence": best_confidence,
            "matched_keywords": best_matches,
        }
    
    def classify_batch(self, emails: List[Dict]) -> List[Dict]:
        """
        Classify a batch of emails.
        
        Args:
            emails: List of email dicts with 'subject' and 'body'
            
        Returns:
            Emails with classification fields added
        """
        for email in emails:
            subject = email.get("subject", "")
            body = email.get("body", "")
            classification = self.classify(subject, body)
            email.update(classification)
        
        logger.info(f"Classified {len(emails)} emails")
        return emails


def is_rejection_email(subject: str, body: str) -> bool:
    """Quick check if email is a rejection."""
    text = (subject + " " + body).lower()
    rejection_indicators = [
        "unfortunately",
        "not moving forward",
        "not selected",
        "other candidates",
    ]
    return any(indicator in text for indicator in rejection_indicators)


def is_interview_email(subject: str, body: str) -> bool:
    """Quick check if email is an interview request."""
    text = (subject + " " + body).lower()
    interview_indicators = [
        "interview",
        "schedule a call",
        "phone screen",
        "next steps",
    ]
    return any(indicator in text for indicator in interview_indicators)


def is_spam_or_marketing(subject: str, body: str) -> bool:
    """Detect if email is spam or marketing."""
    text = (subject + " " + body).lower()
    spam_indicators = [
        "unsubscribe",
        "click here",
        "limited time offer",
        "special promotion",
        "newsletter",
        "weekly digest",
    ]
    return any(indicator in text for indicator in spam_indicators)
