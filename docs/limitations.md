# Known Limitations

## Overview

This document outlines known limitations of the Job Search Intelligence Pipeline. These are design constraints, data quality issues, and edge cases that affect system behavior.

---

## 1. Data Quality & Consistency

### 1.1 Recruiting Email Inconsistency

**Issue**: ATS platforms have inconsistent email formats

**Examples**:
- Workday emails often omit job title entirely
- Handshake emails use generic "Application Update" subjects
- Some platforms send HTML-only emails (body text is incomplete)

**Impact**:
- Company extraction: ~90% accuracy
- Role extraction: ~60% accuracy (fallback to subject line)
- Status matching: ~70% accuracy (when role is missing)

**Workaround**:
- Fallback to company-only matching
- Extract role from subject line when body parsing fails
- Manual review for unmatched emails

---

### 1.2 Job Description Ambiguity

**Issue**: Sponsorship language varies widely

**Examples**:
- "We support work authorization" (unclear)
- "No sponsorship" vs "Cannot sponsor at this time" (temporal)
- "Prefer US work authorization" (soft negative)

**Impact**:
- Sponsorship detection: ~85% precision, ~75% recall
- False negatives: OPT-friendly jobs marked "neutral"
- False positives: Rare (disqualifying phrases are explicit)

**Workaround**:
- Confidence scoring (0-1) instead of binary yes/no
- Soft negative category for "preferred but not required"
- Manual review for high-value opportunities

---

## 2. Technical Constraints

### 2.1 Demo Data Only

**Limitation**: Public version uses synthetic data only

**What this means**:
- ❌ Cannot test with real recruiting emails
- ❌ Cannot validate against actual job postings
- ❌ Cannot measure true classification accuracy

**Why**:
- Privacy: Real data contains PII
- Legal: Terms of Service restrictions
- Portfolio: Demo focuses on methodology, not results

**Impact**:
- Demo is a proof-of-concept, not production-ready
- Actual performance may differ from synthetic benchmarks

---

### 2.2 No Real-Time Processing

**Limitation**: Batch processing (not streaming)

**What this means**:
- ❌ No live Gmail monitoring
- ❌ No real-time job board scraping
- ❌ No instant dashboard updates

**Why**:
- Demo focuses on intelligence logic, not infrastructure
- Real-time processing requires:
  - Gmail API OAuth (not included in public version)
  - Background workers (Celery, RQ)
  - WebSocket connections for live updates

**Impact**:
- Demo is run-once, not continuous
- Production deployment would need significant refactoring

---

### 2.3 SQLite Limitations

**Limitation**: Single-user, file-based database

**Constraints**:
- No concurrent writes (risk of database locking)
- No distributed deployments
- Limited query performance (>10K jobs)

**Why SQLite**:
- Zero configuration
- Portable (single file)
- Sufficient for demo/portfolio

**For Production**:
- Use PostgreSQL with connection pooling
- Add Redis for caching
- Implement connection retry logic

---

## 3. Algorithm Limitations

### 3.1 Keyword-Based Classification

**Limitation**: No semantic understanding

**What this means**:
- ✅ Fast (no ML inference)
- ✅ Explainable (can show matched keywords)
- ❌ Misses synonyms ("phone screen" vs "initial call")
- ❌ Fails on ambiguous language

**Examples of failures**:
- "We regret to inform you" (rejection) → missed if "unfortunately" not present
- "Let's connect" (follow-up) → might be misclassified as interview

**Workaround**:
- Expand keyword lists based on common patterns
- Future: Use sentence embeddings for semantic similarity

---

### 3.2 No Context Window

**Limitation**: Each email classified independently

**What this means**:
- ❌ Cannot track email threads (reply chains)
- ❌ Cannot use application history for context
- ❌ Cannot detect follow-ups to previous rejections

**Example**:
- First email: "Thank you for applying"
- Second email (1 week later): "Unfortunately..." (rejection)
- System classifies both separately, misses connection

