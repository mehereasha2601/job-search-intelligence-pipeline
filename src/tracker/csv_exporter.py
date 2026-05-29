"""
CSV exporter for application data.
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)


class CSVExporter:
    """Export application data to CSV."""
    
    def export_jobs(self, jobs: List[Dict], output_path: Path):
        """
        Export jobs to CSV file.
        
        Args:
            jobs: List of job dictionaries
            output_path: Path to output CSV file
        """
        if not jobs:
            logger.warning("No jobs to export")
            return
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Define CSV columns
        fieldnames = [
            "company",
            "title",
            "location",
            "url",
            "source",
            "status",
            "relevance_score",
            "sponsorship_status",
            "date_discovered",
            "date_applied",
            "notes",
            "rejection_reason",
        ]
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(jobs)
            
            logger.info(f"Exported {len(jobs)} jobs to {output_path}")
        
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise
    
    def export_by_status(self, database, output_dir: Path):
        """
        Export jobs grouped by status to separate CSV files.
        
        Args:
            database: TrackerDatabase instance
            output_dir: Output directory
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        statuses = ["discovered", "approved", "applied", "rejected", "interview", "filtered_out"]
        
        for status in statuses:
            jobs = database.get_jobs_by_status(status)
            if jobs:
                output_path = output_dir / f"{status}.csv"
                self.export_jobs(jobs, output_path)


def export_demo_results(
    filtered_jobs: List[Dict],
    rejected_jobs: List[Dict],
    email_classifications: List[Dict],
    output_dir: Path
):
    """
    Export demo results to multiple CSV files.
    
    Args:
        filtered_jobs: Jobs that passed filters
        rejected_jobs: Jobs that were filtered out
        email_classifications: Classified emails
        output_dir: Output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    exporter = CSVExporter()
    
    # Export filtered jobs
    if filtered_jobs:
        exporter.export_jobs(filtered_jobs, output_dir / "approved_jobs.csv")
    
    # Export rejected jobs
    if rejected_jobs:
        exporter.export_jobs(rejected_jobs, output_dir / "rejected_jobs.csv")
    
    # Export email classifications
    if email_classifications:
        fieldnames = ["sender", "subject", "category", "confidence", "company", "role", "ats_platform"]
        with open(output_dir / "email_classifications.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(email_classifications)
        
        logger.info(f"Exported {len(email_classifications)} email classifications")
    
    logger.info(f"Demo results exported to {output_dir}")
