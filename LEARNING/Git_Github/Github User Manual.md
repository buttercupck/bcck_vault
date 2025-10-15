# GitHub User Manual

---
tags: learning, git, github, version-control
---

## Your Current Understanding
Yes, your understanding is mostly correct! GitHub hosts the main repository online, you clone it to your machine, make changes, and push them back. But there's more nuance to branches, forks, and workflow.

---

## Core Concepts Visualized

```
┌─────────────────────────────────────────┐
│         GitHub (Remote)                 │
│  ┌───────────────────────────────────┐  │
│  │     main branch (origin/main)     │  │
│  └───────────────────────────────────┘  │
│            ▲                 │          │
│            │ push            │ clone    │
│            │                 ▼          │
└────────────┼─────────────────┼──────────┘
             │                 │
             │                 │
┌────────────┼─────────────────┼───────────┐
│            │                 │           │
│  ┌─────────┴─────────────────▼────────┐  │
│  │   Local Repository (Your Machine)  │  │
│  │                                    │  │
│  │  main ──┐                          │  │
│  │         │                          │  │
│  │         └─► feature-branch         │  │
│  └────────────────────────────────────┘  │
│         Your Computer                    │
└──────────────────────────────────────────┘
```

---

## Essential Commands

### Clone - Copy Repository to Your Machine
```bash
git clone <repository-url>
```
**When:** First time working with a repository
**What it does:** Downloads entire repository history to your computer
**Example:**
```bash
git clone https://github.com/username/repo-name.git
```

### Pull - Get Latest Changes from Remote
```bash
git pull
```
**When:** Before starting work (daily habit)
**What it does:** Downloads and merges remote changes into your current branch
**Example workflow:**
```bash
cd my-project
git pull origin main  # Get latest from main branch
```

### Add & Commit - Save Your Changes Locally
```bash
git add <file-name>        # Stage specific file
git add .                  # Stage all changes
git commit -m "message"    # Save with description
```
**When:** After making changes you want to save
**What it does:** Takes snapshot of your work
**Example:**
```bash
git add index.html
git commit -m "Add hero section to homepage"
```

### Push - Send Your Changes to GitHub
```bash
git push origin <branch-name>
```
**When:** Ready to share your work or back it up
**What it does:** Uploads your commits to GitHub
**Example:**
```bash
git push origin main
```

### Status - Check What's Changed
```bash
git status
```
**When:** Anytime you want to see what's modified
**What it does:** Shows modified files and staging status

---

## Branches vs Forks

### Branches - Different Versions Within Same Repository

```
main ──────●────────●────────●────────●
            \                /
             \              /
              ●────●────●──   feature-branch
```

**What:** Separate line of development in YOUR repository
**When to use:**
- Working on new features
- Experimenting without affecting main code
- Team collaboration on same project

**Commands:**
```bash
# Create new branch
git branch feature-name

# Switch to branch
git checkout feature-name

# Create and switch in one command
git checkout -b feature-name

# List all branches
git branch -a

# Merge branch into main
git checkout main
git merge feature-name

# Delete branch after merging
git branch -d feature-name
```

**Typical workflow:**
```bash
git checkout -b add-login-form    # Create feature branch
# ... make changes ...
git add .
git commit -m "Add login form"
git push origin add-login-form    # Push branch to GitHub
# ... create pull request on GitHub ...
# ... after PR approved and merged ...
git checkout main                 # Switch back to main
git pull                          # Get the merged changes
git branch -d add-login-form      # Clean up local branch
```

### Forks - Your Own Copy of Someone Else's Repository

```
Original Repo (danielmiessler/PAI)
       │
       │ fork
       ▼
Your Fork (itza/PAI)
       │
       │ clone
       ▼
Your Computer
```

**What:** Complete copy of someone else's repository under your GitHub account
**When to use:**
- Contributing to open source projects you don't own
- Experimenting with someone else's code without affecting their project
- Creating your own version of a project

**Workflow:**
1. Fork on GitHub (click "Fork" button)
2. Clone YOUR fork to your machine:
```bash
git clone https://github.com/YOUR-USERNAME/repo-name.git
cd repo-name
```
3. Add original repo as "upstream":
```bash
git remote add upstream https://github.com/ORIGINAL-OWNER/repo-name.git
```
4. Make changes on a branch:
```bash
git checkout -b my-contribution
# ... make changes ...
git add .
git commit -m "Fix bug in user authentication"
git push origin my-contribution
```
5. Create Pull Request on GitHub to original repository