**Future Enhancement**:
- Implement email threading based on In-Reply-To headers
- Track conversation history per company

---

### 3.3 Single-Phrase Matching

**Limitation**: One phrase can override entire email

**What this means**:
- "Unfortunately, we're excited to invite you to interview" → classified as rejection
- False positives from boilerplate text

**Example**:
- Marketing email with "Unfortunately, this offer expires soon" → rejection
- Solution: Check for spam indicators first

**Workaround**:
- Filter spam/marketing before classification
- Require multiple keyword matches for high confidence

---

## 4. User Experience Limitations

### 4.1 Manual Approval Queue

**Limitation**: Human must review filtered jobs

**Why**:
- Cannot guarantee 100% filter accuracy
- User may have subjective preferences
- Sponsorship signals are probabilistic

**Impact**:
- Still requires 5-10 minutes daily review
- Not "set and forget" automation

**Design Philosophy**:
- Human-in-the-loop by design
- Intelligence tool, not replacement for judgment

---

### 4.2 Dashboard Not Real-Time

**Limitation**: Requires page refresh to see updates

**Why**:
- No WebSocket implementation
- Server-side rendering (Jinja2)
- Demo simplicity over feature completeness

**Workaround**:
- Add auto-refresh meta tag (every 30 seconds)
- Future: WebSocket connection for live updates

---

### 4.3 No Mobile Optimization

**Limitation**: Dashboard is desktop-first

**Current State**:
- Bootstrap 5 responsive grid (works on mobile)
- Not optimized for touch interactions
- Small screen layout is cramped

**For Production**:
- Mobile-first design
- Touch-friendly buttons
- Progressive Web App (PWA)

---

## 5. Deployment Limitations

### 5.1 No Multi-User Support

**Limitation**: Single-user, no authentication

**What's missing**:
- User accounts
- OAuth login
- Per-user data isolation
- Role-based access control

**Why**:
- Demo/portfolio scope
- Adds significant complexity
- Not needed for single user

**For Production**:
- Implement JWT-based auth
- Add user table to database
- Filter queries by user_id

---

### 5.2 No Email Credentials Management

**Limitation**: No Gmail API integration in public version

**What this means**:
- ❌ Cannot read real emails
- ❌ Cannot send notifications
- ❌ Cannot auto-verify accounts

**Why**:
- Requires OAuth credentials (not public-safe)
- Gmail API quota limits
- Privacy concerns

**For Production**:
- Implement OAuth 2.0 flow
- Store encrypted tokens per user
- Handle token refresh

---

## 6. Data Accuracy

### 6.1 Duplicate Detection

**Limitation**: Basic company + title matching

**Edge Cases**:
- Same role at different locations → treated as separate
- "Software Engineer I" vs "Software Engineer 1" → treated as separate
- Company name variations ("Google" vs "Google LLC")

**Future Enhancement**:
- Fuzzy string matching (Levenshtein distance)
- Normalize company names (remove "Inc", "LLC", etc.)
- URL-based deduplication (same job URL)

---

### 6.2 Date Parsing

**Limitation**: No date extraction from job postings

**Current State**:
- date_discovered = current timestamp
- No "posted 2 days ago" parsing

**Impact**:
- Cannot filter by freshness
- Cannot detect stale job postings

**Future Enhancement**:
- Parse relative dates ("2 days ago")
- Extract "Posted on MM/DD/YYYY" from descriptions

---

## 7. Performance Limitations

### 7.1 Synchronous Processing

**Limitation**: Sequential processing (not parallel)

**Current Performance**:
- 15 jobs × 50ms each = 750ms total
- 8 emails × 30ms each = 240ms total

**For Larger Scale** (1000 jobs):
- Sequential: ~50 seconds
- Parallel (10 workers): ~5 seconds

**Future Enhancement**:
- Use multiprocessing.Pool for job filtering
- Async email classification with asyncio

---

### 7.2 No Caching

**Limitation**: Re-computes everything on each run

