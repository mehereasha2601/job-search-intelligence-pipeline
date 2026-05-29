"""
Extractors for company names, role titles, and other entities from emails.
"""

import logging
import re
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


# Common ATS/platform senders
ATS_DOMAINS = {
    "greenhouse.io": "Greenhouse",
    "lever.co": "Lever",
    "workday.com": "Workday",
    "myworkday.com": "Workday",
    "icims.com": "iCIMS",
    "taleo.net": "Taleo",
    "jobvite.com": "Jobvite",
    "smartrecruiters.com": "SmartRecruiters",
    "ashbyhq.com": "Ashby",
    "handshake.com": "Handshake",
}


def extract_company_from_sender(sender: str) -> Optional[str]:
    """
    Extract company name from email sender.
    
    Args:
        sender: Email sender (e.g., "recruiter@google.com" or "Jane Doe <jane@stripe.com>")
        
    Returns:
        Company name or None
    """
    # Extract email from "Name <email>" format
    email_match = re.search(r'<([^>]+)>', sender)
    if email_match:
        email = email_match.group(1)
    else:
        email = sender
    
    # Extract domain
    domain_match = re.search(r'@([a-z0-9\-\.]+)', email.lower())
    if not domain_match:
        return None
    
    domain = domain_match.group(1)
    
    # Check if it's a known ATS domain
    for ats_domain, ats_name in ATS_DOMAINS.items():
        if ats_domain in domain:
            return None  # Don't return ATS name as company
    
    # Extract company name from domain
    # Remove common prefixes and TLD
    domain_parts = domain.split('.')
    if len(domain_parts) >= 2:
        company = domain_parts[-2]  # Second-to-last part
        
        # Remove common prefixes
        for prefix in ["noreply", "no-reply", "info", "careers", "jobs", "recruiting"]:
            if company.startswith(prefix):
                company = company[len(prefix):].lstrip("-")
        
        if company:
            return company.title()
    
    return None


def extract_company_from_body(body: str) -> Optional[str]:
    """
    Extract company name from email body using patterns.
    
    Args:
        body: Email body text
        
    Returns:
        Company name or None
    """
    # Pattern 1: "at [Company]"
    match = re.search(r'\bat\s+([A-Z][a-zA-Z0-9\s&\.]{2,40}?)(?:\s+for|\s+as|\s+in|\.|,|\s*$)', body)
    if match:
        return match.group(1).strip()
    
    # Pattern 2: "[Company] is hiring"
    match = re.search(r'([A-Z][a-zA-Z0-9\s&\.]{2,40}?)\s+is\s+(?:hiring|looking|seeking)', body)
    if match:
        return match.group(1).strip()
    
    # Pattern 3: "behalf of [Company]"
    match = re.search(r'behalf\s+of\s+([A-Z][a-zA-Z0-9\s&\.]{2,40}?)(?:\.|,|\s*$)', body)
    if match:
        return match.group(1).strip()
    
    return None


def extract_role_from_subject(subject: str) -> Optional[str]:
    """
    Extract job role/title from email subject.
    
    Args:
        subject: Email subject line
        
    Returns:
        Role title or None
    """
    # Pattern 1: "for [Role] position"
    match = re.search(r'for\s+(.+?)\s+(?:position|role)', subject, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Pattern 2: "[Role] - Application"
    match = re.search(r'^(.+?)\s+[-–—]\s+(?:Application|Interview|Assessment)', subject, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Pattern 3: "Your [Role] application"
    match = re.search(r'your\s+(.+?)\s+application', subject, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return None


def extract_role_from_body(body: str) -> Optional[str]:
    """
    Extract job role from email body.
    
    Args:
        body: Email body text
        
    Returns:
        Role title or None
    """
    # Pattern 1: "for the [Role] position"
    match = re.search(r'for\s+the\s+(.+?)\s+(?:position|role)', body, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Pattern 2: "applied for [Role]"
    match = re.search(r'applied\s+for\s+(?:the\s+)?(.+?)\s+(?:at|with|position)', body, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Pattern 3: "Position: [Role]"
    match = re.search(r'position:\s*(.+?)(?:\n|\.|\|)', body, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return None


def extract_application_id(body: str) -> Optional[str]:
    """
    Extract application ID from email body.
    
    Args:
        body: Email body text
        
    Returns:
        Application ID or None
    """
    # Pattern 1: "Application ID: [ID]"
    match = re.search(r'application\s+(?:id|number|ref):\s*([A-Z0-9\-]+)', body, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Pattern 2: "[ID] - Application"
    match = re.search(r'([A-Z0-9]{6,})\s*[-–—]\s*application', body, re.IGNORECASE)
    if match:
        return match.group(1)
    
    return None


class EmailExtractor:
    """Extract structured information from recruiting emails."""
    
    def extract_all(self, sender: str, subject: str, body: str) -> Dict:
        """
        Extract all available information from an email.
        
        Args:
            sender: Email sender
            subject: Email subject
            body: Email body
            
        Returns:
            Dict with extracted fields:
                - company: Company name
                - role: Job role/title
                - application_id: Application ID (if present)
                - ats_platform: Detected ATS platform
        """
        # Extract company
        company = extract_company_from_sender(sender)
        if not company:
            company = extract_company_from_body(body)
        
        # Extract role
        role = extract_role_from_subject(subject)
        if not role:
            role = extract_role_from_body(body)
        
        # Extract application ID
        app_id = extract_application_id(body)
        
        # Detect ATS platform
        ats_platform = self._detect_ats_platform(sender)
        
        result = {
            "company": company,
            "role": role,
            "application_id": app_id,
            "ats_platform": ats_platform,
        }
        
        logger.debug(f"Extracted: company={company}, role={role}, ats={ats_platform}")
        return result
    
    def _detect_ats_platform(self, sender: str) -> Optional[str]:
        """Detect which ATS platform sent the email."""
        sender_lower = sender.lower()
        for domain, platform in ATS_DOMAINS.items():
            if domain in sender_lower:
                return platform
        return None
    
    def extract_from_batch(self, emails: List[Dict]) -> List[Dict]:
        """
        Extract information from a batch of emails.
        
        Args:
            emails: List of email dicts with 'sender', 'subject', 'body'
            
        Returns:
            Emails with extracted fields added
        """
        for email in emails:
            sender = email.get("sender", "")
            subject = email.get("subject", "")
            body = email.get("body", "")
            
            extracted = self.extract_all(sender, subject, body)
            email.update(extracted)
        
        logger.info(f"Extracted information from {len(emails)} emails")
        return emails


def normalize_company_name(company: str) -> str:
    """Normalize company name for matching."""
    if not company:
        return ""
    
    # Remove common suffixes
    suffixes = ["Inc", "Inc.", "LLC", "Ltd", "Ltd.", "Corporation", "Corp", "Corp."]
    normalized = company
    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)].strip()
    
    return normalized.strip()
