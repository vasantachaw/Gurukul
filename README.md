📘 Git Setup & Deployment Guide for Gurukul Project

This document explains how to set up Git, create a .gitignore file, track your project, and push it to GitHub.

🚀 1. Initialize Git in Your Project

Open your project folder in the terminal:

git init


This creates a new Git repository.

📄 2. Create .gitignore File
Create file (PowerShell):
New-Item -Path .gitignore -ItemType File

Open file:
notepad .gitignore

Add recommended ignores:
venv/
.env/
.venv/
__pycache__/
*.pyc
db.sqlite3


This keeps unwanted files out of GitHub.

🔄 3. Remove files already tracked (if needed)

If venv or db.sqlite3 were committed earlier:

git rm -r --cached venv
git rm --cached db.sqlite3


Commit the fix:

git commit -m "Remove venv and db from tracking"

📤 4. Add All Files to Git Tracking
git add .

📝 5. Commit Your Work
git commit -m "Initial commit: Gurukul project with institute and shop modules"

🌐 6. Connect Your GitHub Repository
git remote add origin https://github.com/yourusername/Gurukul.git

🚀 7. Push the Project to GitHub
git push -u origin main


If your branch is master:

git push -u origin master

🔄 8. Pushing Future Changes

After making updates:

git add .
git commit -m "Describe your update here"
git push origin main

