"""
Job Search Intelligence Pipeline

A privacy-first job search organization tool for new graduates.
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils import setup_logging, get_logger
from src.filters import PreferenceFilter, SponsorshipDetector, RelevanceScorer
from src.email_intelligence import (
    EmailClassifier,
    EmailExtractor,
    load_sample_emails,
    load_sample_jobs,
)
from src.tracker import TrackerDatabase, StatusUpdater, export_demo_results


logger = get_logger(__name__)


def run_demo():
    """Run demo mode with synthetic data."""
    print("\n" + "=" * 80)
    print("Job Search Intelligence Pipeline - DEMO MODE")
    print("=" * 80 + "\n")
    
    # Setup paths
    sample_dir = Path("sample_data")
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    print("🔧 Initializing components...")
    preference_filter = PreferenceFilter()
    sponsorship_detector = SponsorshipDetector()
    relevance_scorer = RelevanceScorer(
        target_skills=["python", "machine learning", "backend", "distributed systems"],
        preferred_companies=["google", "stripe", "meta"],
    )
    email_classifier = EmailClassifier()
    email_extractor = EmailExtractor()
    
    # Load sample data
    print(f"📂 Loading sample data from {sample_dir}...")
    jobs = load_sample_jobs(sample_dir)
    emails = load_sample_emails(sample_dir)
    
    print(f"   Loaded {len(jobs)} sample jobs")
    print(f"   Loaded {len(emails)} sample emails\n")
    
    # Step 1: Filter jobs by preferences
    print("🔍 Step 1: Applying preference filters...")
    accepted_jobs, rejected_jobs = preference_filter.filter_jobs(jobs)
    print(f"   ✓ {len(accepted_jobs)} jobs passed filters")
    print(f"   ✗ {len(rejected_jobs)} jobs filtered out\n")
    
    # Step 2: Detect sponsorship signals
    print("🌍 Step 2: Detecting OPT/sponsorship signals...")
    for job in accepted_jobs:
        result = sponsorship_detector.analyze(job.get("description", ""), job.get("title", ""))
        job["sponsorship_status"] = result["status"]
        job["sponsorship_signals"] = result["signals"]
    
    sponsorship_friendly = sum(1 for j in accepted_jobs if j.get("sponsorship_status") == "positive")
    print(f"   ✓ {sponsorship_friendly} jobs are OPT/sponsorship-friendly")
    print(f"   ⚠ {len(accepted_jobs) - sponsorship_friendly} jobs have unclear sponsorship info\n")
    
    # Step 3: Calculate relevance scores
    print("📊 Step 3: Calculating relevance scores...")
    accepted_jobs = relevance_scorer.score_jobs(accepted_jobs)
    top_score = max(j.get("relevance_score", 0) for j in accepted_jobs) if accepted_jobs else 0
    print(f"   ✓ Scored {len(accepted_jobs)} jobs (top score: {top_score:.2f})\n")
    
    # Step 4: Classify emails
    print("📧 Step 4: Classifying recruiting emails...")
    classified_emails = email_classifier.classify_batch(emails)
    extracted_emails = email_extractor.extract_from_batch(classified_emails)
    
    email_stats = {}
    for email in extracted_emails:
        category = email.get("category", "unknown")
        email_stats[category] = email_stats.get(category, 0) + 1
    
    print(f"   Email classification results:")
    for category, count in sorted(email_stats.items()):
        print(f"     • {category}: {count}")
    print()
    
    # Step 5: Save results
    print("💾 Step 5: Exporting results...")
    export_demo_results(
        filtered_jobs=accepted_jobs,
        rejected_jobs=rejected_jobs,
        email_classifications=extracted_emails,
        output_dir=output_dir
    )
    print(f"   ✓ Results saved to {output_dir}/\n")
    
    # Step 6: Create demo database
    print("🗄️  Step 6: Creating demo database...")
    db = TrackerDatabase(output_dir / "demo_tracker.db")
    
    # Add accepted jobs to database
    for job in accepted_jobs:
        job["status"] = "approved"  # Mark as approved in demo
        db.add_job(job)
    
    # Add rejected jobs as filtered_out
    for job in rejected_jobs:
        job["status"] = "filtered_out"
        db.add_job(job)
    
    # Update statuses from emails
    status_updater = StatusUpdater(db)
    update_summary = status_updater.update_from_emails_batch(extracted_emails)
    
    stats = db.get_stats()
    print(f"   ✓ Database created with {stats['total']} jobs")
    print(f"     • Approved: {stats['approved']}")
    print(f"     • Filtered out: {stats['filtered_out']}")
    print(f"     • Applied: {stats['applied']}")
    print(f"     • Interview: {stats['interview']}")
    print(f"     • Rejected: {stats['rejected']}\n")
    
    # Summary
    print("=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print(f"\nResults saved to:")
    print(f"  • {output_dir}/approved_jobs.csv")
    print(f"  • {output_dir}/rejected_jobs.csv")
    print(f"  • {output_dir}/email_classifications.csv")
    print(f"  • {output_dir}/demo_tracker.db")
    print(f"\nTo view in dashboard, run:")
    print(f"  python main.py --dashboard\n")


def run_dashboard():
    """Launch FastAPI dashboard."""
    print("\n🚀 Starting dashboard on http://localhost:8000\n")
    print("   Press Ctrl+C to stop\n")
    
    import uvicorn
    from src.dashboard.app import create_app
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Job Search Intelligence Pipeline - Demo Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo       Run demo with synthetic data
  python main.py --dashboard  Launch web dashboard
        """
    )
    
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--dashboard", action="store_true", help="Launch dashboard")
    parser.add_argument("--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level)
    
    if not args.demo and not args.dashboard:
        parser.print_help()
        return
    
    try:
        if args.demo:
            run_demo()
        
        if args.dashboard:
            run_dashboard()
    
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
