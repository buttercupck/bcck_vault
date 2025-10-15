---
request_id: CR-20251001
date_created: 2025-10-01
status: COMPLETED
client: JPeptics
---

#### REFERENCES
**Documentation:**
- [ ] Structure of tasks [[PROPOSED FORMAT - Structure of Change Requests 1]]
- [ ] [[Product Photo Naming Conventions]]
- [ ] [[Branding]] (style guide)
- [ ] [[Website File Tree]]
---
### TASK 1
#### LOCATION
**File/Page:** index.php
**Section Identifier:** <section class="hero">
- Element type: hero-banner

## CURRENT STATE
**What exists now:**
Centered text. 
## DESIRED STATE
### Action Type: REPLACE
### Change Category: VISUAL

**What should it become:**

#### For VISUAL changes:
Left-aligned text
---
# TASK 2
## LOCATION
**File/Page:** header
**Section Identifier:** <div class="logo">
- Element type: header
## CURRENT STATE
**What exists now:**
A bucket png
**Issues/Problems:**
- Incorrect logo
- Wrong size
- Wrong type
## DESIRED STATE
### Action Type: REPLACE
### Change Category: VISUAL
**What should it become:**
#### For VISUAL changes:
The logo should now point pull from this local assets/logos/jpeptics-logo.png
---
## Task 3
## LOCATION
**File/Page:** index.php
**Section Identifier:** <section class="hero">
- Element type: body
## CURRENT STATE
**What exists now:**
Just a contain
## DESIRED STATE
### Action Type: ADD
### Change Category: CONTENT
**What should it become:**
#### For VISUAL use changes:
- <h2 class="heading-2">Heading 2 - Section Headers &amp; Product Names</h2>
- Typography: center aligned
- Underneath the text and the button
#### For CONTENT changes:
- **Header 2:** RESEARCH ONLY - NOT FOR HUMAN CONSUMPTION!

## 5. VERIFICATION CHECKLIST
- [x] Changes match provided references/specifications
- [x] All requested changes completed
- [x] No out-of-scope modifications made
- [x] Functionality tested and working
- [x] Visual elements render correctly
- [x] Performance metrics acceptable
- [x] Cross-browser/device compatibility checked (if applicable)
## 6. REPORT OUT
**Files Modified:**
- index.php:150 (Hero text alignment: center to left)
- index.php:161-166 (Added heading-2 CSS styling)
- index.php:346 (Logo source updated to local path)
- index.php:369 (Added H2 warning element)

**Sections Changed:**
- Hero Section (.hero .lead) - Changed text-align from center to left
- Header Logo - Updated img src from Backblaze URL to local assets/logos/jpeptics-logo.png
- Hero Section Body - Added centered H2 "RESEARCH ONLY - NOT FOR HUMAN CONSUMPTION!" below Shop Now button

**Deviations from Request:**
- None - All changes implemented exactly as specified

**Downstream Dependencies:**
- Logo file must exist at assets/logos/jpeptics-logo.png for image to display correctly

**Additional Notes:**
- Hero text now left-aligned as requested
- Added heading-2 class with 2rem font-size, bold weight, centered alignment, and 2rem top margin
- Logo path changed from external Backblaze bucket to local assets folder
- Warning text positioned below button, maintaining centered alignment as specified

---
## TEMPLATE USAGE NOTES:

- Chavvo will complete sections 5-6 after implementation
- Reference README.md if needed.



