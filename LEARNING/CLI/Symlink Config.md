---
date: 2025-10-07
type: task
aliases:
  - Oct07
tags:
  - chavvo-to-do
---

## First thing:
---
chavvotodo
## PAI Symlink Configuration - Multi-Device Setup 

**Context:** PAI system syncs across multiple computers via vault, but had hardcoded paths in `settings.json` causing hooks to fail on different machines.

**Solution Implemented (Work Computer):**

### Step 1: Create Symlink at Canonical Location
```bash
ln -s /Users/intercomlanguageservices/bcck_vault/PAI/PAI_DIRECTORY ~/.claude/PAI_DIRECTORY
```

### Step 2: Remove Hardcoded PAI_DIR from settings.json
Removed this line from `PAI_DIRECTORY/settings.json`:
```json
"PAI_DIR": "/Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY",
```

This allows PAI hooks to use their built-in fallback: `${HOME}/.claude/PAI_DIRECTORY`

### Step 3: Verify Hook Functionality
```bash
DA=TestAI bun ~/.claude/PAI_DIRECTORY/hooks/session-start-hook.ts
```

###TODO: Apply Same Fix to Main Computer

**On main computer (Users/itza), run:**

```bash
# Create the canonical symlink
ln -s /Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY ~/.claude/PAI_DIRECTORY

# Verify symlink created correctly
ls -la ~/.claude/ | grep PAI

# Test hook works
DA=TestAI bun ~/.claude/PAI_DIRECTORY/hooks/session-start-hook.ts
```

**Expected Output:**
- ✅ Stop-hook found and is executable
- 📍 Set initial tab title: "Chavvo Ready"
- Connection refused to localhost:8888 (expected - voice server not running)

**Why This Works:**
- PAI was designed with `~/.claude` as the canonical location
- All hooks have fallback: `process.env.PAI_DIR || '${HOME}/.claude'`
- Symlink resolves to correct path on each machine
- `settings.json` now machine-agnostic, syncs without conflicts

---

## Analysis: Current vs. Proposed System

### Current State (Main Computer - /Users/itza)
❌ **Issues Found:**
1. **Hardcoded PAI_DIR in settings.json** (line 7):
   ```json
   "PAI_DIR": "/Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY"
   ```
   - Machine-specific path
   - Will break on work computer or any other device
   - Creates sync conflicts in git

2. **No symlink at canonical location**:
   - `~/.claude/PAI_DIRECTORY` does NOT exist
   - All hooks reference `${PAI_DIR}` which works only because of hardcoded env var
   - System not portable

3. **Hook dependency on env var**:
   - 6 hooks all use `${PAI_DIR}` variable
   - Currently works but fragile
   - Not using designed fallback mechanism

### Work Computer State (Already Fixed)
✅ **Correct Implementation:**
1. Symlink created: `~/.claude/PAI_DIRECTORY` → actual vault location
2. Hardcoded PAI_DIR removed from settings.json
3. Hooks work via fallback: `process.env.PAI_DIR || '${HOME}/.claude'`

### Design Analysis
**PAI was architecturally designed for this:**
- Found in `load-dynamic-requirements.ts:51`:
  ```typescript
  const paiDir = process.env.PAI_DIR || `${process.env.HOME}/.claude`;
  ```
- This fallback exists but is currently bypassed by hardcoded env var
- Symlink approach is **the intended design pattern**

### Why This Matters
1. **Multi-device sync**: Vault syncs via git/iCloud - settings.json should be machine-agnostic
2. **Portability**: New computers should just need symlink, not settings edits
3. **Reliability**: Reduces configuration errors and path conflicts
4. **Design integrity**: Using system as architecturally intended

---

---

## ✅ IMPLEMENTATION COMPLETE

**Executed on:** 2025-10-07
**Status:** Successfully implemented on main computer

