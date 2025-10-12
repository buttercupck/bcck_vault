---
template-type: task-request
version: 1.0
created: 2025-10-04
optimized-for: speed + clarity
---
# Task Request - Change customer confirmation email

## Tasks
1. In the first div following the first paragraph add the following "A representative will reach out shortly to guide you through the payment process."
2. Add the following below the order summary and shipping details
   - "💳 Payment Options

Because payment processing for peptides can be tricky, Bitcoin is our preferred method.

We can also accept Cash App or Venmo in select cases, but we heavily reward Bitcoin payments with:

💥 Free 30mL Hospira BAC Water
      ($20 value!)
💥 Free Shipping
💥 $10 Off Your Order

⸻

💡 Need Help Getting Started?

No worries — it’s easier than you might think! We’ve made Bitcoin super simple by making a step-by-step guide that walks you through buying and sending Bitcoin using Cash App, Venmo, or PayPal.

If you’d like, we can personally help you thru the process from start to finish. Just let us know — we’re happy to help!

⸻

Once payment is confirmed, your order will be picked, packed, and shipped quickly, and you’ll get tracking right away.

For any questions or help, email us at JPeptics@gmail.com — we respond fast! 

⸻

Thank you again for choosing JPeptics
Tested. Trusted. Transparent.

-JP
JPeptics Support"

## Files
- order-form.php

## Done When
- [x] The customer clicks order form and receives the confirmation email which thanks them for their order, see the payment options, know what they get when they pay for bitcoin, if they need help, they know where they can turn and what to expect when they make payment.

---

## Notes
Keep the same formatting as it shows above. Do not add any additional verbiage.

---

## Completion Report
**Modified:**
- order-form.php:72 - Added representative contact message after opening paragraph
- order-form.php:93-113 - Added comprehensive payment options section with Bitcoin incentives, help guidance, and expectations

**Created:**
- None (all modifications to existing email template)

**Issues/Deviations:**
- Removed duplicate closing text that was already present in the original template
- Used HTML `<hr>` tags for divider lines (⸻) for better email rendering
- Used `&nbsp;` for indentation on BAC Water value line for proper HTML formatting

---
*Completed by Chavvo - 2025-10-10*

**For Chavvo:**
1. Read the entire request before starting work
2. Check that all Assets/Dependencies exist before coding
3. If something is ambiguous, ask first - don't guess
4. Mark "Done When" checkboxes as you complete them
5. Fill out Completion Report with actual line numbers and deviations only
6. If you need to make judgment calls beyond the scope, do it - just document it in Issues/Deviations

**Philosophy:**
This template optimizes for speed and clarity. Trust is assumed. Document deviations, not confirmations.
