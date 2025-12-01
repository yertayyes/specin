#!/bin/bash
# Helper script to set up Git repository
# Run this script to initialize your Git repository

echo "=========================================="
echo "Git Repository Setup Helper"
echo "=========================================="
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo "Please install Git first:"
    echo "  Linux: sudo apt install git"
    echo "  Mac: brew install git"
    echo "  Windows: Download from https://git-scm.com"
    exit 1
fi

echo "✅ Git is installed: $(git --version)"
echo ""

# Check if Git is configured
if [ -z "$(git config --global user.name)" ]; then
    echo "⚠️  Git is not configured yet."
    echo ""
    read -p "Enter your name (for Git commits): " git_name
    read -p "Enter your email (for Git commits): " git_email
    
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    echo "✅ Git configured!"
else
    echo "✅ Git is already configured:"
    echo "   Name: $(git config --global user.name)"
    echo "   Email: $(git config --global user.email)"
fi

echo ""
echo "=========================================="
echo "Step 1: Initializing Git repository..."
echo "=========================================="

# Check if already a git repository
if [ -d .git ]; then
    echo "⚠️  This directory is already a Git repository!"
    read -p "Continue anyway? (y/n): " continue_choice
    if [ "$continue_choice" != "y" ]; then
        exit 0
    fi
else
    git init
    echo "✅ Git repository initialized!"
fi

echo ""
echo "=========================================="
echo "Step 2: Adding files..."
echo "=========================================="

git add .
echo "✅ Files added to Git!"

echo ""
echo "=========================================="
echo "Step 3: Creating initial commit..."
echo "=========================================="

git commit -m "Initial commit: Spectral signatures collection"
echo "✅ Initial commit created!"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to https://github.com and create an account (if you don't have one)"
echo "2. Create a new repository on GitHub"
echo "3. Run these commands (replace YOUR_USERNAME with your GitHub username):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/spectral-signatures-collection.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "For detailed instructions, see:"
echo "  - SIMPLE_GITHUB_GUIDE.md"
echo "  - GITHUB_SETUP_GUIDE.md"
echo ""

