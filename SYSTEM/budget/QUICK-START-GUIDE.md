---
type: budget-docs
category: guide
date: 2025-10-07
---

# Budget System - Quick Start Guide

## 🎯 What This System Does

A fully automated Obsidian-based budget system that:
- Tracks weekly income and expenses
- Auto-calculates bills due each week
- Manages two checking accounts (INCOMING & EXPENSES)
- Shows available money for debt paydown
- All updates happen in **frontmatter** - body text auto-generates

---

## 📁 File Structure

```
SYSTEM/budget/
├── dashboard.md              ← START HERE (main view)
├── accounts.md               ← Update balances here
├── bills.md                  ← View all bills
├── cash-flow.md              ← Transfer calculator
├── bills/                    ← Individual bill files
│   ├── rent.md
│   ├── electric.md
│   └── [add more bills...]
└── 2025/
    ├── 2025-W41.md          ← This week's budget
    └── templates/
        └── weekly-budget-template.md
```

---

## 🚀 Weekly Workflow (5 minutes)

### **Monday Morning:**

1. **Update Account Balances** → `accounts.md`
   - Edit frontmatter only:
   ```yaml
   incoming-balance: 703.62
   expenses-balance: 1079.16
   ```

2. **Set Weekly Budget** → `2025/2025-W41.md`
   - Edit frontmatter only:
   ```yaml
   groceries-budget: 100
   gas-budget: 60
   misc-budget: 0
   ```

3. **Check Dashboard** → `dashboard.md`
   - See bills due this week
   - See if you need to transfer money
   - See available money for debt

### **Throughout the Week:**

4. **Track Spending** → `2025/2025-W41.md`
   - Update actual spending in frontmatter:
   ```yaml
   groceries-actual: 45.32
   gas-actual: 30.00
   ```

5. **Mark Bills Paid** → Copy from auto-list, check off manually

### **End of Week:**

6. **Pay Down Debt** → Use leftover money shown in dashboard

---

## 💰 Two-Account System

### **INCOMING Account**
- **Purpose:** Direct deposit, daily debit card spending, manual bill payments
- **What comes out:** Manual bills, weekly budget spending

### **EXPENSES Account**
- **Purpose:** Auto-pay bills and minimum credit card payments only
- **What comes out:** Auto-pay bills

### **When to Transfer:**
Check `cash-flow.md` - it will tell you if EXPENSES needs money from INCOMING

---

## 📝 How to Add/Edit Bills

### **Add New Bill:**
1. Create new file: `SYSTEM/budget/bills/new-bill-name.md`
2. Copy this frontmatter:
```yaml
---
type: bill
bill-name: Bill Name
amount: 100
due-date: 15
auto-pay: false
account: INCOMING
category: Utilities
status: unpaid
---
```
3. Save - it appears everywhere automatically!

### **Edit Existing Bill:**
1. Open the bill file (e.g., `bills/rent.md`)
2. Edit frontmatter fields (amount, due-date, etc.)
3. Save - updates everywhere automatically!

---

## 🔧 Key Files Explained

### **dashboard.md** - Your Main View
**What it shows:**
- Bills due this week vs This week's budget (side by side)
- INCOMING balance minus bills
- INCOMING balance minus budget
- Next week's bills preview

**Auto-updates when you change:**
- Account balances in `accounts.md`
- Bill amounts in `bills/` folder
- Weekly budget in weekly note

---

### **accounts.md** - Account Balances
**Update weekly in frontmatter:**
```yaml
incoming-balance: 703.62      # INCOMING account balance
expenses-balance: 1079.16     # EXPENSES account balance
cc1-balance: 0                # Credit card 1 balance
cc2-balance: 0                # Credit card 2 balance
weekly-budget: 98             # Default weekly budget
```

**Also update:** Body text for your reference (not used by automation)

---

### **cash-flow.md** - Transfer Calculator
**What it shows:**
- Bills due this week by account (auto-pay vs manual)
- How much money EXPENSES needs
- How much to transfer from INCOMING to EXPENSES
- Available money for debt paydown

