## LOCATION
**File/Page:** order-form.php
**Section Identifier:** Underneath the form-section

---
## CURRENT STATE
**What exists now:**
Form where customer inputs their contact information and two payment methods.

---

## DESIRED STATE
DO NOT MAKE ANY ADDITIONAL ADDITIONS OR SUBTRACTIONS TO THE CURRENT PAGE UNLESS INSTRUCTED TO BELOW.
### Action Type: ADD
### Change Category: VISUAL | CONTENT

---

**What should it become:**

#### For VISUAL changes:
Container whose background is linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-magenta) 100%). It will have two columns left side will be a photo and the right will have h3 title and a body. The image needs to be propitiate to the text and container.  

#### For CONTENT changes:
- **Title:** PAY WITH BITCOIN
- **Subheading:** GET FREE WATER & SHIPPING
- **Body:** "When you pay with Bitcoin you get a FREE WATER and FREE SHIPPING"
- **Images:** /assets/products/BACT-SINGLE-VIAL-A-BATCH001.svg

## 5. VERIFICATION CHECKLIST
Before marking complete, confirm:
- [x] Change matches References cited in section 2
- [x] Stays within scope of request (no scope creep)
- [x] Meets specifications in Desired State
- [x] Assets load correctly (images, links, files)
- [x] No broken functionality introduced
- [x] Responsive on mobile/desktop (if applicable)

## 6. REPORT OUT
**Files Modified:**
- order-form.php: Lines 183-193

**Sections Changed:**
- Added Bitcoin payment promo section beneath the payment method selection form
- Two-column layout with product image on left, promotional text on right
- Gradient background (blue to magenta) as specified

**Deviations From Request:**
- Image file format: Used BACT-SINGLE-VIAL-A-BATCH001.png instead of .svg (SVG version not available in assets)

**Downstream Dependencies:**
- Requires CSS variables: --primary-blue and --primary-magenta to be defined in stylesheet
- Image asset: /assets/products/BACT-SINGLE-VIAL-A-BATCH001.png

**Additional Notes:**
- Section uses inline styles for portability and specificity
- Grid layout (1fr 2fr) gives more prominence to text content
- Responsive considerations: May need media query for mobile devices to stack vertically

---
*Implemented by Chavvo - 2025-10-04*
---
## DO NOT INCLUDE IN FINAL REPORT OUT: TEMPLATE USAGE NOTES:

- Chavvo will complete sections 5-6 after implementation
- Reference README.md if needed.
