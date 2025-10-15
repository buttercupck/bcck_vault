---
template-type: task-request
version: 1.0
created: 2025-10-04
optimized-for: speed + clarity
---
## Task 1: Fix index.php Footer Whitespace Issue
1. Fix index.php Footer Whitespace Issue
   - Huge whitespace appearing underneath the footer on index.php ONLY
   - Other pages (products-page.php, tz-product-page.php, rt-product-page.php) display footer correctly
   - Issue persists after multiple fix attempts
## Files
- ~/Users/itza/Desktop/JPeptics/partials/footer.php
-  ~/Users/itza/Desktop/JPeptics/index.php
## Assets/Dependencies
- Prerequisite: Check for margin/padding issues specific to hero section, Check if hero section has a min-height or height property causing the issue

## Done When
- [ ] There is no visible above or below the footer in index.php
- [ ] When the index.php footer is visibly identical to the other pages

---

## Notes
**Attempts Made:**

1. **Attempt 1: Added Flexbox to Body**
   - Added `display: flex`, `flex-direction: column`, `min-height: 100vh` to body
   - Kept `flex: 1` on main element
   - Result: ❌ Issue persisted

2. **Attempt 2: Changed Main Min-Height**
   - Removed flexbox from body
   - Changed main to `min-height: calc(100vh - 200px)`
   - Result: ❌ Issue persisted

---
## Completion Report
**Modified:**
- file.ext:123 - [what changed]

**Created:**
- new-file.ext - [purpose]

**Issues/Deviations:**
- [Anything that couldn't be done as requested and why]

---
*Completed by Chavvo - [date]*

---
---
ask Request - [Brief Title]

## Task 2: Mobile Responsiveness & Polish Issues
1. **Mobile Navigation Missing**
   - No nav buttons showing on mobile for Home and Products pages
   - Need to add mobile menu/hamburger

2. **Index Page - Mobile**
   - Hero text is crunched up and slim
   - Needs better text sizing and spacing for mobile viewports
3. **Payment-Received Page**
   - BAC Water photo link is broken
4. **Product Pages - Gallery Issues**
   - Product image gallery not centered
   - COA photo not centered

## Files
-  /JPeptics/index.php
- /JPeptics/payment-received.php
- /JPeptics/rt-product-page.php
- /JPeptics/tz-product-page.php
- /assets/css/styles.css

## Assets/Dependencies
- Image: /assets/products/BACT-SINGLE-VIAL-A.PNG

## Done When
- [ ] All changes have been made
- [ ] All changes are aligned with original request
- [ ] Specific outcome 3 redirects correctly

---

## Notes
Just make sure it's mobile optimized since thats likely where all of our customers will be from.

---

## Completion Report
**Modified:**
- file.ext:123 - [what changed]

**Created:**
- new-file.ext - [purpose]

**Issues/Deviations:**
- [Anything that couldn't be done as requested and why]

---
*Completed by Chavvo - [date]*
