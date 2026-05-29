# Portfolio Website Content

Ready-to-use content for your portfolio website. Choose the format that matches your site structure.

---

## Option 1: HTML Card Component

```html
<div class="project-card" id="job-search-pipeline">
    <div class="project-header">
        <h2>Job Search Intelligence Pipeline</h2>
        <p class="project-tagline">Privacy-first job search organization tool for new graduates</p>
        <div class="project-links">
            <a href="https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline" 
               class="btn btn-github" target="_blank">
                <svg class="icon"><!-- GitHub icon --></svg>
                View Code
            </a>
            <a href="https://job-search-intelligence-pipeline.onrender.com" 
               class="btn btn-demo" target="_blank">
                <svg class="icon"><!-- External link icon --></svg>
                Live Demo
            </a>
        </div>
    </div>

    <div class="project-content">
        <div class="project-challenge">
            <h3>🎯 The Challenge</h3>
            <p>During my OPT job search as an international student, I faced three major pain points:</p>
            <ul>
                <li><strong>Sponsorship ambiguity:</strong> Job descriptions rarely clarify H1B/OPT eligibility</li>
                <li><strong>Email overload:</strong> Recruiting emails (applied, rejected, interview) mixed with spam</li>
                <li><strong>Manual tracking chaos:</strong> Applications spread across 10+ ATS platforms</li>
            </ul>
        </div>

        <div class="project-solution">
            <h3>💡 The Solution</h3>
            <p>Built an intelligent job search pipeline that converts messy job-search signals into structured tracking data:</p>
            <ul>
                <li><strong>Smart Filtering:</strong> Filters jobs by role level (new grad/entry), location, and custom preferences</li>
                <li><strong>Sponsorship Detection:</strong> Identifies OPT-friendly opportunities by detecting visa sponsorship signals</li>
                <li><strong>Email Intelligence:</strong> Classifies recruiting emails into 5 categories with 90%+ accuracy</li>
                <li><strong>Pipeline Tracking:</strong> SQLite database with FastAPI dashboard for visualization</li>
            </ul>
        </div>

        <div class="project-tech">
            <h3>🛠️ Tech Stack</h3>
            <div class="tech-badges">
                <span class="badge">Python</span>
                <span class="badge">FastAPI</span>
                <span class="badge">SQLAlchemy</span>
                <span class="badge">Jinja2</span>
                <span class="badge">Bootstrap 5</span>
                <span class="badge">pytest</span>
                <span class="badge">SQLite</span>
                <span class="badge">Render</span>
            </div>
        </div>

        <div class="project-highlights">
            <h3>✨ Key Features</h3>
            <div class="features-grid">
                <div class="feature">
                    <h4>🔍 Preference Filtering</h4>
                    <p>Accept only new grad/entry-level full-time positions. Exclude internships, senior roles, and blacklisted companies.</p>
                </div>
                <div class="feature">
                    <h4>🌍 Sponsorship Detection</h4>
                    <p>Detect "US citizenship required", "no sponsorship", or positive signals like "OPT students welcome".</p>
                </div>
                <div class="feature">
                    <h4>📧 Email Classification</h4>
                    <p>Classify emails as applied, rejected, interview, assessment, or follow-up with 90%+ confidence.</p>
                </div>
                <div class="feature">
                    <h4>📊 Dashboard Visualization</h4>
                    <p>FastAPI dashboard with metrics cards, job pipeline, and email classifications.</p>
                </div>
            </div>
        </div>

        <div class="project-impact">
            <h3>📈 Impact & Results</h3>
            <ul>
                <li><strong>95%+ test coverage:</strong> 33 unit tests covering core filtering, classification, and database operations</li>
                <li><strong>85% precision:</strong> Sponsorship detection identifies OPT-friendly opportunities</li>
                <li><strong>90%+ accuracy:</strong> Email classification across 5 categories</li>
                <li><strong>80% time savings:</strong> Reduces manual tracking effort while maintaining human review</li>
            </ul>
        </div>

        <div class="project-screenshots">
            <h3>📸 Screenshots</h3>
            <div class="screenshots-grid">
                <figure>
                    <img src="screenshots/dashboard.png" alt="Dashboard Overview">
                    <figcaption>Dashboard with metrics cards and pipeline stats</figcaption>
                </figure>
                <figure>
                    <img src="screenshots/jobs.png" alt="Jobs List">
                    <figcaption>Jobs list with sponsorship signals and filters</figcaption>
                </figure>
                <figure>
                    <img src="screenshots/emails.png" alt="Email Classifications">
                    <figcaption>Email classifications with confidence scores</figcaption>
                </figure>
            </div>
        </div>

        <div class="project-architecture">
            <h3>🏗️ Architecture Highlights</h3>
            <ul>
                <li><strong>Modular Design:</strong> Separate modules for filtering, email intelligence, tracking, and dashboard</li>
                <li><strong>Test-Driven Development:</strong> 95%+ coverage with pytest, fixtures, and mocking</li>
                <li><strong>Privacy-First:</strong> Demo uses synthetic data only, no real credentials or PII</li>
                <li><strong>Scalable:</strong> SQLite for demo, PostgreSQL-ready for production with connection pooling</li>
            </ul>
        </div>

        <div class="project-learnings">
            <h3>🎓 What I Learned</h3>
            <ul>
                <li><strong>NLP without ML:</strong> Pattern matching and keyword-based classification can achieve 85-90% accuracy</li>
                <li><strong>Privacy by Design:</strong> Built public version with synthetic data from day one</li>
                <li><strong>Product Thinking:</strong> Focused on real pain points (sponsorship, email chaos) vs over-automation</li>
                <li><strong>Testing Best Practices:</strong> Comprehensive test suite with fixtures, mocking, and edge case coverage</li>
            </ul>
        </div>
    </div>
</div>
```