### Changes Made:
1. ✅ Created symlink: `~/.claude/PAI_DIRECTORY` → `/Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY`
2. ✅ Removed hardcoded `PAI_DIR` from `settings.json`
3. ✅ Added fallback mechanism to `session-start-hook.ts`
4. ✅ Removed `PAI_DIR` export from `~/.zshrc`
5. ✅ Updated `vsync` alias to use `bcck_vault` path
6. ✅ Tested hook functionality - working correctly

### Validation Results:
- Symlink accessible: 6 hook files found via `~/.claude/PAI_DIRECTORY/hooks/`
- Hook test passed: Stop-hook found and executable
- Settings.json portable: No machine-specific PAI_DIR in env section
- Fallback mechanism working: Hooks resolve correctly without env var

### Next Steps:
- Restart terminal/shell to load new .zshrc (or run: `source ~/.zshrc`)
- Both machines (main + work) now using identical portable configuration
- New devices only need: `ln -s <vault_path>/PAI/PAI_DIRECTORY ~/.claude/PAI_DIRECTORY`

---

## Implementation Plan

### Phase 1: Verification & Backup ✅
**Tasks:**
- [x] Verify current settings.json has hardcoded PAI_DIR
- [x] Verify symlink does NOT exist on main computer
- [x] Confirm hook fallback mechanism exists in codebase
- [x] Document current vs. work computer configuration

### Phase 2: Apply Fix to Main Computer
**Tasks:**
1. **Create canonical symlink**
   ```bash
   ln -s /Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY ~/.claude/PAI_DIRECTORY
   ```

2. **Verify symlink creation**
   ```bash
   ls -la ~/.claude/ | grep PAI
   # Expected: PAI_DIRECTORY -> /Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY
   ```

3. **Remove hardcoded PAI_DIR from settings.json**
   - Edit: `/Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY/settings.json`
   - Remove line 7: `"PAI_DIR": "/Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY",`
   - This allows hooks to use fallback: `${HOME}/.claude/PAI_DIRECTORY`

4. **Test hook functionality**
   ```bash
   # Test session-start hook
   DA=TestAI bun ~/.claude/PAI_DIRECTORY/hooks/session-start-hook.ts

   # Expected output:
   # ✅ Stop-hook found and is executable
   # 📍 Set initial tab title: "Chavvo Ready"
   # (Connection refused to localhost:8888 is expected if voice server not running)
   ```

5. **Test complete system**
   ```bash
   # Start a new Claude session and verify:
   # - Session start hook executes
   # - User prompt submit hook works
   # - All dynamic requirement loading functions correctly
   ```

### Phase 3: Validation & Documentation
**Tasks:**
1. **Verify both machines work identically**
   - Main computer (Users/itza)
   - Work computer (Users/intercomlanguageservices)

2. **Confirm settings.json is now portable**
   - No machine-specific paths
   - Can sync via git without conflicts

3. **Update documentation**
   - Document symlink as standard setup procedure
   - Add to onboarding for new devices

### Phase 4: Future-Proofing
**Tasks:**
1. **Create setup script for new devices**
   ```bash
   # setup-pai.sh
   #!/bin/bash
   VAULT_PATH="$1"
   ln -s "$VAULT_PATH/PAI/PAI_DIRECTORY" ~/.claude/PAI_DIRECTORY
   echo "PAI symlink created. Run test: DA=TestAI bun ~/.claude/PAI_DIRECTORY/hooks/session-start-hook.ts"
   ```

2. **Add setup instructions to README**
   - One-command setup for new machines
   - Clear explanation of symlink architecture

---

## Risk Assessment

**Low Risk:**
- Symlink is non-destructive (just creates a pointer)
- Removing env var relies on existing fallback mechanism
- Can easily revert by re-adding PAI_DIR to settings.json

**Validation Points:**
- ✅ Fallback code exists: `process.env.PAI_DIR || '${HOME}/.claude'`
- ✅ Work computer already using this pattern successfully
- ✅ All hooks reference `${PAI_DIR}` which will resolve via symlink

**Rollback Plan:**
If issues occur, re-add to settings.json:
```json
"PAI_DIR": "/Users/itza/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY"
```