**No manual input needed** - all auto-calculated!

---

### **Weekly Budget Note** (e.g., `2025-W41.md`)
**Update in frontmatter:**
```yaml
groceries-budget: 100
groceries-actual: 0
gas-budget: 60
gas-actual: 0
misc-budget: 0
misc-actual: 0
```

**Auto-displays:**
- Budget vs actual for each category
- Remaining budget
- Over/under budget status

---

## 🎨 What's Automated

✅ **Bills due this week** - Calculated based on today's date
✅ **Bills by account** - Auto-sorted by INCOMING vs EXPENSES
✅ **Weekly budget totals** - Auto-summed from categories
✅ **Money available** - Auto-calculated from balances
✅ **Transfer recommendations** - Auto-calculated
✅ **Next week preview** - Auto-shows upcoming bills

---

## 📊 Understanding the Dashboard

### **Top Section: This Week**
```
┌─────────────────────────┬──────────────────────────┐
│ Bills Due This Week     │ This Week's Budget       │
├─────────────────────────┼──────────────────────────┤
│ Electric: $446.01       │ Groceries: $100.00       │
│ xFinity: $79.00         │ Gas: $60.00              │
│ Total: $525.01          │ Total: $160.00           │
└─────────────────────────┴──────────────────────────┘
```

### **Bottom Section: Money Left**
```
┌─────────────────────────┬──────────────────────────┐
│ After This Week's Bills │ After This Week's Budget │
├─────────────────────────┼──────────────────────────┤
│ INCOMING: $703.62       │ INCOMING: $703.62        │
│ - Bills: $525.01        │ - Budget: $160.00        │
│ = $178.61               │ = $543.62                │
└─────────────────────────┴──────────────────────────┘
```

**Interpretation:**
- Left: If you pay all bills, you'll have $178.61 left
- Right: If you spend full budget, you'll have $543.62 left

---

## 🔮 Future Automation (Not Yet Built)

### **Phase 2: Toggl Integration**
- Auto-sync hours worked from Toggl
- Calculate weekly pay automatically
- No more manual income entry

### **Phase 3: Bank APIs**
- Real-time account balances
- Auto-detect bill payments
- Transaction categorization

### **Phase 4: Advanced Features**
- Debt payoff calculators (avalanche/snowball)
- Spending trends and analytics
- Bill payment reminders/notifications

---

## ❓ Troubleshooting

### **Bills not showing in dashboard?**
1. Check bill file has `type: bill` in frontmatter
2. Verify `due-date` is a number (1-31), not text
3. Make sure file is in `SYSTEM/budget/bills/` folder

### **Balances not updating?**
1. Make sure you updated **frontmatter**, not body text
2. Reload the note in Obsidian
3. Check spelling: `incoming-balance` not `incoming_balance`

### **Weekly budget not showing?**
1. Check weekly note has `status: active` in frontmatter
2. Only one weekly note should be active at a time
3. Budget fields must be numbers, not text

### **DataviewJS not rendering?**
1. Settings → Community Plugins → Dataview
2. Enable "Enable JavaScript Queries"
3. Enable "Enable Inline JavaScript Queries"
4. Restart Obsidian

---

## 🎯 Pro Tips

1. **Update balances every Monday** - Makes the week easier
2. **Set budget at start of week** - Know your limits upfront
3. **Check dashboard daily** - Quick 30-second money check
4. **Use cash-flow.md before payday** - Plan transfers ahead
5. **Review weekly note Friday** - See if you stayed on budget
6. **Copy bills to manual tracking** - Check them off as paid

---

## 📞 Need Help?

**Common Tasks:**
- Add bill → Create file in `bills/` folder
- Update balance → Edit `accounts.md` frontmatter
- Set weekly budget → Edit weekly note frontmatter
- Check money available → Open `dashboard.md`
- Plan transfer → Open `cash-flow.md`

**Remember:** All data input happens in **frontmatter only**. The body text is auto-generated for display.

---

*System created: 2025-10-07*
*Last updated: 2025-10-07*
*Version: 1.0 - MVP Complete*
