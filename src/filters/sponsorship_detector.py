"""
Sponsorship and OPT signal detection module.

Detects:
- Negative signals: citizenship requirements, security clearance, no sponsorship
- Positive signals: OPT-friendly, sponsorship available, international students welcome
- Neutral: No clear signals
"""

import logging
import re
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


# Disqualifying phrases (strong negative signals)
DISQUALIFYING_PHRASES = [
    "us citizen only",
    "us citizenship required",
    "must be a us citizen",
    "security clearance required",
    "active security clearance",
    "secret clearance",
    "top secret clearance",
    "ts/sci clearance",
    "no sponsorship",
    "cannot provide sponsorship",
    "will not sponsor",
    "not providing sponsorship",
    "unable to sponsor",
    "not sponsoring",
    "permanent resident only",
    "green card required",
    "must have work authorization",
    "authorized to work without sponsorship",
    "no visa sponsorship",
]

# Positive signals (OPT/sponsorship friendly)
POSITIVE_SIGNALS = [
    "opt students welcome",
    "opt eligible",
    "f-1 students",
    "f1 visa",
    "opt/cpt",
    "will sponsor",
    "sponsorship available",
    "h1b sponsorship",
    "visa sponsorship available",
    "international students welcome",
    "work authorization sponsorship",
    "can sponsor",
    "provides visa sponsorship",
]

# Soft negative signals (proceed with caution)
SOFT_NEGATIVE_SIGNALS = [
    "prefer us work authorization",
    "preferred: us citizen",
    "citizenship preferred",
]


class SponsorshipDetector:
    """Detect sponsorship and OPT signals in job descriptions."""
    
    def __init__(
        self,
        disqualifying_phrases: Optional[list] = None,
        positive_signals: Optional[list] = None,
        soft_negative_signals: Optional[list] = None,
    ):
        """
        Initialize sponsorship detector.
        
        Args:
            disqualifying_phrases: Hard blockers
            positive_signals: OPT/sponsorship friendly indicators
            soft_negative_signals: Proceed-with-caution indicators
        """
        self.disqualifying_phrases = disqualifying_phrases or DISQUALIFYING_PHRASES
        self.positive_signals = positive_signals or POSITIVE_SIGNALS
        self.soft_negative_signals = soft_negative_signals or SOFT_NEGATIVE_SIGNALS
    
    def analyze(self, description: str, title: str = "") -> Dict:
        """
        Analyze job description for sponsorship signals.
        
        Args:
            description: Job description text
            title: Job title (optional)
            
        Returns:
            Dict with:
                - status: "disqualified", "positive", "soft_negative", "neutral"
                - confidence: float 0-1
                - signals: list of detected phrases
                - recommendation: str
        """
        text = (title + " " + description).lower()
        
        # Check for disqualifying phrases
        disqualifying_found = []
        for phrase in self.disqualifying_phrases:
            if phrase.lower() in text:
                disqualifying_found.append(phrase)
        
        if disqualifying_found:
            return {
                "status": "disqualified",
                "confidence": 0.95,
                "signals": disqualifying_found,
                "recommendation": "Skip - citizenship/clearance required or no sponsorship",
                "sponsors_visa": False,
            }
        
        # Check for positive signals
        positive_found = []
        for signal in self.positive_signals:
            if signal.lower() in text:
                positive_found.append(signal)
        
        if positive_found:
            return {
                "status": "positive",
                "confidence": 0.85,
                "signals": positive_found,
                "recommendation": "Apply - OPT/sponsorship friendly",
                "sponsors_visa": True,
            }
        
        # Check for soft negative signals
        soft_negative_found = []
        for signal in self.soft_negative_signals:
            if signal.lower() in text:
                soft_negative_found.append(signal)
        
        if soft_negative_found:
            return {
                "status": "soft_negative",
                "confidence": 0.60,
                "signals": soft_negative_found,
                "recommendation": "Proceed with caution - citizenship preferred but not required",
                "sponsors_visa": None,  # Unknown
            }
        
        # No clear signals found
        return {
            "status": "neutral",
            "confidence": 0.50,
            "signals": [],
            "recommendation": "Apply with caution - no clear sponsorship info",
            "sponsors_visa": None,  # Unknown
        }
    
    def is_opt_friendly(self, description: str, title: str = "") -> bool:
        """
        Check if job is OPT-friendly (quick check).
        
        Returns:
            True if OPT-friendly or neutral, False if disqualified
        """
        result = self.analyze(description, title)
        return result["status"] != "disqualified"
    
    def requires_citizenship(self, description: str, title: str = "") -> bool:
        """Check if job requires US citizenship."""
        text = (title + " " + description).lower()
        citizenship_patterns = [
            r"us citizen(ship)? required",
            r"must be (a )?us citizen",
            r"only us citizens",
            r"citizenship required",
        ]
        return any(re.search(pattern, text) for pattern in citizenship_patterns)
    
    def requires_clearance(self, description: str, title: str = "") -> bool:
        """Check if job requires security clearance."""
        text = (title + " " + description).lower()
        clearance_keywords = [
            "security clearance",
            "secret clearance",
            "top secret",
            "ts/sci",
            "active clearance",
        ]
        return any(keyword in text for keyword in clearance_keywords)


def detect_sponsorship_status(description: str, title: str = "") -> str:
    """
    Quick helper to detect sponsorship status.
    
    Returns:
        "disqualified", "positive", "soft_negative", or "neutral"
    """
    detector = SponsorshipDetector()
    result = detector.analyze(description, title)
    return result["status"]


def extract_work_authorization_text(description: str) -> Optional[str]:
    """
    Extract work authorization section from job description.
    
    Returns:
        Relevant text snippet or None
    """
    text_lower = description.lower()
    
    # Look for work authorization section
    patterns = [
        r"(work authorization:?.{0,200})",
        r"(visa.{0,100}sponsor.{0,100})",
        r"(citizenship.{0,100}required.{0,100})",
        r"(security clearance.{0,100})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None
