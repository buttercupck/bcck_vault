---
request_id: CR-20251001
date_created: 2025-10-01
status: COMPLETED
client: JPeptics
---

#### REFERENCES
**Documentation:**
- [ ] [[Product Photo Naming Conventions]]
- [ ] [[Branding]] (style guide)
- [ ] [[Website File Tree]]
### TASK 1
#### LOCATION
**File/Page:** index.php
**Section Identifier:** <div class="payment-info",  #coa-section , div.product-grid>
- Element type: card
---
#### DESIRED STATE
DELETE
--

### TASK 2
#### LOCATION
**File/Page:** index.php
**Section Identifier:** <section class="hero">
- Element type: hero-banner, card

---
## CURRENT STATE
**What exists now:**
Paragraph is left aligned, semi-medium font size. Small text at the bottom.

**Issues/Problems:**
- Hard to read and not convening authority because text. Font should increase, and centered with appropriate spacing.
- Bottom text should be larger for emphasis. 

---

## DESIRED STATE

### Action Type: REPLACE | ADJUST
### Change Category: VISUAL | FUNCTIONAL | CONTENT 

---

**What should it become:**

#### For VISUAL changes:
Use  <class="button button-secondary button-lg"> 

#### For FUNCTIONAL changes:
- Add Button that leads to product-page

#### For CONTENT changes:
- **Buttons:** "Shop Now"

---

## 5. VERIFICATION CHECKLIST
Before marking complete, confirm:
- [x] Change matches References cited in section 2
- [x] Stays within scope of request (no scope creep)
- [x] Meets specifications in Desired State
- [x] Assets load correctly (images, links, files)
- [x] No broken functionality introduced
- [x] Responsive on mobile/desktop (if applicable)

---

## 6. REPORT OUT
**Files Modified:**
- index.php:143-159 (CSS styling for hero section)
- index.php:357-363 (Hero section HTML)
- index.php:355-368 (Deleted product-grid, payment-info, and coa-info sections)

**Sections Changed:**
- Hero Section - Increased font size from 1.25rem to 1.75rem, centered text, added emphasis styling for bottom text (2rem, bold), and added "Shop Now" button with btn-secondary btn-lg classes
- Product Grid Section - Completely removed product cards for Retatrutide and Tirzepatide
- Payment Info Section - Completely removed Bitcoin payment information card
- COA Info Section - Completely removed Certificates of Analysis card

**Deviations from Request:**
- None - All changes implemented exactly as specified

**Downstream Dependencies:**
- None - Changes are isolated to index.php homepage

**Additional Notes:**
- Hero text now has better readability with larger font (1.75rem vs 1.25rem)
- "Tested, Trusted, Transparent" emphasis text is now 2rem and bold for maximum impact
- Shop Now button uses button-secondary (magenta) and button-lg classes as specified
- Button links to products-page.php
- Removed all inline style="text-align: left;" to allow centered text to work properly
- Product Overview section now empty but structure maintained for future use if needed

---

## TEMPLATE USAGE NOTES:
- Copy this template for each change request
- Fill in sections 1-4 before submitting to Chavvo
- Chavvo will complete sections 5-6 after implementation
- Use your natural Website changes.md style in section 4 - mix numbered lists, bullets, and inline HTML
- Reference asset naming conventions from README.md
- Link to actual Backblaze URLs for images when available
```
