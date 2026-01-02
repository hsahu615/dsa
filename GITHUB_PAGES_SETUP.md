# GitHub Pages Setup Guide

## Quick Start

### 1. Initialize Git Repository (if not already done)

```bash
cd "/Users/sahu/Downloads/Editing Pack/Educative.io - Grokking the Coding Interview - Patterns for Coding Questions 2"
git init
git add .
git commit -m "Initial commit: Course materials with navigation"
```

### 2. Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Name your repository (e.g., `coding-interview-patterns`)
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### 3. Push to GitHub

```bash
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual GitHub username and repository name
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 4. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**

### 5. Access Your Site

Your site will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME
```

It may take a few minutes to deploy initially.

## Important Notes

- ✅ All navigation uses relative paths - works perfectly on GitHub Pages
- ✅ The `index.html` file will serve as your landing page
- ✅ All HTML files with navigation buttons will work correctly
- ✅ No server-side processing needed - GitHub Pages serves static files

## Updating Your Site

To update your site after making changes:

```bash
git add .
git commit -m "Update: description of changes"
git push
```

Changes will be live within a few minutes.

## Troubleshooting

- If pages don't load, check that the file paths are correct
- Make sure you've selected the correct branch in GitHub Pages settings
- Check repository settings to ensure Pages is enabled
- File names with spaces are fine - GitHub Pages handles them correctly

