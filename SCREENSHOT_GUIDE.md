# Screenshot Guide

Quick guide to capture professional screenshots for your portfolio.

---

## 📸 What You Need

- Running dashboard (python main.py --dashboard)
- Web browser (Chrome/Firefox recommended)
- Screenshot tool (built-in or Snagit/Monosnap)

---

## 🎯 Screenshots to Take

### 1. Dashboard Overview (dashboard.png)

**URL:** http://localhost:8000

**What to capture:**
- Full browser window (not just content)
- Metrics cards showing:
  - Total Jobs
  - Approved
  - Applied
  - Interview
- Pipeline status table
- Quick links section

**Tips:**
- Wait for demo to complete first (so there's data)
- Use browser zoom to fit everything nicely
- Hide browser bookmarks bar for clean look

**Ideal dimensions:** 1200px width

---

### 2. Jobs List (jobs.png)

**URL:** http://localhost:8000/jobs

**What to capture:**
- Filter buttons at top
- Job cards showing:
  - Company name
  - Role title
  - Location
  - Status badge (approved, applied, etc.)
  - Sponsorship badge (OPT Friendly, No Sponsorship, Unknown)
- At least 5-6 job cards visible

**Tips:**
- Click "Approved" filter to show interesting jobs
- Scroll to show variety of sponsorship statuses
- Make sure badges are visible

**Ideal dimensions:** 1200px width

---

### 3. Email Classifications (emails.png)

**URL:** http://localhost:8000/emails

**What to capture:**
- Email cards showing:
  - Subject line
  - Sender
  - Category badge (Applied, Rejected, Interview, etc.)
  - Extracted company and role
  - Confidence score
- At least 4-5 emails visible

**Tips:**
- Shows variety of email types (applied, rejected, interview)
- Make sure confidence percentages are visible
- Highlight the classification accuracy

**Ideal dimensions:** 1200px width

---

## 🛠️ How to Take Screenshots

### Method 1: Built-in Tools

**macOS:**
```bash
# Full screen
Cmd + Shift + 3

# Select area
Cmd + Shift + 4

# Window capture
Cmd + Shift + 4, then Space
```

**Windows:**
```bash
# Snipping Tool
Win + Shift + S

# Full screen
PrtScn
```

**Linux:**
```bash
# Most distros
PrtScn or Shift + PrtScn
```

### Method 2: Browser DevTools

1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl/Cmd + Shift + M)
3. Set to "Responsive" 1200px width
4. Click "..." → Capture screenshot

### Method 3: Browser Extensions

- **Awesome Screenshot** (Chrome/Firefox)
- **FireShot** (Chrome/Firefox)
- **Full Page Screen Capture** (Chrome)

---

## ✨ Screenshot Optimization

### Resize
```bash
# Using ImageMagick (install: brew install imagemagick)
convert dashboard.png -resize 1200x dashboard_optimized.png
```

### Compress
```bash
# Using ImageOptim (macOS)
# Or online: https://tinypng.com
```

### Format
- **PNG** for screenshots (lossless)
- Keep under 500KB per image
- Max width: 1200px

---

## 📁 Where to Save

Save to project directory:
```
docs/screenshots/
├── dashboard.png
├── jobs.png
└── emails.png
```

Then commit:
```bash
git add docs/screenshots/
git commit -m "Add dashboard screenshots"
git push
```

---

## 🎨 Pro Tips

1. **Consistent Browser Size**
   - Use same browser width for all screenshots
   - Recommend: 1200px window width

2. **Clean Browser**
   - Hide bookmarks bar
   - Close unnecessary tabs
   - Use "Guest" or clean profile

3. **Highlight Key Features**
   - Use arrows/annotations (optional)
   - Circle important UI elements
   - Add captions if needed

4. **Timing**
   - Run demo first to populate data
   - Wait for page to fully load
   - Hover effects should be visible but not distracting

5. **Accessibility**
   - Ensure text is readable
   - Good contrast
   - Don't rely on color alone for meaning

---

## 🖼️ Example Screenshot Workflow

```bash
# Step 1: Run demo to populate data
python main.py --demo

# Step 2: Start dashboard
python main.py --dashboard

# Step 3: Open browser
open http://localhost:8000

# Step 4: Take screenshots
# - Dashboard (main page)
# - Jobs list (/jobs)
# - Emails list (/emails)

# Step 5: Save to docs/screenshots/

# Step 6: Optimize images
# (resize to 1200px, compress to <500KB)

# Step 7: Add to git
git add docs/screenshots/
git commit -m "Add dashboard screenshots"
git push
```

---

## ✅ Checklist

- [ ] Dashboard shows metrics cards
- [ ] Jobs list shows sponsorship badges
- [ ] Emails list shows classifications
- [ ] All images are 1200px width max
- [ ] All images are under 500KB
- [ ] Saved to `docs/screenshots/`
- [ ] Committed to git
- [ ] Referenced in README.md

---

## 🚀 Using Screenshots

### In README
```markdown
## 📊 Screenshots

### Dashboard Overview
![Dashboard](docs/screenshots/dashboard.png)
```

### In Portfolio
```html
<img src="screenshots/dashboard.png" alt="Dashboard Overview">
```

### On LinkedIn
- Upload to post as image
- Add caption: "Dashboard from my Job Search Intelligence Pipeline"

---

Need help? Check DEPLOYMENT_GUIDE.md for more details!
