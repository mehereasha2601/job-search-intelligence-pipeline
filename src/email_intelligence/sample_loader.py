"""
Sample data loader for demo mode.
"""

import csv
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


def load_sample_emails(sample_dir: Path) -> List[Dict]:
    """
    Load sample emails from text files.
    
    Args:
        sample_dir: Directory containing sample email files
        
    Returns:
        List of email dictionaries
    """
    emails = []
    email_dir = sample_dir / "emails"
    
    if not email_dir.exists():
        logger.warning(f"Sample email directory not found: {email_dir}")
        return emails
    
    for email_file in email_dir.glob("*.txt"):
        try:
            with open(email_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Parse email format (simple parser)
                lines = content.split('\n')
                sender = ""
                subject = ""
                body_lines = []
                
                in_body = False
                for line in lines:
                    if line.startswith("From:"):
                        sender = line.replace("From:", "").strip()
                    elif line.startswith("Subject:"):
                        subject = line.replace("Subject:", "").strip()
                    elif line.strip() == "":
                        in_body = True
                    elif in_body:
                        body_lines.append(line)
                
                body = "\n".join(body_lines)
                
                emails.append({
                    "sender": sender,
                    "subject": subject,
                    "body": body,
                    "source_file": email_file.name,
                })
                
                logger.debug(f"Loaded email from {email_file.name}")
        
        except Exception as e:
            logger.error(f"Error loading {email_file.name}: {e}")
            continue
    
    logger.info(f"Loaded {len(emails)} sample emails")
    return emails


def load_sample_jobs(sample_dir: Path) -> List[Dict]:
    """
    Load sample jobs from CSV file.
    
    Args:
        sample_dir: Directory containing jobs.csv
        
    Returns:
        List of job dictionaries
    """
    jobs = []
    jobs_file = sample_dir / "jobs.csv"
    
    if not jobs_file.exists():
        logger.warning(f"Sample jobs file not found: {jobs_file}")
        return jobs
    
    try:
        with open(jobs_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            jobs = list(reader)
        
        logger.info(f"Loaded {len(jobs)} sample jobs from {jobs_file}")
    
    except Exception as e:
        logger.error(f"Error loading jobs from {jobs_file}: {e}")
    
    return jobs
