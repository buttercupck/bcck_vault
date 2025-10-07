# Vault Git Sync Setup Guide

## Overview
This guide sets up Git version control on your 3 desktop devices while keeping S3 sync active on all 5 devices (including iPhone/iPad).

## Part 1: Main Mac (Current Device) - ALREADY DONE ✅

Your main Mac (Desktop vault) is already configured with:
- ✅ Git initialized at `~/Desktop/v1_self_vault`
- ✅ .gitignore created
- ✅ Initial commit made
- ✅ Pushed to: `https://github.com/buttercupck/bcck_vault.git`

**Working Directory**: `~/Desktop/v1_self_vault`

## Part 2: Add Sync Alias (All 3 Desktop Devices)

Add this to your `~/.zshrc` or `~/.bashrc`:

```bash
# Obsidian vault sync alias
alias vsync='cd ~/Desktop/v1_self_vault && git add . && git commit -m "sync: $(hostname) $(date +%Y-%m-%d_%H:%M)" && git pull --rebase && git push'
```

Then reload:
```bash
source ~/.zshrc
```

**Usage**: Just run `vsync` before closing Obsidian.

## Part 3: Desktop Device 2 & 3 Setup

### Option A: Clone to New Device (Recommended)

```bash
# 1. Clone the repository
cd ~/Desktop
git clone https://github.com/buttercupck/bcck_vault.git v1_self_vault

# 2. Open Obsidian and point it to the cloned vault
# File → Open Vault → ~/Desktop/v1_self_vault

# 3. Install Remotely Save plugin in Obsidian
# 4. Configure same S3 credentials as other devices

# 5. Add sync alias (see Part 2 above)
```

### Option B: Existing Vault on Device

If vault already exists on the device via S3 sync:

```bash
# 1. Navigate to vault
cd /Users/itza/Documents/vault_self/v1_self_vault

# 2. Check git status
git status

# 3. Pull latest changes
git pull origin main

# 4. Add sync alias (see Part 2 above)
```

## Part 4: iPhone/iPad Setup - NO CHANGES NEEDED ✅

Your iPhone and iPad are already set up with:
- ✅ Obsidian app installed
- ✅ Remotely Save configured with S3
- ✅ Auto-sync enabled

**No Git needed on iOS** - S3 handles all syncing automatically.

## Daily Workflow

### On Desktop (Any of 3 computers)

**Before working:**
```bash
vsync  # Pulls latest, pushes any uncommitted changes
```

**After working:**
```bash
vsync  # Commits and pushes your changes
```

**Or manually:**
```bash
cd /Users/itza/Documents/vault_self/v1_self_vault
git pull
# ... work in Obsidian ...
git add .
git commit -m "update"
git push
```

### On iPhone/iPad

Just use Obsidian normally - Remotely Save handles everything automatically in the background.

## Conflict Resolution

### Desktop ↔ Desktop
- Git will show merge conflicts
- Edit conflicted files manually
- Run `git add .` then `git commit` then `git push`

### Desktop ↔ Mobile
- Remotely Save creates `-conflict` files
- Review both versions
- Keep the correct one, delete the conflict file
- Let both Git (desktop) and S3 (mobile) sync

### Mobile ↔ Mobile
- Rare, S3 uses last-write-wins
- Check file timestamps if something looks wrong

## Troubleshooting

### "Permission denied (publickey)" on push
```bash
# Generate SSH key
cd ~/.ssh
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/keys
```

### "Your branch is behind 'origin/main'"
```bash
git pull --rebase
# Fix any conflicts if they appear
git push
```

### "Uncommitted changes" on pull
```bash
git stash
git pull
git stash pop
```

### S3 and Git out of sync
```bash
# Git is source of truth for desktops
# Let S3 sync from Git
git pull  # Get latest from Git
# Wait for S3 to sync (check Remotely Save)
```

## What's Synced Where

| Content | Desktop Git | S3 (All Devices) | Notes |
|---------|------------|------------------|-------|
| Markdown files | ✅ | ✅ | Both systems |
| Images/PDFs | ✅ | ✅ | Both systems |
| Plugin files | ✅ | ✅ | Sync settings across devices |
| Workspace | ❌ | ✅ | Excluded from Git (device-specific) |
| .trash | ❌ | ❌ | Not synced anywhere |

## Benefits of This Setup

1. **Version History**: Git tracks all changes with full history
2. **Conflict Resolution**: Git handles merge conflicts better than S3
3. **Mobile Friendly**: iOS devices use simple S3 sync
4. **Backup**: Both Git remote AND S3 bucket serve as backups
5. **Fast Sync**: S3 provides quick mobile sync, Git for desktop control

## Quick Reference

```bash
# Sync everything (before/after work)
vsync

# Check status
cd /Users/itza/Documents/vault_self/v1_self_vault && git status

# View recent commits
git log --oneline -5

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View what changed
git diff
```
