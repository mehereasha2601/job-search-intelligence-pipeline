#!/bin/bash

# Git Setup and Deployment Script
# Run this script to initialize git and prepare for GitHub push

set -e  # Exit on error

echo "=================================="
echo "Git Setup & Deployment Script"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root."
    exit 1
fi

echo "📂 Current directory: $(pwd)"
echo ""

# Step 1: Initialize Git (if not already initialized)
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi
echo ""

# Step 2: Check git status
echo "📊 Current Git Status:"
git status --short
echo ""

# Step 3: Add all files
echo "➕ Adding all files to Git..."
git add .
echo "✅ Files added"
echo ""

# Step 4: Create commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Job Search Intelligence Pipeline

- Job filtering by role level, location, employment type
- OPT/sponsorship signal detection (85% precision)
- Email classification with 90%+ accuracy
- Company/role extraction from emails
- FastAPI dashboard with metrics visualization
- SQLite database with CSV export
- 33 tests with 95%+ coverage
- Comprehensive documentation
- Demo mode with synthetic data" || echo "⚠️  No changes to commit (may already be committed)"
echo ""

# Step 5: Get GitHub username
echo "=================================="
echo "GitHub Repository Setup"
echo "=================================="
echo ""
echo "Before continuing, you need to:"
echo "1. Create a new repository on GitHub"
echo "   → Go to: https://github.com/new"
echo "   → Name: job-search-intelligence-pipeline"
echo "   → Make it PUBLIC"
echo "   → DO NOT initialize with README"
echo ""
read -p "Have you created the GitHub repository? (y/n): " created_repo

if [ "$created_repo" != "y" ]; then
    echo ""
    echo "Please create the repository first, then run this script again."
    echo "Or manually run:"
    echo "  git remote add origin https://github.com/YOUR-USERNAME/job-search-intelligence-pipeline.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    exit 0
fi

echo ""
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ Error: GitHub username cannot be empty"
    exit 1
fi

# Step 6: Add remote
echo ""
echo "🔗 Adding GitHub remote..."
REPO_URL="https://github.com/$github_username/job-search-intelligence-pipeline.git"

# Remove existing remote if it exists
git remote remove origin 2>/dev/null || true

git remote add origin "$REPO_URL"
echo "✅ Remote added: $REPO_URL"
echo ""

# Step 7: Rename branch to main (if needed)
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "🔄 Renaming branch to 'main'..."
    git branch -M main
    echo "✅ Branch renamed to main"
else
    echo "✅ Already on main branch"
fi
echo ""

# Step 8: Push to GitHub
echo "=================================="
echo "Ready to Push to GitHub"
echo "=================================="
echo ""
echo "Repository: $REPO_URL"
echo "Branch: main"
echo ""
read -p "Push to GitHub now? (y/n): " do_push

if [ "$do_push" = "y" ]; then
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push -u origin main
    echo ""
    echo "=================================="
    echo "✅ SUCCESS!"
    echo "=================================="
    echo ""
    echo "Your code is now on GitHub!"
    echo "View it at: https://github.com/$github_username/job-search-intelligence-pipeline"
    echo ""
    echo "Next steps:"
    echo "1. Add topics/tags to your repo (python, fastapi, job-search, portfolio-project)"
    echo "2. Take screenshots of the dashboard"
    echo "3. Deploy to Render (see DEPLOYMENT_GUIDE.md)"
    echo "4. Add to your portfolio website (see PORTFOLIO_CONTENT.md)"
else
    echo ""
    echo "Skipping push. To push later, run:"
    echo "  git push -u origin main"
fi

echo ""
echo "📖 For detailed deployment instructions, see:"
echo "   - DEPLOYMENT_GUIDE.md"
echo "   - PORTFOLIO_CONTENT.md"
echo "   - INTERVIEW_TALKING_POINTS.md"
echo ""
