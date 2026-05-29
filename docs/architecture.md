# Architecture Overview

## System Design

The Job Search Intelligence Pipeline is designed as a modular, privacy-first job search organization tool. The architecture separates concerns into distinct layers:

---

## Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Sample Data Layer                       │
│  • jobs.csv (15 synthetic job postings)                     │
│  • emails/*.txt (8 synthetic recruiting emails)             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Intelligence Layer                        │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ Preference Filter│  │Sponsorship Detector│              │
│  │ • Role level     │  │ • Citizenship req  │              │
│  │ • Employment type│  │ • Security clearance│             │
│  │ • Location       │  │ • OPT signals      │              │
│  │ • Blacklist      │  │ • Visa sponsorship │              │
│  └──────────────────┘  └──────────────────┘               │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ Email Classifier │  │  Email Extractor  │              │
│  │ • Applied        │  │ • Company name    │              │
│  │ • Rejected       │  │ • Role title      │              │
│  │ • Interview      │  │ • ATS platform    │              │
│  │ • Assessment     │  │ • Application ID  │              │
│  └──────────────────┘  └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      Tracking Layer                          │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ SQLite Database  │  │  Status Updater   │              │
│  │ • Applications   │  │ • Email → Status  │              │
│  │ • Status history │  │ • Match logic     │              │
│  │ • Metadata       │  │ • Deduplication   │              │
│  └──────────────────┘  └──────────────────┘               │
│                                                              │
│  ┌──────────────────────────────────────┐                  │
│  │          CSV Exporter                 │                  │
│  │ • approved_jobs.csv                   │                  │
│  │ • rejected_jobs.csv                   │                  │
│  │ • email_classifications.csv           │                  │
│  └──────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ FastAPI Backend  │  │  Jinja2 Templates │              │
│  │ • REST endpoints │  │ • Dashboard       │              │
│  │ • Stats API      │  │ • Jobs list       │              │
│  │ • Health check   │  │ • Email list      │              │
│  └──────────────────┘  └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Job Filtering Pipeline

```
Sample Job (CSV row)
  ↓
[Parse] → Job Dict {company, title, description, location}
  ↓
[Preference Filter]
  • Check role level (new grad/entry vs senior/intern)
  • Check employment type (full-time vs part-time/contract)
  • Check location (US-based or remote)
  • Check company blacklist
  ↓
[PASS] → Continue | [FAIL] → Mark as "filtered_out" + reason
  ↓
[Sponsorship Detector]
  • Scan for disqualifying phrases (citizenship, clearance)
  • Scan for positive signals (OPT, sponsorship available)
  • Assign status: disqualified, positive, neutral, soft_negative
  ↓
[Relevance Scorer]
  • Calculate skill match score (0-1)
  • Boost score for preferred companies/locations
  ↓
[Add to Database]
  • status: "approved" (if passed filters)
  • sponsorship_status: positive/neutral/disqualified
  • relevance_score: 0.0-1.0
```

### 2. Email Classification Pipeline

```
Sample Email (TXT file)
  ↓
[Parse] → Email Dict {sender, subject, body}
  ↓
[Email Classifier]
  • Match body keywords against classification rules
  • Match subject keywords (higher weight)
  • Calculate confidence score (0-1)
  • Assign category: applied, rejected, interview, assessment, follow_up
  ↓
[Email Extractor]
  • Extract company name from sender domain
  • Extract role title from subject/body patterns
  • Detect ATS platform (Greenhouse, Lever, Workday, etc.)
  • Extract application ID (if present)
  ↓
[Status Updater]
  • Find matching job in database (by company + role)
  • Map email category to application status
  • Update database status + date fields
  ↓
[Export to CSV]
  • Save classification results
  • Include confidence scores and extracted entities
```

---

## Module Descriptions

### `src/filters/`

#### `preference_filter.py`
**Purpose**: Filter jobs based on user preferences

**Key classes**:
- `PreferenceFilter`: Main filtering engine
  - Configurable target levels, skip keywords, role types
  - Returns (passed_jobs, rejected_jobs) tuple

**Configuration**:
```python
TARGET_LEVELS = ["new grad", "entry level", "junior", "l3", "l4"]
SKIP_KEYWORDS = ["senior", "staff", "principal", "intern", "part-time"]
```

**Logic**:
1. Check title for skip keywords → reject if found
2. Check title/description for target levels → reject if not found
3. Check location for US indicators → reject if non-US
4. Check company against blacklist → reject if blacklisted
5. If passes all filters → accept

---

#### `sponsorship_detector.py`
**Purpose**: Detect OPT/visa sponsorship signals in job descriptions

**Key classes**:
- `SponsorshipDetector`: Signal detection engine
  - 3 tiers: disqualifying, positive, soft_negative
  - Confidence scoring based on signal strength

**Signal Categories**:
```python
DISQUALIFYING_PHRASES = [
    "us citizen only",
    "security clearance required",
    "no sponsorship",
    # ... ~20 phrases
]

POSITIVE_SIGNALS = [
    "opt students welcome",
    "h1b sponsorship",
    "visa sponsorship available",
    # ... ~15 phrases
]
```

**Output**:
```python
{
    "status": "positive",  # or disqualified, neutral, soft_negative
    "confidence": 0.85,
    "signals": ["opt students welcome", "h1b sponsorship"],
    "recommendation": "Apply - OPT/sponsorship friendly",
    "sponsors_visa": True
}
```

---

#### `relevance_scorer.py`
**Purpose**: Score job relevance based on skills and preferences

**Scoring formula**:
```
score = (skill_match * 0.6) + (company_match * 0.2) + (location_match * 0.2)
```

**Example**:
- Job mentions 3/5 target skills → skill_match = 0.6
- Company in preferred list → company_match = 1.0
- Location matches preference → location_match = 1.0
- **Final score**: (0.6 × 0.6) + (1.0 × 0.2) + (1.0 × 0.2) = 0.76

---

### `src/email_intelligence/`

#### `classifier.py`
**Purpose**: Classify recruiting emails into categories

**Classification Rules**:
```python
{
    "applied": {
        "keywords": ["application received", "thank you for applying"],
        "subject_keywords": ["confirmation", "received"]
    },
    "rejected": {
        "keywords": ["unfortunately", "not moving forward"],
        "subject_keywords": ["application status"]
    },
    "interview": {
        "keywords": ["interview", "schedule a call", "phone screen"],
        "subject_keywords": ["interview", "next steps"]
    },
    # ... more categories
}
```

**Confidence Calculation**:
```python
confidence = (body_matches + 2 * subject_matches) / total_keywords
```
- Subject matches have 2x weight (higher signal)
- Capped at 1.0

---

#### `extractors.py`
**Purpose**: Extract structured entities from email text

**Extraction Patterns**:

**Company from sender**:
```
recruiter@google.com → "Google"
Jane Doe <jane@stripe.com> → "Stripe"
noreply@greenhouse.io → None (ATS platform)
```

**Role from subject**:
```
"Software Engineer - Application Received" → "Software Engineer"
"Your Backend Developer application" → "Backend Developer"
```

**Role from body**:
```
"for the Machine Learning Engineer position" → "Machine Learning Engineer"
"applied for Data Scientist at" → "Data Scientist"
```

---

### `src/tracker/`

#### `database.py`
**Purpose**: SQLite database management with SQLAlchemy ORM

**Schema**:
```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    url VARCHAR(2048),
    source VARCHAR(50),  -- demo, linkedin, handshake, etc.
    status VARCHAR(50) DEFAULT 'discovered',  -- discovered, approved, applied, interview, rejected, filtered_out
    relevance_score FLOAT,
    sponsorship_status VARCHAR(50),  -- positive, neutral, disqualified, soft_negative
    date_discovered DATETIME NOT NULL,
    date_applied DATETIME,
    date_updated DATETIME,
    notes TEXT,
    rejection_reason VARCHAR(255)
);
```

**Key Operations**:
- `add_job()`: Insert new job (with duplicate check)
- `update_status()`: Change application status
- `get_jobs_by_status()`: Query by status
- `get_stats()`: Aggregate counts by status

---

#### `status_updater.py`
**Purpose**: Update application status based on email classification

**Mapping Logic**:
```python
email_category → application_status
{
    "applied" → "applied",
    "rejected" → "rejected",
    "interview" → "interview",
    "assessment" → "assessment",
    "follow_up" → "discovered"  # no status change
}
```

**Matching Strategy**:
1. If email has company + role → exact match
2. If email has only company → match any job from that company
3. If no match found → log warning

---

### `src/dashboard/`

#### `app.py` + `routes.py`
**Purpose**: FastAPI web application for visualization

**Endpoints**:
- `GET /` → Dashboard with metrics cards
- `GET /jobs` → Jobs list (with status filter)
- `GET /emails` → Email classifications list
- `GET /api/stats` → JSON stats API
- `GET /health` → Health check

**Templates**:
- `index.html`: Dashboard with metrics cards (Bootstrap 5)
- `jobs.html`: Jobs table with status badges and filters
- `emails.html`: Email classifications with category badges

---

## Key Design Decisions

### 1. **CSV + SQLite (not live scraping)**
**Why**: Demo focuses on intelligence layer, not scraping infrastructure

**Trade-offs**:
- ✅ Simple, reproducible demo
- ✅ No platform ToS violations
- ❌ Not real-time

---

### 2. **Keyword-based detection (not ML)**
**Why**: 80% accuracy with 0 training data

**Trade-offs**:
- ✅ Fast, deterministic, explainable
- ✅ No model training/deployment
- ❌ Misses subtle semantic signals

---

### 3. **SQLite (not PostgreSQL)**
**Why**: Demo/portfolio project with single user

**Trade-offs**:
- ✅ Zero configuration
- ✅ File-based (easy to share)
- ❌ No concurrent writes

---

### 4. **Jinja2 + Bootstrap (not React)**
**Why**: Focus on backend logic, not frontend polish

**Trade-offs**:
- ✅ Fast development
- ✅ Server-side rendering
- ❌ Less interactive

---

## Performance Characteristics

**Demo Mode**:
- 15 jobs filtered in <100ms
- 8 emails classified in <50ms
- Database write: ~10ms per job
- Total runtime: ~500ms

**Dashboard**:
- Page load: <200ms (no auth, no network)
- Database queries: <50ms (SQLite file)

**Scalability**:
- Current: <100 jobs, single user
- Production needs: PostgreSQL, Redis cache, auth

---

## Security Considerations

**Current (Demo)**:
- No authentication
- No rate limiting
- Local file database
- Synthetic data only

**For Production**:
- Add OAuth/JWT auth
- Rate limit API endpoints
- Use PostgreSQL with connection pooling
- Encrypt sensitive data at rest
- Add CSRF protection

---

## Testing Strategy

**Unit Tests** (pytest):
- Each filter function tested with 5-10 cases
- Email classification with known examples
- Database operations with temp DB

**Integration Tests**:
- End-to-end demo flow
- Dashboard routes with fixtures

**No Load Tests**:
- Demo is single-user, no need for load testing

---

## Future Architecture Enhancements

1. **Semantic Search**: Replace keyword matching with embeddings (sentence-transformers)
2. **Event Sourcing**: Track full status history (not just current status)
3. **Async Email Processing**: Background workers for real-time classification
4. **Caching Layer**: Redis for frequently accessed stats
5. **Microservices**: Separate filter service, email service, dashboard service
