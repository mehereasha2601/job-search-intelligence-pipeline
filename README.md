# Job Search Intelligence Pipeline

> A privacy-first job search organization tool that converts messy job signals into structured tracking data for new graduates.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Overview

During my OPT job search as an international student, I faced challenges tracking applications across multiple platforms (Workday, Handshake, Greenhouse, Lever) and classifying recruiting emails. This project converts messy job-search signals into structured application tracking data while keeping a human review step.

**This is a demo/portfolio version using synthetic data only.** It focuses on the intelligence layer—filtering, sponsorship detection, and email classification—rather than automation.

---

## 🎯 Problem Statement

New graduates, especially international students on F1 visas, face several challenges:

1. **Manual tracking chaos**: Applications spread across 10+ ATS platforms (Greenhouse, Lever, Workday, iCIMS, etc.)
2. **Sponsorship ambiguity**: Job descriptions rarely clarify H1B/OPT eligibility upfront
3. **Email overload**: Recruiting emails (applied, rejected, interview, assessment) mixed with spam
4. **Relevance filtering**: Need to filter out senior roles, internships, and non-target positions
5. **Status tracking**: Difficult to know which stage each application is in

---

## ✨ Solution

A **Job Search Intelligence Pipeline** that:

- **Filters jobs** by role level (new grad/entry-level), employment type, location, and custom preferences
- **Detects OPT/sponsorship signals** in job descriptions (citizenship requirements, security clearance, visa sponsorship)
- **Classifies recruiting emails** into categories: applied, rejected, interview, assessment, follow-up
- **Extracts structured data** from emails (company name, role, ATS platform)
- **Tracks application status** in SQLite database with CSV export
- **Visualizes pipeline** via FastAPI dashboard

---

## 🚀 Features

### Job Filtering

- ✅ **Role level filtering**: Accept only new grad, entry-level, junior, associate, L3/L4
- ✅ **Employment type filtering**: Full-time only (exclude internships, co-ops, part-time)
- ✅ **Location filtering**: US-based or remote
- ✅ **Company blacklist**: Exclude specific companies
- ✅ **Relevance scoring**: Rank jobs by skill match and preferences

### Sponsorship Detection

- ✅ **Disqualifying phrases**: Detect "US citizenship required", "security clearance", "no sponsorship"
- ✅ **Positive signals**: Detect "OPT students welcome", "H1B sponsorship available", "international students"
- ✅ **Confidence scoring**: 0-1 confidence for each classification
- ✅ **Work authorization extraction**: Pull relevant text snippets from descriptions

### Email Intelligence

- ✅ **Classify emails** into 5 categories: applied, rejected, interview, assessment, follow_up
- ✅ **Extract company names** from sender addresses
- ✅ **Extract role titles** from subject lines and body text
- ✅ **Detect ATS platform**: Greenhouse, Lever, Workday, iCIMS, Ashby, etc.
- ✅ **Filter spam**: Ignore marketing newsletters and promotions

### Tracking & Visualization

- ✅ **SQLite database**: Track all jobs with status history
- ✅ **CSV export**: Export filtered jobs, rejected jobs, email classifications
- ✅ **FastAPI dashboard**: Web UI for pipeline visualization
- ✅ **Status management**: discovered → approved → applied → interview/rejected

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.11+ |
| **Data Processing** | pandas, SQLAlchemy |
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | Jinja2 Templates, Bootstrap 5 |
| **Database** | SQLite |
| **Testing** | pytest, pytest-cov |
| **Optional LLM** | Groq API (for advanced filtering) |

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

```bash
# Clone the repository
cd job-search-intelligence-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🎮 Demo Instructions

### Run Demo Mode

```bash
python main.py --demo
```

This will:
1. Load 15 sample jobs from `sample_data/jobs.csv`
2. Apply preference filters (role level, employment type, etc.)
3. Detect OPT/sponsorship signals in job descriptions
4. Load 8 sample recruiting emails from `sample_data/emails/`
5. Classify emails into categories (applied, rejected, interview, etc.)
6. Extract company names and roles from emails
7. Create SQLite database at `output/demo_tracker.db`
8. Export results to CSV files in `output/`

**Expected output:**
```
🔍 Step 1: Applying preference filters...
   ✓ 8 jobs passed filters
   ✗ 7 jobs filtered out

🌍 Step 2: Detecting OPT/sponsorship signals...
   ✓ 5 jobs are OPT/sponsorship-friendly

📧 Step 4: Classifying recruiting emails...
   Email classification results:
     • applied: 2
     • interview: 2
     • rejected: 2
     • assessment: 1
     • follow_up: 1

