"""
Database module for tracking job applications.

Uses SQLite with SQLAlchemy ORM.
"""

import logging
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional, Dict

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


class Application(Base):
    """Job application model."""
    
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    location = Column(String(255))
    url = Column(String(2048))
    source = Column(String(50))  # linkedin, indeed, handshake, etc.
    status = Column(String(50), nullable=False, default="discovered", index=True)
    # Status options: discovered, filtered_out, approved, applied, rejected, interview, assessment
    
    relevance_score = Column(Float)
    sponsorship_status = Column(String(50))  # disqualified, positive, neutral, soft_negative
    
    date_discovered = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_applied = Column(DateTime)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    notes = Column(Text)
    rejection_reason = Column(String(255))
    
    def __repr__(self):
        return f"<Application {self.company} - {self.title} ({self.status})>"


class TrackerDatabase:
    """Database manager for application tracking."""
    
    def __init__(self, db_path: Path = None):
        """
        Initialize database.
        
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = Path("output/tracker.db")
        
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
        logger.info(f"Database initialized at {db_path}")
    
    @contextmanager
    def get_session(self):
        """Context manager for database sessions."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def add_job(self, job: Dict) -> Optional[Application]:
        """
        Add a new job to the database.
        
        Args:
            job: Job dictionary
            
        Returns:
            Application object or None if duplicate
        """
        with self.get_session() as session:
            # Check for duplicate
            existing = session.query(Application).filter(
                Application.company == job.get("company"),
                Application.title == job.get("title")
            ).first()
            
            if existing:
                logger.debug(f"Duplicate job: {job.get('company')} - {job.get('title')}")
                return None
            
            app = Application(
                company=job.get("company", ""),
                title=job.get("title", ""),
                location=job.get("location", ""),
                url=job.get("url", ""),
                source=job.get("source", "demo"),
                status=job.get("status", "discovered"),
                relevance_score=job.get("relevance_score"),
                sponsorship_status=job.get("sponsorship_status"),
                date_discovered=datetime.utcnow(),
            )
            
            session.add(app)
            session.flush()
            logger.debug(f"Added job: {app.company} - {app.title}")
            return app
    
    def update_status(self, company: str, title: str, new_status: str):
        """Update application status."""
        with self.get_session() as session:
            app = session.query(Application).filter(
                Application.company == company,
                Application.title == title
            ).first()
            
            if app:
                app.status = new_status
                app.date_updated = datetime.utcnow()
                
                if new_status == "applied":
                    app.date_applied = datetime.utcnow()
                
                logger.info(f"Updated status: {company} - {title} -> {new_status}")
    
    def get_jobs_by_status(self, status: str) -> List[Application]:
        """Get all jobs with a specific status."""
        with self.get_session() as session:
            jobs = session.query(Application).filter(
                Application.status == status
            ).order_by(Application.date_discovered.desc()).all()
            
            # Detach from session (convert to dict-like objects)
            result = [{
                "id": job.id,
                "company": job.company,
                "title": job.title,
                "location": job.location,
                "status": job.status,
                "relevance_score": job.relevance_score,
                "sponsorship_status": job.sponsorship_status,
                "date_discovered": job.date_discovered,
            } for job in jobs]
            
            return result
    
    def get_stats(self) -> Dict:
        """Get application statistics."""
        with self.get_session() as session:
            total = session.query(Application).count()
            discovered = session.query(Application).filter(Application.status == "discovered").count()
            approved = session.query(Application).filter(Application.status == "approved").count()
            applied = session.query(Application).filter(Application.status == "applied").count()
            rejected = session.query(Application).filter(Application.status == "rejected").count()
            interview = session.query(Application).filter(Application.status == "interview").count()
            filtered_out = session.query(Application).filter(Application.status == "filtered_out").count()
            
            return {
                "total": total,
                "discovered": discovered,
                "approved": approved,
                "applied": applied,
                "rejected": rejected,
                "interview": interview,
                "filtered_out": filtered_out,
            }
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs as dictionaries."""
        with self.get_session() as session:
            jobs = session.query(Application).order_by(Application.date_discovered.desc()).all()
            
            return [{
                "id": job.id,
                "company": job.company,
                "title": job.title,
                "location": job.location,
                "url": job.url,
                "source": job.source,
                "status": job.status,
                "relevance_score": job.relevance_score,
                "sponsorship_status": job.sponsorship_status,
                "date_discovered": job.date_discovered.isoformat() if job.date_discovered else None,
                "date_applied": job.date_applied.isoformat() if job.date_applied else None,
                "notes": job.notes,
                "rejection_reason": job.rejection_reason,
            } for job in jobs]
