---
description: Smart git pull with automatic stash handling
globs: ""
alwaysApply: false
---

# 🔄 SMART GIT PULL

Intelligently pull from the current branch with automatic stash handling for untracked files.

## 🎯 YOUR MISSION

Execute a safe git pull that:
1. **Detects conflicts** - Identifies untracked files that would block the pull
2. **Stashes automatically** - Saves your local work safely
3. **Pulls cleanly** - Gets latest changes from remote
4. **Offers restoration** - Gives you the option to reapply stashed work
5. **Provides feedback** - Shows what happened at each step

---

## 📋 WORKFLOW

### Step 1: Determine Current Branch

Run these commands to understand the current state:
- `git branch --show-current` - Get current branch name
- `git status --short` - Check for untracked/modified files

### Step 2: Attempt Pull

Try pulling from the current branch:
```bash
git pull origin $(git branch --show-current)
```

### Step 3: Handle Conflicts (If Any)

**If pull fails due to untracked files:**

1. **Inform the user:**
   ```
   ⚠️ Found untracked files that conflict with remote changes.
   🗂️ Stashing them automatically to complete the pull...
   ```

2. **Stash the files:**
   ```bash
   git add -A && git stash push -m "Auto-stash before pull on $(date '+%Y-%m-%d %H:%M')"
   ```

3. **Retry the pull:**
   ```bash
   git pull origin $(git branch --show-current)
   ```

4. **Show what was stashed:**
   ```bash
   git stash list | head -1
   ```

### Step 4: Report Results

**After successful pull, show:**
- Number of files changed
- Key changes (new files, renames, major updates)
- Whether anything was stashed

**Example output structure:**
```
✅ Pull completed successfully!

📊 Changes pulled:
- 51 files changed, 3,923 insertions(+), 78 deletions(-)
- New: Interlingo architecture docs, N8N setup guide
- Renamed: App - Interlingo → Interlingo
- Updated: end-of-day.md, PAI SKILL.md

🗂️ Stashed: 1 item (Daily Notes/2025-10-21.md)
```

### Step 5: Offer Stash Restoration

**If files were stashed, ask the user:**

"I've stashed your local changes. What would you like to do?

- **Option A:** Apply the stash (merge your changes back in)
- **Option B:** Keep it stashed for later review
- **Option C:** Drop the stash (discard your local changes)

Type 'apply', 'keep', or 'drop'."

**Based on response:**
- `apply` → Run `git stash pop` and show merge results
- `keep` → Show `git stash list` for reference
- `drop` → Run `git stash drop` after confirming one more time

---

## 🎨 RESPONSE FORMAT

Use the mandatory PAI response format:

```
📋 SUMMARY: Git pull from [branch-name]

🔍 ANALYSIS:
Current branch: [branch]
Remote: [remote-url]
Local state: [clean/untracked files/modified files]

⚡ ACTIONS:
- Checked current branch: [branch]
- [If needed] Stashed untracked files: [files]
- Pulled from origin/[branch]
- Retrieved [X] files with [Y] changes

✅ RESULTS:
[Detailed change summary as shown in Step 4]

📊 STATUS: Pull completed, repository up to date

[If stashed]
➡️ NEXT: What would you like to do with your stashed changes?

🎯 COMPLETED: Successfully pulled latest changes from [branch]

🗣️ CUSTOM COMPLETED: Pull complete, [X] files updated
```

---

## 🚨 SAFETY RULES

1. ✅ **ALWAYS show the user what's being stashed** - No silent operations
2. ✅ **ASK before dropping stashes** - Don't discard user work without confirmation
3. ✅ **Show meaningful summaries** - Highlight important changes, not just file counts
4. ✅ **Handle merge conflicts gracefully** - If stash pop conflicts, guide the user
5. ❌ **NEVER force operations** - No `--force` flags
6. ❌ **NEVER pull from wrong branch** - Always use current branch

---

## 💡 EXAMPLE EXECUTION

**User:** `/pull`

**Chavvo:**

📋 SUMMARY: Git pull from chavvo-update-v0.2

🔍 ANALYSIS:
Current branch: chavvo-update-v0.2
Remote: github.com:buttercupck/bcck_vault
Local state: 1 untracked file found (Daily Notes/2025-10-21.md)

⚡ ACTIONS:
- Checked current branch: chavvo-update-v0.2
- Stashed untracked file: Daily Notes/2025-10-21.md
- Pulled from origin/chavvo-update-v0.2
- Retrieved 51 files with 3,923 insertions, 78 deletions

✅ RESULTS:
✅ Pull completed successfully!

📊 Changes pulled:
- 51 files changed, 3,923 insertions(+), 78 deletions(-)
- New files: Interlingo architecture docs, N8N setup guide, GCal integration
- Renamed: App - Interlingo → Interlingo (directory restructure)
- Updated: end-of-day.md, PAI SKILL.md, multiple system logic files

🗂️ Stashed: 1 item
- stash@{0}: Auto-stash before pull on 2025-10-22 09:15

📊 STATUS: Pull completed, repository up to date with remote

➡️ NEXT: What would you like to do with your stashed changes?
- **Option A:** Apply the stash (merge your changes back in)
- **Option B:** Keep it stashed for later review
- **Option C:** Drop the stash (discard your local changes)

Type 'apply', 'keep', or 'drop'.

🎯 COMPLETED: Successfully pulled latest changes from chavvo-update-v0.2

🗣️ CUSTOM COMPLETED: Pull complete, fifty-one files updated

---

## 🔧 ERROR HANDLING

### Merge Conflicts on Stash Pop

**If `git stash pop` creates conflicts:**

```
⚠️ Merge conflict detected when applying stash!

The stashed file conflicts with the pulled changes.

Files in conflict:
- Daily Notes/2025-10-21.md

What would you like to do?
- **Option A:** Manually resolve conflicts (I'll guide you)
- **Option B:** Keep the remote version and discard stashed changes
- **Option C:** Keep the stash and review differences manually

Type 'resolve', 'remote', or 'review'.
```

### Network/Connection Issues

**If pull fails due to connection:**

```
❌ Pull failed: Could not connect to remote repository

This might be a network issue or authentication problem.

Troubleshooting steps:
1. Check your internet connection
2. Verify GitHub authentication: `gh auth status`
3. Try again in a moment

Your local work is safe. Nothing was changed.
```

### No Remote Tracking Branch

**If branch has no upstream:**

```
⚠️ This branch doesn't track a remote branch yet.

To set up tracking:
`git push -u origin [branch-name]`

Would you like me to:
- **Option A:** Set up tracking and push this branch
- **Option B:** Pull from a different branch
- **Option C:** Skip the pull

Type 'setup', 'different', or 'skip'.
```

---

**This command should make git pulls effortless and beginner-friendly.**
