# Restructuring Progress & Migration Guide

## Phase 1: Create New Folder Structure ✅
## Phase 2: Move and Rename Files (In Progress)
## Phase 3: Update Internal Links
## Phase 4: Verify Structure

## UPDATED MIGRATION GUIDE

### 📁 Current → New Location Mapping:

#### INCOME/ (Revenue-generating work)
```
intercom/ → INCOME/intercom/
JPeptics/ → INCOME/JPeptics/
```

#### LEARNING/ (Skill development) - ✅ Subfolders created
```
bug bounty/ → LEARNING/web-security/traditional-hacking/
ai_bugBounty/ → LEARNING/web-security/ai-security/
(Remove duplicates between the two)

Extract development content from intercom/ → LEARNING/full-stack-dev/
Move ai_bugBounty/AI Prompt Engineering/ → LEARNING/ai-prompt-engineering/
```

#### SELF/ (Keep as SELF, not PERSONAL)
```
self/ → SELF/
├── Keep Daily Logs/ → DAILY-LOGS/ (move this out)
├── athlete/ → Keep as SELF/athlete/ (unchanged per your request)
├── Finances/ → Keep as SELF/Finances/
├── Health Dashboard.md → Keep as SELF/Health Dashboard.md
├── Telos/ → Keep as SELF/Telos/
└── Training/ → Keep as SELF/Training/

0_Personal Telos.md → SELF/Telos/SELF-Telos-Personal.md
Dinner Times.md → SELF/Lifestyle/SELF-Lifestyle-Dinner-Times.md (create Lifestyle folder)
```

#### SPIRITUAL/ (Faith and worship)
```
god/ → SPIRITUAL/
```

#### DAILY-LOGS/ (Task tracking across silos)
```
self/Daily Logs/ → DAILY-LOGS/
```

#### SYSTEM/ (Vault operations) - ✅ Subfolders created
```
templates/ → SYSTEM/templates/
Excalidraw/ → SYSTEM/assets/excalidraw/
Screenshot 2025-09-15 at 4.56.26 PM.png → SYSTEM/assets/screenshots/
gpt-5-for-coding-cheatsheet.pdf → SYSTEM/assets/documents/
```

#### Mysterious Files:
```
Untitled*.base → Investigate/ignore (seems to auto-regenerate)
```

### 🏷️ Updated File Renaming Rules:

#### By Silo:
- **INCOME**: `INC-[Category]-[Specific-Topic].md`
- **LEARNING**: `LRN-[Category]-[Specific-Topic].md`
- **SELF**: `SELF-[Category]-[Specific-Topic].md`
- **SPIRITUAL**: `SPI-[Category]-[Specific-Topic].md`
- **SYSTEM**: `SYS-[Category]-[Specific-Topic].md` or `TMPL-[Purpose].md`
- **DAILY-LOGS**: Keep existing format

### 📋 Simplified Action Items:
1. ✅ I created all necessary subfolders
2. ⏳ You move existing folders:
   - `intercom/` → `INCOME/`
   - `JPeptics/` → `INCOME/`
   - `bug bounty/` → `LEARNING/web-security/traditional-hacking/`
   - `ai_bugBounty/` → `LEARNING/web-security/ai-security/`
   - `god/` → `SPIRITUAL/`
   - `self/Daily Logs/` → `DAILY-LOGS/`
   - `templates/` → `SYSTEM/`
   - `Excalidraw/` → `SYSTEM/assets/`
   - Assets → `SYSTEM/assets/` (appropriate subfolders)
3. ⏳ Let me know when complete
4. ⏳ I'll handle file renaming and link updates

---
*Updated: 2025-09-16*  
*~ Claude (Chavvo)*