**Keep your fork updated:**
```bash
git fetch upstream              # Get changes from original repo
git checkout main
git merge upstream/main         # Merge into your main
git push origin main            # Update your fork on GitHub
```

**Key Difference:**
- **Branch:** Working within your own or team's repository
- **Fork:** Your own copy of someone else's repository

---

## Pull Requests (PRs)

**What:** Request to merge your changes into another branch (usually main)
**Where:** Created on GitHub website, not command line
**When to use:**
- Proposing changes to a project
- Code review before merging to main
- Collaborating with team

### Creating a Pull Request

**Step 1:** Push your branch to GitHub
```bash
git push origin feature-branch-name
```

**Step 2:** On GitHub website:
1. Navigate to the repository
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select your branch to merge
5. Add title and description
6. Click "Create pull request"

**Step 3:** Team reviews, discusses, requests changes

**Step 4:** After approval:
- Project maintainer clicks "Merge pull request"
- Or you merge (if you have permissions)

### PR Best Practices
- **Clear title:** "Add user authentication system"
- **Detailed description:** What changed and why
- **Reference issues:** "Fixes #42"
- **Keep PRs focused:** One feature per PR
- **Respond to feedback:** Make requested changes

---

## Common Workflows

### Daily Work Routine
```bash
# Start of day
git checkout main
git pull origin main              # Get latest changes

# Create feature branch
git checkout -b add-new-feature

# Work on changes
# ... edit files ...
git add .
git commit -m "Add feature X"

# Push to GitHub
git push origin add-new-feature

# Create PR on GitHub
# After PR merged, clean up
git checkout main
git pull
git branch -d add-new-feature
```

### Contributing to Open Source
```bash
# One-time setup
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/project.git
cd project
git remote add upstream https://github.com/ORIGINAL-OWNER/project.git

# For each contribution
git checkout main
git pull upstream main             # Get latest from original
git checkout -b fix-bug-123
# ... make changes ...
git add .
git commit -m "Fix bug in payment processing"
git push origin fix-bug-123
# Create PR from your fork to original repo on GitHub
```

### Fixing Conflicts

When `git pull` or `git merge` has conflicts:
```bash
# Git will mark conflicted files
git status                         # See what's conflicted

# Open conflicted files, look for:
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> branch-name

# Edit file to resolve (keep what you want, delete markers)
git add resolved-file.js
git commit -m "Resolve merge conflict"
git push
```

---

## Useful Status Commands

```bash
# What's changed?
git status

# What did I change in detail?
git diff

# What commits have I made?
git log
git log --oneline                  # Compact view

# What branches exist?
git branch -a

# Where am I?
git branch                         # Shows current branch with *

# What remotes do I have?
git remote -v
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Get latest changes | `git pull` |
| See what changed | `git status` |
| Stage changes | `git add .` or `git add filename` |
| Save changes locally | `git commit -m "message"` |
| Send to GitHub | `git push origin branch-name` |
| Create branch | `git checkout -b new-branch` |
| Switch branch | `git checkout branch-name` |
| See all branches | `git branch -a` |
| Delete local branch | `git branch -d branch-name` |
| Clone repository | `git clone url` |
| Check remote URLs | `git remote -v` |

---

## Emergency Commands (Use With Caution)

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

### Discard All Local Changes
```bash
git reset --hard HEAD
git clean -fd
```
⚠️ **WARNING:** This deletes all uncommitted work!

### Fix Last Commit Message
```bash
git commit --amend -m "New message"
```

---

## References

- [GitHub Official Docs](https://docs.github.com)[^1]
- [Git Documentation](https://git-scm.com/doc)[^2]
- [GitHub Flow Guide](https://docs.github.com/en/get-started/quickstart/github-flow)[^3]
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)[^4]

[^1]: https://docs.github.com
[^2]: https://git-scm.com/doc
[^3]: https://docs.github.com/en/get-started/quickstart/github-flow
[^4]: https://www.atlassian.com/git/tutorials