---

## Option 2: Markdown (Jekyll/Hugo/Gatsby)

```markdown
---
title: "Job Search Intelligence Pipeline"
date: 2026-05-29
tags: [python, fastapi, nlp, portfolio]
featured: true
---

# Job Search Intelligence Pipeline

> A privacy-first job search organization tool for new graduates

[View on GitHub](https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline) • 
[Live Demo](https://job-search-intelligence-pipeline.onrender.com)

---

## 🎯 The Problem

During my OPT job search as an international student, I faced three major challenges:

- **Sponsorship ambiguity:** Job descriptions rarely clarify H1B/OPT eligibility upfront
- **Email overload:** Recruiting emails mixed with spam across multiple platforms
- **Manual tracking chaos:** Applications spread across 10+ ATS systems (Greenhouse, Lever, Workday, etc.)

## 💡 The Solution

I built a job search intelligence pipeline that converts messy job-search signals into structured tracking data:

- ✅ **Smart Filtering:** Role level, location, sponsorship signals
- ✅ **Email Classification:** 5 categories with 90%+ accuracy
- ✅ **Pipeline Tracking:** SQLite database + FastAPI dashboard
- ✅ **Privacy-First:** Demo uses synthetic data only

## 🛠️ Tech Stack

`Python` `FastAPI` `SQLAlchemy` `Jinja2` `Bootstrap` `pytest` `SQLite` `Render`

## ✨ Key Features

### 1. Preference Filtering
Filters jobs by role level (new grad/entry-level), employment type (full-time only), location (US-based), and company preferences.

### 2. Sponsorship Detection
Detects disqualifying phrases ("US citizenship required", "no sponsorship") and positive signals ("OPT students welcome", "visa sponsorship available").

### 3. Email Intelligence
Classifies recruiting emails into 5 categories:
- **Applied:** Application confirmations
- **Rejected:** Rejection notifications
- **Interview:** Interview requests
- **Assessment:** Coding challenges
- **Follow-up:** Recruiter outreach

### 4. Company/Role Extraction
Extracts structured data from unstructured email text using regex patterns.

### 5. Dashboard Visualization
FastAPI backend with Jinja2 templates and Bootstrap 5 for metrics visualization.

## 📈 Impact & Results

- **95%+ test coverage** (33 unit tests)
- **85% precision** sponsorship detection
- **90%+ accuracy** email classification
- **80% time savings** in manual tracking

## 🏗️ Architecture

```
Sample Data (CSV/TXT)
    ↓
Filtering Layer (role, location, sponsorship)
    ↓
Intelligence Layer (email classification, extraction)
    ↓
