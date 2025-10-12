---
template-type: task-request
version: 1.0
created: 2025-10-04
optimized-for: speed + clarity
---
# Task 1 - Changing order quantity

## Tasks
1. Change the maximum order quantity to 2 on both product pages.
   - Add "2" to the quantity and it should be the maximum amount that the customer can order.
2. Change order-page if needed since it was coded to be max 1 quantity
## Files
- rt-product-page.php 
- tz-product-page.php
- order-form.php

## Done When
- [x] Customer can order 1 or 2 products.
- [x] The correct order quantity is shown in the email confirmations
---
# Task 2 - Order Form Phone Number

## Tasks
1. In the order-form phone number should NOT be required.
   - Should still have a space for a phone number to be inputted but can be empty to submit order.

## Files
- order-page.php

## Done When
- [x] Customer can submit order without needing to input phone number

---
# Task 3 - Bitcoin Promo Subheading

## Tasks
1. Add "AND GET:" as a subheading to "PAY WITH BITCOIN"
2. Must be center aligned and underneath the title.

## Files
- payment-received.php
- assets/css/styles.css

## Assets/Dependencies
- Left Column: Bitcoin Promo

## Done When
- [x] You the customer can read "PAY WITH BITCOIN AND GET:"

---
# Task Request - Add Quality Statement to Nav Bar

## Tasks
1. Add a button to the nav bar called "Transparency".
   - When clicked the button takes you to the pdf asset.
   - Button should be on the right hand side of the "Products" button. 
## Files
- partials/header.php

## Assets/Dependencies
-  assets/quality_statement.pdf

## Done When
- [x] Customer can click on the "Transparency" button to read the PDF.

---

## Completion Report
**Modified:**
- rt-product-page.php:33-37 - Added quantity option "2" to dropdown, updated help text to "Maximum 2 quantity per order"
- tz-product-page.php:33-37 - Added quantity option "2" to dropdown, updated help text to "Maximum 2 quantity per order"
- order-form.php:227-228 - Removed `required` attribute and asterisk from phone number field (now optional)
- payment-received.php:47-48 - Added "AND GET:" subheading below "PAY WITH BITCOIN", fixed malformed HTML tag
- partials/header.php:36 - Added "Transparency" nav link pointing to `/assets/quality_statement.pdf` (opens in new tab)

**Created:**
- None (all modifications to existing files)

**Issues/Deviations:**
- Minor HTML fix: Corrected malformed `<ul h4 style="...">` tag in payment-received.php to proper semantic HTML with separate `<h4>` and `<ul>` tags. Improves code quality without affecting visual appearance.
- Email confirmation logic in order-form.php already handles variable quantity correctly - no changes needed.

---
*Completed by Chavvo - 2025-10-10*