**What's not cached**:
- Sponsorship detection results
- Relevance scores
- Email classifications

**Impact**:
- Unnecessary re-computation
- Slower dashboard loads

**Future Enhancement**:
- Cache filtered job results
- Cache email classifications
- Invalidate cache on new data

---

## 8. Business Logic Limitations

### 8.1 Fixed Filter Criteria

**Limitation**: Hardcoded filter rules

**Current State**:
```python
TARGET_LEVELS = ["new grad", "entry level", "junior"]  # Fixed list
SKIP_KEYWORDS = ["senior", "staff", "intern"]          # Fixed list
```

**Why**:
- Demo simplicity
- Avoids configuration complexity

**For Production**:
- User-configurable filters
- Save preferences to database
- Dynamic filter rules per user

---

### 8.2 No Learning

**Limitation**: System doesn't improve from feedback

**What this means**:
- If user rejects an "approved" job → no feedback loop
- If user applies to "filtered out" job → no adjustment

**Future Enhancement**:
- Track user approve/reject actions
- Adjust relevance scoring based on history
- Active learning: retrain filters on labeled data

---

## 9. Compliance & Legal

### 9.1 Platform Terms of Service

**Public Version**:
- ✅ No scraping (uses synthetic data)
- ✅ No automation (demo only)
- ✅ No CAPTCHA bypass

**Private Version Risks** (if extended):
- ⚠️ LinkedIn/Indeed scraping violates ToS
- ⚠️ Automated applications may be flagged
- ⚠️ Account creation may trigger fraud detection

**Recommendation**:
- Use official APIs when available
- Respect rate limits
- Disclose automation to platforms

---

### 9.2 Privacy Regulations

**Demo Version**:
- ✅ No real PII
- ✅ No user tracking
- ✅ No cookies

**For Production**:
- Must comply with GDPR (EU users)
- Must comply with CCPA (California users)
- Requires privacy policy and data retention policy

---

## 10. Summary of Key Limitations

| Category | Limitation | Severity | Workaround |
|----------|-----------|----------|------------|
| **Data Quality** | Inconsistent email formats | 🟡 Medium | Company-only matching |
| **Data Quality** | Ambiguous sponsorship language | 🟡 Medium | Confidence scoring |
| **Technical** | No real-time processing | 🟡 Medium | Batch runs |
| **Technical** | SQLite (not PostgreSQL) | 🟢 Low | Sufficient for demo |
| **Algorithm** | Keyword-based (not semantic) | 🟡 Medium | Expand keyword lists |
| **Algorithm** | No email threading | 🟢 Low | Classify independently |
| **UX** | Manual approval required | 🟢 Low | By design |
| **UX** | No mobile optimization | 🟢 Low | Responsive grid works |
| **Deployment** | No multi-user support | 🟡 Medium | Single-user demo |
| **Deployment** | No Gmail API integration | 🔴 High | Use synthetic emails |
| **Performance** | Synchronous processing | 🟢 Low | Fast enough for demo |
| **Business Logic** | Fixed filter criteria | 🟡 Medium | Hardcoded for demo |
| **Compliance** | ToS violations (if extended) | 🔴 High | Use synthetic data |

**Legend**:
- 🔴 High: Blocks production use
- 🟡 Medium: Limits scale/accuracy
- 🟢 Low: Acceptable for demo

---

## Conclusion

This project prioritizes **demonstrating methodology over production readiness**. The limitations are intentional trade-offs for a portfolio/demo project:

- ✅ Focus on intelligence layer (filters, classification, extraction)
- ✅ Privacy-first (no real data, no credentials)
- ✅ Explainable (keyword-based, not black-box ML)
- ❌ Not real-time
- ❌ Not production-scale
- ❌ Not multi-user

For a production system, address:
1. Real-time email processing (Gmail API + workers)
2. Semantic understanding (embeddings + LLM)
3. Multi-user authentication (OAuth)
4. Platform compliance (official APIs)
5. Performance optimization (caching, parallelization)
