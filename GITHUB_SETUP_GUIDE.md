# GitHub Setup Guide for Beginners

## What is Git and GitHub?

**Git** is a version control system - it tracks changes to your files over time. Think of it like a "save history" for your project.

**GitHub** is a website where you can store your Git repositories online, share them with others, and collaborate.

## Step-by-Step Guide

### Step 1: Install Git (if not already installed)

Check if Git is installed:
```bash
git --version
```

If you see a version number, Git is installed! If not, install it:
- **Linux**: `sudo apt install git`
- **Mac**: `brew install git` or download from git-scm.com
- **Windows**: Download from git-scm.com

### Step 2: Configure Git (first time only)

Tell Git who you are:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Initialize Your Repository

Navigate to your project folder and initialize Git:

```bash
cd spectral_signatures_collection
git init
```

This creates a hidden `.git` folder that tracks your files.

### Step 4: Add Files to Git

Tell Git to track all your files:

```bash
git add .
```

The `.` means "all files in this directory".

### Step 5: Make Your First Commit

Save a snapshot of your files:

```bash
git commit -m "Initial commit: Spectral signatures collection"
```

The `-m` flag lets you add a message describing what you're saving.

### Step 6: Create a GitHub Account

1. Go to https://github.com
2. Click "Sign up"
3. Choose a username, enter email, create password
4. Verify your email

### Step 7: Create a New Repository on GitHub

1. Log into GitHub
2. Click the "+" icon in the top right
3. Click "New repository"
4. Name it: `spectral-signatures-collection` (or any name you like)
5. **DO NOT** check "Initialize with README" (you already have files)
6. Click "Create repository"

### Step 8: Connect Your Local Repository to GitHub

GitHub will show you commands. Use these:

```bash
# Add GitHub as a remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/spectral-signatures-collection.git

# Rename your main branch (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

You'll be asked for your GitHub username and password (or use a Personal Access Token).

### Step 9: Verify

Go to your GitHub repository page - you should see all your files!

## Common Commands You'll Use

```bash
# Check status of your files
git status

# See what changed
git diff

# Add specific file
git add filename.py

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes from GitHub
git pull
```

## Troubleshooting

### "Permission denied" error
- You might need to use a Personal Access Token instead of password
- Go to GitHub → Settings → Developer settings → Personal access tokens
- Generate a new token with "repo" permissions
- Use the token as your password

### "Repository not found" error
- Check that you spelled the repository name correctly
- Make sure the repository exists on GitHub
- Verify your username is correct

## What Happens Next?

Once your code is on GitHub:
- ✅ It's backed up online
- ✅ You can access it from anywhere
- ✅ Others can see and use it (if public)
- ✅ You can track changes over time
- ✅ You can collaborate with others

## Need Help?

- Git documentation: https://git-scm.com/doc
- GitHub guides: https://guides.github.com
- Git tutorial: https://learngitbranching.js.org