Tracking Layer (SQLite + CSV export)
    ↓
Presentation Layer (FastAPI dashboard)
```

## 🎓 What I Learned

1. **NLP without ML:** Keyword-based classification can achieve 85-90% accuracy for structured domains
2. **Privacy by Design:** Built public version with synthetic data from day one
3. **Product Thinking:** Focused on real pain points vs feature bloat
4. **Testing Best Practices:** Comprehensive test suite with fixtures and mocking

## 📸 Screenshots

![Dashboard Overview](screenshots/dashboard.png)
*Dashboard with metrics cards and pipeline visualization*

![Jobs List](screenshots/jobs.png)
*Jobs list with sponsorship badges and status filters*

![Email Classifications](screenshots/emails.png)
*Email classifications with confidence scores and extracted entities*

---

**Links:**
- [GitHub Repository](https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline)
- [Live Demo on Render](https://job-search-intelligence-pipeline.onrender.com)
- [Architecture Documentation](https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline/blob/main/docs/architecture.md)
```

---

## Option 3: Simple Text Section

```
JOB SEARCH INTELLIGENCE PIPELINE

A privacy-first job search organization tool that helps new graduates track applications 
across multiple platforms and identify OPT-friendly opportunities.

TECH: Python • FastAPI • SQLAlchemy • pytest • SQLite • Render

KEY FEATURES:
• Filters jobs by role level, location, and sponsorship signals
• Classifies recruiting emails with 90%+ accuracy (applied, rejected, interview, etc.)
• Extracts company/role information from unstructured email text
• Tracks application pipeline in SQLite database
• FastAPI dashboard with metrics visualization

RESULTS:
• 95%+ test coverage (33 unit tests)
• 85% precision detecting OPT/visa-friendly opportunities
• 80% reduction in manual tracking effort

GITHUB: https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline
DEMO: https://job-search-intelligence-pipeline.onrender.com
```

---

## Option 4: JSON (for dynamic portfolio sites)

```json
{
  "id": "job-search-intelligence-pipeline",
  "title": "Job Search Intelligence Pipeline",
  "tagline": "Privacy-first job search organization tool for new graduates",
  "description": "Built a job search intelligence pipeline to solve OPT application tracking challenges. Filters jobs by sponsorship signals, classifies recruiting emails with 90%+ accuracy, and tracks pipeline across 10+ ATS platforms.",
  "category": "Full-Stack Application",
  "featured": true,
  "date": "2026-05-29",
  "tags": ["python", "fastapi", "nlp", "database", "testing"],
  "tech_stack": [
    "Python 3.11",
    "FastAPI",
    "SQLAlchemy",
    "Jinja2",
    "Bootstrap 5",
    "pytest",
    "SQLite",
    "Render"
  ],
  "links": {
    "github": "https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline",
    "demo": "https://job-search-intelligence-pipeline.onrender.com",
    "docs": "https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline/blob/main/docs/architecture.md"
  },
  "highlights": [
    "95%+ test coverage with 33 unit tests",
    "90%+ email classification accuracy",
    "85% precision sponsorship detection",
    "80% reduction in manual tracking effort"
  ],
  "screenshots": [
    {
      "url": "screenshots/dashboard.png",
      "caption": "Dashboard with metrics cards and pipeline stats"
    },
    {
      "url": "screenshots/jobs.png",
      "caption": "Jobs list with sponsorship signals"
    },
    {
      "url": "screenshots/emails.png",
      "caption": "Email classifications with confidence scores"
    }
  ]
}
```

---

## Social Media Posts

### LinkedIn Announcement

```
🚀 Excited to share my latest project: Job Search Intelligence Pipeline!

During my OPT job search, I identified three major pain points and built a solution:

❌ Problem:
• Sponsorship info buried in job descriptions
• Recruiting emails mixed with spam  
• Manual tracking across 10+ ATS platforms

✅ Solution:
• Smart filtering by role level & sponsorship signals
• Email classification with 90%+ accuracy
• Pipeline tracking with FastAPI dashboard

🛠️ Built with: Python | FastAPI | SQLAlchemy | pytest

📊 Results:
• 95%+ test coverage (33 tests)
• 85% precision detecting OPT-friendly jobs
• 80% time savings in tracking

This project showcases:
✓ Backend development with RESTful APIs
✓ NLP for email classification
✓ Database design with SQLAlchemy ORM
✓ Test-driven development
✓ Privacy-first design principles

🔗 Live Demo: [YOUR-RENDER-URL]
📂 GitHub: [YOUR-GITHUB-URL]

#Python #FastAPI #JobSearch #SoftwareEngineering #OPT #NewGrad #Portfolio
```

