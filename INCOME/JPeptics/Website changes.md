---
date_created: 2025-09-28
---
10/01


---
## index.php
1. hero-banner
	1. Increase size to make it look balanced to the size of the banner.
2. in the body add "RESEARCH USE ONLY - NOT FOR HUMAN CONSUMPTION!"
3. Payment Information change to
	1. <title> "Pay with Bitcoin & Get FREE Bonuses!"<\title>
	2. <body> "CHECK OUT OUR SIMPLE, EASY TO FOLLOW INSTRUCTIONS ON HOW TO PAY IN BITCOIN BY CLICKING ON 'PAY WITH BITCOIN"<\body>
	3. <button btc-payment-info.php> Learn how!
4. COA banner should be the one found in the products-page.

### products-page.php
1. Needs the updated header
2. Delete TITLE: "Research Peptides"
3. The body needs to be left aligned.
4. Product cards 
	1. Need to have a white background
	2. The button sections need to align of both cards need to align to each other
5. The certificates of analysis section needs to lead to coa-page, with the buttons leading to the corresponding COA's
6. Needs footer

---
## header
1. Put the complete logo.
2. Get rid of the Order Now box.
## index
1. Get rid of "Research Peptides" title. 
2. Hero section: Paragraph needs to be left aligned and with paragraph breaks.<br>ex. "We believe access to research peptides shouldn’t come with uncertainty or inflated prices.<br>Reliability matters.<br>That’s why we carefully source only small controlled batches, independently test them here in U.S. labs, and every Certificate of Analysis is linked directly to the product you receive.<br>No guessing, no worrying - just verified, transparent quality in every vial.<br>Tested, Trusted, Transparent."
3. Remove "Our Products"
4. For the TZ product card add the following: <br> TITLE: "Tirzepatide 30mg"
   SUBHEADING: "Below $2/mg!"
   BODY: "At JPeptics, we don't carry dozens of products, we keep it simple. We concentrate on the two most in-demand GLP-1 peptides on the market, Tirzepatide and Retatrutide. Why?  It allows us to focus on unmatched quality control, independent U.S. testing, and full transparency-so you know exactly what you're getting. <br> Tested. Trusted. Transparent."
	1. Add two buttons. "View Details" "View COA's"
	2. Footer of the product card should say "RESEARCH USE ONLY - NOT FOR HUMAN CONSUMPTION!"
5. ## Payment Information:
	1. Fix bitcon-logo link
	2. Changes?
6. ## Certificates of Analysis (COAs)
	1. Link must now go link to coa-page.php
## products-page
1. Page description the following needs to be added: “At JPeptics, we don’t carry dozens of products, we keep it simple. We concentrate on the two most in-demand GLP-1 peptides on the market, Tirzepatide and Retatrutide. Why?<br>It allows us to focus on unmatched quality control, independent U.S. testing, and full transparency—so you know exactly what you’re getting.<br>**Tested. Trusted. Transparent.”**
2. Delete pricing in the product cards.
3. Change product card title and descriptions as follows:
	1. **Retatrutide** 20mg<br>A research peptide that activates three different hormone receptors at once—GLP-1, GIP, and glucagon—to give scientists a way to study how these systems work together. Its triple action is being investigated for potential roles in weight management, blood sugar regulation, and metabolism.
	2. **Tirzepatide** 30mg<br>A lab-made compound that can interact with two natural receptors in the body at the same time. By activating both, it helps researchers study how these pathways may work together in regulating metabolism and blood sugar.

## coa-page.php
<header>
<2 columns>
 <column Retatrutide>
 <image coa: [RT-COA-Label-JP-RITA-0925.png](https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-COA-Label-JP-RITA-0925.png) >
 <title> "Retatrutide"
 <body> "Each batch of Retatrutide comes with a complete Certificate of Analysis showing:
- Purity testing results
- Identity verification
- Potency analysis"
<button [sampleCOAs.jpg](https://f004.backblazeb2.com/file/jpeptics/COAs/sampleCOAs.jpg) >
<class="button button-gradient button-lg">
"Retatrutide - Batch TZ001"
</column Retatrutide>

<column Tirzepatide>
<image coa: [TZ-COA-Label-JP-TIRZ-0925.png.png](https://f004.backblazeb2.com/file/jpeptics/assets/TZ-0925/TZ-COA-Label-JP-TIRZ-0925.png.png)>
<title> Tirzepatide
 <body> "Each batch of Tirzepatide comes with a complete Certificate of Analysis showing:
- Purity testing results
- Identity verification
- Potency analysis"
<button: [TZ-COA-Label-JP-TIRZ-0925.png.png](https://f004.backblazeb2.com/file/jpeptics/assets/TZ-0925/TZ-COA-Label-JP-TIRZ-0925.png.png)>
<class= "button button-primary button-lg">
"Tirzepatide - Batch TZ001"
</column Tirzepatide>