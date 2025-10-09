**Budget System Intent:**

I need an Obsidian-based budget system that tracks my finances on a weekly pay schedule. The system should:

1. **Track my income** by automatically syncing my hours worked from Toggl, multiplying by my hourly rate to calculate weekly pay
2. **Organize bills by week** so I can see which bills are due each week and mark them as paid. Also making sure I am working enough to cover bills, and budget.
3. **Calculate leftover funds** after each paycheck by subtracting bills and weekly budget expenses (groceries, gas, etc.) from my weekly pay
4. **Direct extra money to debt paydown** - any money left over after bills and budget automatically goes to credit card payments
5. **Visualize debt progress** by tracking credit card balances month-over-month and showing how much debt I've paid down
6. **Manage multiple accounts** including credit cards and 2 checking accounts
7. **Reset monthly** with a template system so I can easily create a new budget each month with bills distributed across the appropriate weeks

**Core workflow**: Get paid weekly → Pay this week's bills → Spend weekly budget → Send whatever's left to credit cards → Track progress monthly

The system should be visual, easy to update, and show me at a glance where my money needs to go each week, and how much progress I'm making on debt elimination.

---

## ✅ MVP COMPLETE - System Ready!

**Start Here:** [[SYSTEM/budget/dashboard|📊 Budget Dashboard]]

### What's Working Now (Manual Entry)

✅ **Weekly Budget System**
- Track income, bills, and spending by week
- Calculate leftover money for debt paydown
- Quick "can I afford this?" decision helper

✅ **Two-Account System**
- **EXPENSES Account:** All monthly bills & minimum credit card payments (auto-pay)
- **INCOMING Account:** Direct deposit, daily debit card spending, and manual bill payments
- Auto-calculates if you need to transfer money between accounts
- Shows available money for debt paydown

✅ **Bill Management**
- Auto-calculated bills due this week
- Organized by account (EXPENSES vs INCOMING)
- Automatic totals and transfer recommendations

### Quick Start Guide

1. **Set Up Your Bills** → [[SYSTEM/budget/bills|bills.md]]
   - Add all recurring bills with amounts and due dates
   - Assign to appropriate week (1-5)

2. **Update Account Balances** → [[SYSTEM/budget/accounts|accounts.md]]
   - Enter current checking balances
   - Enter credit card balances and limits
   - Update monthly debt snapshot

3. **Fill Out This Week** → [[SYSTEM/budget/2025/2025-W41|2025-W41.md]]
   - Enter hours worked and hourly rate
   - Copy this week's bills from bills.md
   - Set weekly budget amounts
   - Calculate leftover for debt payment

4. **Use the Dashboard** → [[SYSTEM/budget/dashboard|dashboard.md]]
   - See current week at a glance
   - View recent weeks
   - Track monthly progress

### Future Automation Roadmap

**Phase 2: Toggl Integration** (Next)
- Auto-sync hours worked
- Auto-calculate weekly pay
- Show "hours needed" per bill

**Phase 3: Smart Bill Distribution**
- Auto-populate bills by week
- Payment reminders
- Payment history tracking

**Phase 4: Debt Optimization**
- Avalanche/snowball calculators
- Debt-free date projections
- Visual progress tracking

**Phase 5: Bank APIs**
- Real-time balance sync
- Transaction categorization
- Automated account reconciliation

### System Structure

```
SYSTEM/budget/
├── README.md (this file - planning & docs)
├── dashboard.md (main entry point)
├── bills.md (master bill list)
├── accounts.md (balance tracking)
└── 2025/
    ├── 2025-W41.md (this week)
    └── templates/
        └── weekly-budget-template.md
```

**All files are automation-ready:**
- Structured frontmatter for Dataview
- API integration hooks in place
- Metadata prepared for future features