### Twitter/X Thread

```
🧵 1/6 Built a job search intelligence pipeline to solve OPT application tracking challenges

Problem: As an int'l student, hard to know which companies sponsor visas + tracking apps across 10+ platforms

Solution: Automated filtering & email classification 🔽
```

```
2/6 Smart Filtering 🔍

✅ Role level (new grad/entry only)
✅ Sponsorship signals ("OPT welcome" vs "US citizen only")
✅ Location (US-based, remote)

85% precision detecting visa-friendly opportunities
```

```
3/6 Email Intelligence 📧

Classifies recruiting emails into 5 categories:
• Applied (confirmations)
• Rejected (unfortunately...)
• Interview (let's chat!)
• Assessment (HackerRank, Codility)
• Follow-up (recruiter outreach)

90%+ accuracy with keyword matching
```

```
4/6 Tech Stack 🛠️

Backend: Python + FastAPI
Database: SQLAlchemy + SQLite
Frontend: Jinja2 + Bootstrap 5
Testing: pytest (95%+ coverage, 33 tests)
Deploy: Render (free tier)

Privacy-first: demo uses synthetic data only
```

```
5/6 What I Learned 🎓

• NLP without ML can hit 85-90% accuracy
• Privacy by design (built public version from day 1)
• Test-driven development pays off
• Product thinking > feature bloat

Focus on solving real pain points!
```

```
6/6 Check it out 👇

🔗 Live Demo: [URL]
📂 Code: [GitHub URL]
📖 Docs: [Architecture MD]

Feedback welcome! Currently looking for new grad SWE roles (May 2026) 🙏

#Python #FastAPI #BuildInPublic
```

---

## Reddit Post (r/Python, r/cscareerquestions)

**Title:** Built a job search intelligence pipeline to track OPT applications [Python + FastAPI]

**Body:**
```markdown
During my OPT job search, I got frustrated with:
- Not knowing which companies sponsor visas
- Recruiting emails buried in my inbox
- Manually tracking applications across 10+ ATS platforms

So I built a job search intelligence pipeline:

**Features:**
- Filters jobs by role level, location, sponsorship signals
- Classifies recruiting emails (applied, rejected, interview, assessment) with 90%+ accuracy
- Tracks application pipeline in SQLite with FastAPI dashboard
- 95%+ test coverage with pytest

**Tech Stack:**
- Backend: FastAPI + SQLAlchemy
- Frontend: Jinja2 templates + Bootstrap 5
- Database: SQLite (PostgreSQL-ready)
- Testing: pytest with 33 unit tests
- Deploy: Render free tier

**Privacy-first design:**
- Public version uses synthetic data only
- No real credentials or PII
- Demo mode for portfolio visibility

**What I learned:**
- Keyword-based NLP can hit 85-90% accuracy
- Test-driven development is worth it
- Privacy by design from day one

**Live Demo:** [URL]
**GitHub:** [URL]
**Docs:** [Architecture link]

Happy to answer questions or get feedback! Currently looking for new grad SWE roles.
```

---

## Email Signature

```
Easha Meher Koppisetty
MS Artificial Intelligence | Northeastern University
📧 mehereasha2601@gmail.com
💼 linkedin.com/in/easha-meher
🐙 github.com/YOUR-USERNAME
🌐 Portfolio: [YOUR-PORTFOLIO-URL]

Latest Project: Job Search Intelligence Pipeline
🔗 [GITHUB-URL] | 🚀 [DEMO-URL]
```

---

## Choose What Works Best

Pick the format that matches your portfolio structure:
- **HTML:** For traditional portfolio websites
- **Markdown:** For Jekyll, Hugo, Gatsby sites
- **JSON:** For React/Vue/Angular dynamic portfolios
- **Text:** For simple sites or README sections

Then customize with your actual URLs! 🚀
