---
type: EOD
category: workflow
date: 2025-10-07
---

# Session Terminate Protocol

**Use this flow at the end of every day to ensure work is saved and synced across all devices.**

---
## Task 1:  Reviewing what was accomplished

  - Build out a recap of the days workload.
  - Add to the Daily Note
  - Clearing temporary files
  - Setting priorities for tomorrow


### **Task 2: Git Add All Commit**

Navigate to root folder, bcck_vault. Check for uncommitted changes first. Branch strategy is commit to main, unless otherwise told durning the work day. Be selective of untracked files. Add all changes. I trust your ability to create effective messages. Messages need to be approved by me before push.

**Commit Message Format:**
```
<type>: <short summary> (50 chars max)

<optional detailed description>
```
**Types:** feat, fix, docs, refactor, chore

```
feat: Add TERMINATE-PROTOCOL.md for daily EOD workflow

Created standardized checklist for end-of-day git operations
to ensure work is synced across devices.
```

**Expected output:**
- ✅ Files committed successfully
- ✅ Pushed to remote repository
- ✅ No errors

**If you get errors:**
- Check network connection
- Verify git credentials
- Report back to me
## 🔐 Security Notes
- NEVER commit `.env` files, API keys, tokens, credentials, private keys, passwords anything in .gitignore
```bash
git diff | grep -i "api_key\|secret\|password\|token"
```

## Validation
Ask for my approval and once approved push and provide status update on the push.

---

*Protocol established: 2025-10-07*
*Part of Boot Down Process v1.5*
*Required for multi-device sync*

---