✅ DEMO COMPLETE
```

### Launch Dashboard

```bash
python main.py --dashboard
```

Then open http://localhost:8000 in your browser.

The dashboard shows:
- **Metrics overview**: Total jobs, approved, applied, interview pipeline
- **Jobs list**: All jobs with status badges and sponsorship signals
- **Email classifications**: Recruiting emails categorized by type

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_filters.py
```

**Test coverage:**
- ✅ Preference filters (entry-level vs senior roles)
- ✅ Sponsorship detection (citizenship, clearance, OPT signals)
- ✅ Email classification (applied, rejected, interview, assessment)
- ✅ Company/role extraction from email text
- ✅ Database operations (add, update, query)

---

## 📊 Screenshots

### Dashboard Overview
*Screenshot placeholder - metrics cards showing pipeline stats*

### Jobs List with Sponsorship Signals
*Screenshot placeholder - table with OPT-friendly badges*

### Email Classifications
*Screenshot placeholder - categorized recruiting emails*

---

## 🏗️ Architecture

See [docs/architecture.md](docs/architecture.md) for detailed system design.

**High-level data flow:**

```
Sample Jobs (CSV)
    ↓
Preference Filter → (role level, employment type, location)
    ↓
Sponsorship Detector → (citizenship, clearance, OPT signals)
    ↓
Relevance Scorer → (skill match, company preferences)
    ↓
SQLite Database (approved jobs)
    ↓
FastAPI Dashboard

Sample Emails (TXT)
    ↓
Email Classifier → (applied, rejected, interview, assessment)
    ↓
Email Extractor → (company, role, ATS platform)
    ↓
Status Updater → (update database from email signals)
    ↓
Dashboard / CSV Export
```

---

## ⚠️ Known Limitations

See [docs/limitations.md](docs/limitations.md) for full details.

**Key limitations:**
1. **Recruiting emails are inconsistent** - Workday/Handshake emails often omit role names
2. **Public version uses synthetic data only** - No real applications or credentials
3. **Demo version does not submit applications** - Focus is on filtering and tracking
4. **Sponsorship detection is keyword-based** - No semantic analysis (yet)
5. **Dashboard is for demo visibility** - Not production-ready for concurrent users

---

## 🔐 Privacy & Safety

This public version is designed to be **portfolio-safe**:

- ❌ No real Gmail credentials
- ❌ No real resumes or personal data
- ❌ No real application data or screenshots
- ❌ No aggressive scraping or automation
- ❌ No CAPTCHA bypass or account creation
- ✅ Synthetic sample data only
- ✅ Focus on filtering and intelligence logic
- ✅ No submission automation
- ✅ Human review step maintained

---

## 🚀 Deployment (Render)

To deploy on Render:

```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn main:app --host 0.0.0.0 --port $PORT
```

See `render.yaml` for configuration.

---

## 🔮 Future Improvements

- [ ] **Semantic job matching**: Replace keyword matching with embedding-based similarity (sentence-transformers)
- [ ] **LLM-powered resume tailoring**: Generate job-specific resumes
- [ ] **Email threading**: Link follow-up emails to original applications
- [ ] **Interview scheduler integration**: Auto-book calendar slots from interview emails
- [ ] **Analytics dashboard**: Success rate by company, ATS type, time of day
- [ ] **Mobile-responsive design**: PWA with offline support
- [ ] **Multi-language support**: i18n for international job boards

---

## 🎓 What I Learned

Building this project taught me:

1. **NLP without ML**: Pattern matching and regex can solve 80% of text classification problems
2. **Data quality > quantity**: Good sample data beats large messy datasets
3. **User-centric design**: Focused on actual pain points (sponsorship, email chaos) rather than over-automation
4. **Portfolio presentation**: Framing matters—this is a "job search intelligence tool", not a "mass auto-apply bot"
5. **Privacy by design**: Building public versions requires careful data sanitization from day one

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🤝 Contributing

This is a portfolio/demo project, but suggestions are welcome! Please open an issue to discuss proposed changes.

---

## 👤 Author

**Easha Meher Koppisetty**
- Portfolio: [mehereasha2601.github.io](https://mehereasha2601.github.io/)
- GitHub: [@mehereasha2601](https://github.com/mehereasha2601)
- LinkedIn: [easha-meher](https://www.linkedin.com/in/easha-meher)

---

## 🙏 Acknowledgments

- Built during my MS in Artificial Intelligence at Northeastern University
- Inspired by challenges faced during OPT job search (May 2026 graduation)
- Sample data structure based on real ATS platforms (Greenhouse, Lever, Workday)

---

**Note**: This is a portfolio demonstration project. For production use, consider proper authentication, rate limiting, and compliance with platform Terms of Service.
