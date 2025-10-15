---
type: budget-docs
category: workflow
date: 2025-10-07
---

# Session Terminate Protocol

**Use this checklist at the end of every budget work session to ensure your work is saved and synced across all devices.**

---

## 🔒 Terminate Protocol Checklist

### **Step 1: Save All Changes**
- [ ] Close all open notes in Obsidian
- [ ] Verify all edits are saved (no unsaved indicators)

---

### **Step 2: Git Commit & Push**

**Open Terminal and run:**

```bash
# Navigate to vault
cd /Users/intercomlanguageservices/bcck_vault

# Check status
git status

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Budget session $(date +%Y-%m-%d): Updated balances and bills"

# Push to remote repository
git push
```

**Expected output:**
- ✅ Files committed successfully
- ✅ Pushed to remote repository
- ✅ No errors

**If you get errors:**
- Check network connection
- Verify git credentials
- Try `git pull` first if behind

---

### **Step 3: Remotely Save (Obsidian Plugin)**

**In Obsidian:**

1. Open Command Palette (`Cmd + P`)
2. Type: "Remotely Save"
3. Select: **"Remotely Save: start sync"**
4. Wait for sync confirmation
5. Verify: "Sync completed" notification

**Alternative:**
- Click the sync icon in Obsidian status bar (if configured)
- Or use sidebar "Remotely Save" button

**What this does:**
- Syncs vault to cloud storage (if configured)
- Backs up to remote location
- Ensures multi-device access

---

### **Step 4: Log Off**

**Final checks:**
- [ ] Git push successful
- [ ] Remotely Save completed
- [ ] All notes closed
- [ ] No unsaved changes

**Then:**
- Close Obsidian
- Close Terminal
- Log off system

---

## 🔄 Quick Command Version

**For experienced users - run all at once:**

```bash
cd /Users/intercomlanguageservices/bcck_vault && \
git add . && \
git commit -m "Budget session $(date +%Y-%m-%d): Updated balances and bills" && \
git push && \
echo "✅ Git sync complete - Now run Remotely Save in Obsidian"
```

Then:
1. Obsidian → Command Palette → "Remotely Save: start sync"
2. Wait for confirmation
3. Log off

---

## ⚠️ Important Notes

### **When to Run This:**
- ✅ End of budget work session
- ✅ After updating balances
- ✅ After adding/editing bills
- ✅ After weekly budget setup
- ✅ Before switching computers

### **What Happens If You Don't:**
- ❌ Changes won't sync to other devices
- ❌ Work could be lost if system crashes
- ❌ Main computer won't have latest updates
- ❌ Git history incomplete

### **Git Commit Message Guidelines:**
- **Format:** `Budget session YYYY-MM-DD: [what you did]`
- **Examples:**
  - `Budget session 2025-10-07: Updated balances and bills`
  - `Budget session 2025-10-07: Added new credit card bill`
  - `Budget session 2025-10-07: Set Week 42 budget`
  - `Budget session 2025-10-07: Tracked weekly spending`

---

## 🔍 Verification Steps

### **Verify Git Push:**
```bash
# Check remote status
git log --oneline -1

# Should show your latest commit
```

### **Verify Remotely Save:**
- Check Obsidian notification area
- Look for "Last sync: [timestamp]"
- Should be within last minute

### **Verify on Other Device:**
1. Open vault on main computer
2. Pull latest changes: `git pull`
3. Run Remotely Save
4. Verify your changes appear

---

## 🆘 Troubleshooting

### **Git Push Fails:**
```bash
# Pull first, then push
git pull --rebase
git push
```

### **Remotely Save Fails:**
- Check internet connection
- Check cloud storage credentials
- Try manual sync from plugin settings

### **Merge Conflicts:**
```bash
# See conflicted files
git status

# Resolve conflicts manually, then:
git add .
git commit -m "Resolved merge conflicts"
git push
```

---

## 📱 Multi-Device Sync Workflow

### **On Work Computer (End of Day):**
1. ✅ Git commit & push
2. ✅ Remotely Save sync
3. ✅ Log off

### **On Main Computer (Next Time):**
1. ✅ Git pull
2. ✅ Remotely Save sync
3. ✅ Start working with latest changes

---

## 🎯 Best Practices

1. **Commit often** - Don't wait until end of day
2. **Descriptive messages** - Know what changed
3. **Always push** - Don't just commit locally
4. **Run both syncs** - Git AND Remotely Save
5. **Verify on other device** - Confirm sync worked

---

## ⏱️ Time Required

- **Git Commit & Push:** 30 seconds
- **Remotely Save:** 15 seconds
- **Total:** Less than 1 minute

**Worth it to protect your work!**

---

## 🔐 Security Notes

- Git commits are local until pushed
- Remotely Save uses encrypted connection (if configured)
- Always log off when done
- Don't leave terminal open with vault path

---

*Protocol established: 2025-10-07*
*Part of Budget System v1.0*
*Required for multi-device sync*
