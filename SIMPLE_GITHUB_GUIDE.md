# Simple GitHub Guide - Step by Step

## What You're Doing (Simple Explanation)

Think of it like this:
- **Your computer** = Your local workspace (where you work)
- **GitHub** = A cloud storage for code (like Dropbox, but for code)
- **Git** = The tool that syncs between your computer and GitHub

## The Process in 3 Steps

### 1️⃣ Prepare Your Files (On Your Computer)
### 2️⃣ Create a GitHub Account & Repository (On GitHub Website)
### 3️⃣ Connect Them Together (Using Commands)

---

## Step 1: Prepare Your Files (On Your Computer)

Open a terminal and run these commands one by one:

```bash
# Go to your project folder
cd /home/yertay/.cursor-tutor/spectral_signatures_collection

# Initialize Git (creates a .git folder to track changes)
git init

# Add all your files to Git
git add .

# Save a snapshot (like taking a photo of your project)
git commit -m "Initial commit: Spectral signatures collection"
```

**What happened?** Git is now tracking all your files on your computer.

---

## Step 2: Create GitHub Repository (On GitHub Website)

### A. Create GitHub Account (if you don't have one)
1. Go to: https://github.com
2. Click "Sign up"
3. Fill in: Username, Email, Password
4. Verify your email

### B. Create New Repository
1. After logging in, click the **"+"** button (top right)
2. Click **"New repository"**
3. Fill in:
   - **Repository name**: `spectral-signatures-collection` (or any name)
   - **Description**: "Collection of relative spectral signatures for remote sensing"
   - **Visibility**: Choose Public (anyone can see) or Private (only you)
   - **DO NOT** check "Add a README file" (you already have one!)
4. Click **"Create repository"**

**What happened?** You created an empty "box" on GitHub to store your files.

---

## Step 3: Connect Your Computer to GitHub

GitHub will show you a page with instructions. Look for the section that says:

**"...or push an existing repository from the command line"**

Copy and run these commands (replace `YOUR_USERNAME` with your GitHub username):

```bash
# Tell Git where your GitHub repository is
git remote add origin https://github.com/YOUR_USERNAME/spectral-signatures-collection.git

# Make sure you're on the 'main' branch
git branch -M main

# Upload your files to GitHub
git push -u origin main
```

**What will happen?**
- Git will ask for your GitHub username
- Then it will ask for your password (or a Personal Access Token - see below)

---

## Important: Authentication

GitHub no longer accepts passwords. You need a **Personal Access Token**:

### How to Create a Token:
1. Go to GitHub → Click your profile picture (top right)
2. Click **"Settings"**
3. Scroll down → Click **"Developer settings"** (left sidebar)
4. Click **"Personal access tokens"** → **"Tokens (classic)"**
5. Click **"Generate new token"** → **"Generate new token (classic)"**
6. Give it a name: "My Computer"
7. Check the box: **"repo"** (this gives access to repositories)
8. Scroll down → Click **"Generate token"**
9. **COPY THE TOKEN** (you won't see it again!)

When Git asks for your password, **paste the token instead**.

---

## Visual Summary

```
Your Computer                    GitHub Website
─────────────────               ────────────────
spectral_signatures/            [Empty Repository]
  ├── README.md                  
  ├── tools/                     
  └── ...                       

     Step 1: git init
     Step 2: git add .
     Step 3: git commit
     
     Step 4: Create repo on GitHub
     
     Step 5: git remote add origin
     Step 6: git push
     
     ────────────────────────────────>
     
spectral_signatures/            spectral-signatures/
  ├── README.md        ──────>   ├── README.md
  ├── tools/           ──────>   ├── tools/
  └── ...              ──────>   └── ...
```

---

## After You Push

✅ Your files are now on GitHub!
✅ You can see them at: `https://github.com/YOUR_USERNAME/spectral-signatures-collection`
✅ They're backed up online
✅ You can share the link with others

---

## Common Questions

**Q: What if I make changes later?**
A: Run these commands:
```bash
git add .
git commit -m "Description of changes"
git push
```

**Q: Can I delete files from GitHub?**
A: Yes! Delete locally, then:
```bash
git add .
git commit -m "Removed files"
git push
```

**Q: What if I make a mistake?**
A: Don't worry! Git tracks everything. You can always go back.

---

## Need Help?

- Check `GITHUB_SETUP_GUIDE.md` for more details
- GitHub Help: https://docs.github.com/en/get-started
- Git Tutorial: https://learngitbranching.js.org

