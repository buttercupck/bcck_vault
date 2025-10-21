
**7 Required Pages Analysis**

### **1. index.php (Homepage)**

✅ **Status:** Framework created, needs finalization

- Hero section with brand messaging:
	- "We believe access to research peptides shouldn’t come with uncertainty or inflated prices. Reliability matters. That’s why we carefully source only small controlled batches, independently test them here in U.S. labs, and every Certificate of Analysis is linked directly to the product you receive.  No guessing, no worrying - just verified, transparent quality in every vial.  Tested, Trusted, Transparent."
- Product overview cards
	- Use product vile image paths:
		- /var/www/d1517907-f8a0-4746-a7d5-21ae0ed43082/public_html/jpeps/assets/products/RZ/RT-Vile.png
		-  `/var/www/d1517907-f8a0-4746-a7d5-21ae0ed43082/public_html/jpeps/assets/products/TZ/TZ-Vile.jpeg`
- Payment information section needs to include:
	- "We accept Bitcoin only as the form of payment. For the easiest checkout , our preferred app is CashApp."
	- Use the bitcoin and cashapp logo paths:
	  - `/var/www/d1517907-f8a0-4746-a7d5-21ae0ed43082/public_html/jpeps/assets/payment/bitcoin-logo.png`
	  -  `/var/www/d1517907-f8a0-4746-a7d5-21ae0ed43082/public_html/jpeps/assets/payment/cashapp-logo.svg`
	  - Button the leads to the btc-payment-info.php page.
- Certificates of Analysis (COAs)
	- COAs are independent lab reports that verify the identity, purity, and quality of each batch we supply. We publish them so researchers can see the exact testing data tied to their product’s lot number. This level of transparency ensures trust, consistency, and confidence in every vial.
	- It should have a button to products-page.php COA section

### **2. order-form.php (Manual Order Collection)**

📝 **New requirement based on your layout:**

- Customer information collection
- Product selection overview
- Shipping address
- Button that leads them to btc-payment-info.php 

### **3. products-page.php (Product Overview)**

📝 **Product listing page:**

- Both Tirzepatide and Retatrutide in grid
- Quick "Add to Cart" functionality
- What's in the box sections with the following assets
	- /var/www/d1517907-f8a0-4746-a7d5-21ae0ed43082/public_html/jpeps/assets/products/BACT-SINGLE-VIAL-A-BATCH001.jpeg
- Lastly include a list of the Certificates of Analysis

### **4. tz-product-page.php (Tirzepatide Detail)**

📝 **Individual product page:**

- Detailed product information:
	- "A lab-made compound that can interact with two natural receptors in the body at the same time. By activating both, it helps researchers study how these pathways may work together in regulating metabolism and blood sugar"
- "What's in the Box" section
- COA information for specific batch
- Add to cart with quantity selection
	- Once "Add to Cart" is clicked should lead them to btc-payment-info.php
- Drop down to choose the pack amounts with the corresponding pricing
	- 3 pack - $179
	- 6 pack - $339
	- 10 pack - $529

### **5. rz-product-page.php (Retatrutide Detail)**

📝 **Individual product page:**

- Same structure as Tirzepatide
- Blue color theming
- Include this for product description
	- "Retatrutide is a research peptide that activates three different hormone receptors at once—GLP-1, GIP, and glucagon—to give scientists a way to study how these systems work together. Its triple action is being investigated for potential roles in weight management, blood sugar regulation, and metabolism."

### **6. btc-payment-info.php (Bitcoin Education)**

🤔 **Need wireframe - Bitcoin education page:**

- How to set up CashApp account
- Step-by-step Bitcoin purchasing guide
- Payment process explanation
- Button that leads to btc-trans-verification.php

### **7. btc-trans-verification.php (Transaction Verification)**

🤔 **Need wireframe - Transaction confirmation:**

-  Bitcoin transaction ID submission
- After the transaction ID is submitted there should be an order confirmation details


---

## 🎨 **Bitcoin Payment Pages Wireframes**

### **btc-payment-info.php Wireframe:**

```
┌─────────────────────────────────────────────────────────┐
│ [Header with JPeptics Logo and Navigation]              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│           🔰 Bitcoin Payment Guide                      │
│                                                         │
│  Step 1: Download CashApp                               │
│  [CashApp Logo] Download from App Store/Google Play    │
│                                                         │
│  Step 2: Set Up Bitcoin                                 │
│  □ Create account                                       │
│  □ Verify identity                                      │
│  □ Add payment method                                   │
│  □ Enable Bitcoin purchases                             │
│                                                         │
│  Step 3: Purchase Bitcoin                               │
│  □ Buy amount needed for your order                     │
│  □ Wait for Bitcoin to be available                     │
│                                                         │
│  Step 4: Send Payment                                   │
│  □ Copy our Bitcoin address                             │
│  □ Send exact amount                                    │
│  □ Save transaction ID                                  │
│                                                         │
│  [Video Tutorial] [FAQ Section] [Contact Support]      │
│                                                         │
│           [Continue to Checkout] Button                 │
└─────────────────────────────────────────────────────────┘
```

### **btc-trans-verification.php Wireframe:**

```
┌─────────────────────────────────────────────────────────┐
│ [Header with JPeptics Logo and Navigation]              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│        ✅ Complete Your Bitcoin Payment                 │
│                                                         │
│  Order Summary:                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1x Tirzepatide 30mg - 10 pack        $529      │   │
│  │ Shipping                              FREE      │   │
│  │ ─────────────────────────────────────────────   │   │
│  │ Total                                 $529      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Bitcoin Payment Address:                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh    │   │
│  │                                    [Copy] 📋   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Amount to Send: 0.0089 BTC ($529)                     │
│                                                         │
│  Transaction ID Submission:                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Enter Bitcoin Transaction ID]                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ⚠️ Important: Send exact amount to avoid delays       │
│                                                         │
│           [Submit Transaction] Button                   │
│                                                         │
│  After submission:                                      │
│  • We'll verify your payment (1-6 hours)              │
│  • You'll receive email confirmation                   │
│  • Order ships within 1-2 business days               │
└─────────────────────────────────────────────────────────┘
```

---

## ❓ **Questions Before We Begin:**

1. **Bitcoin Address:** Do you have a specific Bitcoin wallet address for receiving payments, or should I create a placeholder?
    
2. **Email Notifications:** Where should order submissions be sent for manual processing? Send to JPeptics@gmail.com the transaction ID also needs to be included in the email.
    
3. **Order Numbers:** How do you want to generate order numbers? (Date-based, sequential, random? Date-based.
    
4. **Shipping Information:** Do you need specific shipping options, or is everything standard shipping?
    
5. **Product Quantities:** Are there minimum/maximum order quantities I should enforce? Max 1 quantity
    
6. **Inventory Checking:** Should I disable ordering if you're out of stock, or just note it in the admin email? TBD
    
7. **CashApp Integration:** Do you have specific CashApp tutorial videos/links you want to include?
    
8. **Customer Communication:** After order submission, should customers receive an auto-confirmation email? Yes they should.
    

## 🚀 **Ready to Start?**

Once you answer these questions, I can begin building immediately. The first deliverable will be the complete homepage and product pages (Day 1), so you can see the design and functionality working right away.

Should I proceed with creating the first set of pages using placeholder information that we can update later?