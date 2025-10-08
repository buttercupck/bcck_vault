---
type: budget-helper
category: cash-flow
---

# Cash Flow Manager

**Purpose:** Calculate if you need to move money between INCOMING and EXPENSES accounts.

---

## 💰 Current Account Balances

**Auto-pulled from [[SYSTEM/budget/accounts|accounts.md]]:**

```dataviewjs
const accountsPage = dv.page("SYSTEM/budget/accounts");
const incomingBalance = accountsPage["incoming-balance"] || 0;
const expensesBalance = accountsPage["expenses-balance"] || 0;

dv.paragraph(`- **INCOMING Balance:** $${incomingBalance.toFixed(2)}`);
dv.paragraph(`- **EXPENSES Balance:** $${expensesBalance.toFixed(2)}`);
dv.paragraph(`- **Total Checking:** $${(incomingBalance + expensesBalance).toFixed(2)}`);
```

---

## 📊 Bills Due This Week by Account

### Auto-Pay Bills (EXPENSES Account)

```dataviewjs
const today = dv.date("today");
const currentDay = today.day;
const startOfWeek = currentDay - (currentDay % 7) + 1;
const endOfWeek = startOfWeek + 6;

// Query auto-pay bills due this week
const autoPayBills = dv.pages('"SYSTEM/budget/bills"')
    .where(p => p.type === "bill")
    .where(b => b["auto-pay"] === true)
    .where(b => b["due-date"] >= startOfWeek && b["due-date"] <= endOfWeek)
    .sort(p => p["due-date"], 'asc');

if (autoPayBills.length === 0) {
    dv.paragraph("✅ No auto-pay bills due this week");
} else {
    let total = 0;
    for (let bill of autoPayBills) {
        const name = bill["bill-name"];
        const amount = bill.amount || 0;
        const dueDate = bill["due-date"];
        total += amount;
        dv.paragraph(`- **${name}** - $${amount.toFixed(2)} (Due: Day ${dueDate})`);
    }
    dv.paragraph(`\n**Total Auto-Pay This Week:** $${total.toFixed(2)}`);
}
```

### Manual Bills (INCOMING Account)

```dataviewjs
const today = dv.date("today");
const currentDay = today.day;
const startOfWeek = currentDay - (currentDay % 7) + 1;
const endOfWeek = startOfWeek + 6;

// Query manual bills due this week
const manualBills = dv.pages('"SYSTEM/budget/bills"')
    .where(p => p.type === "bill")
    .where(b => b["auto-pay"] === false)
    .where(b => b["due-date"] >= startOfWeek && b["due-date"] <= endOfWeek)
    .sort(p => p["due-date"], 'asc');

if (manualBills.length === 0) {
    dv.paragraph("✅ No manual bills due this week");
} else {
    let total = 0;
    for (let bill of manualBills) {
        const name = bill["bill-name"];
        const amount = bill.amount || 0;
        const dueDate = bill["due-date"];
        total += amount;
        dv.paragraph(`- **${name}** - $${amount.toFixed(2)} (Due: Day ${dueDate})`);
    }
    dv.paragraph(`\n**Total Manual Bills This Week:** $${total.toFixed(2)}`);
}
```

---

## 🔄 Transfer Calculator (Auto-Calculated)

```dataviewjs
// Get account balances
const accountsPage = dv.page("SYSTEM/budget/accounts");
const incomingBalance = accountsPage["incoming-balance"] || 0;
const expensesBalance = accountsPage["expenses-balance"] || 0;

// Get this week's date range
const today = dv.date("today");
const currentDay = today.day;
const startOfWeek = currentDay - (currentDay % 7) + 1;
const endOfWeek = startOfWeek + 6;

// Calculate auto-pay bills total
const autoPayBills = dv.pages('"SYSTEM/budget/bills"')
    .where(p => p.type === "bill")
    .where(b => b["auto-pay"] === true)
    .where(b => b["due-date"] >= startOfWeek && b["due-date"] <= endOfWeek);

let autoPayTotal = 0;
for (let bill of autoPayBills) {
    autoPayTotal += bill.amount || 0;
}

// Calculate manual bills total
const manualBills = dv.pages('"SYSTEM/budget/bills"')
    .where(p => p.type === "bill")
    .where(b => b["auto-pay"] === false)
    .where(b => b["due-date"] >= startOfWeek && b["due-date"] <= endOfWeek);

let manualTotal = 0;
for (let bill of manualBills) {
    manualTotal += bill.amount || 0;
}

// Calculate EXPENSES status
const expensesAfterBills = expensesBalance - autoPayTotal;
const expensesStatus = expensesAfterBills >= 0 ? "✅ Safe" : "⚠️ NEED TRANSFER";

dv.header(3, "EXPENSES Account Check");
dv.paragraph(`\`\`\`
EXPENSES Current Balance:     $${expensesBalance.toFixed(2)}
- Auto-Pay Bills Due:         $${autoPayTotal.toFixed(2)}
────────────────────────────────────
= Remaining After Bills:      $${expensesAfterBills.toFixed(2)}
\`\`\``);
dv.paragraph(`**Status:** ${expensesStatus}`);

// Get weekly budget from accounts
const weeklyBudget = accountsPage["weekly-budget"] || 100;
const incomingAfterBills = incomingBalance - manualTotal - weeklyBudget;

dv.paragraph("---");
dv.header(3, "INCOMING Account Check");
dv.paragraph(`\`\`\`
INCOMING Current Balance:     $${incomingBalance.toFixed(2)}
- Manual Bills Due:           $${manualTotal.toFixed(2)}
- Weekly Budget:              $${weeklyBudget.toFixed(2)}
────────────────────────────────────
= Available for Debt:         $${incomingAfterBills.toFixed(2)}
\`\`\``);

// Recommended action
dv.paragraph("---");
dv.header(3, "🎯 Recommended Action");

if (expensesAfterBills < 0) {
    const transferNeeded = Math.abs(expensesAfterBills);
    dv.paragraph(`⚠️ **TRANSFER NEEDED:** Move **$${transferNeeded.toFixed(2)}** from INCOMING to EXPENSES`);
    dv.paragraph(`After transfer, INCOMING will have: $${(incomingBalance - transferNeeded - manualTotal - weeklyBudget).toFixed(2)} for debt`);
} else {
    dv.paragraph(`✅ **No transfer needed** - EXPENSES has enough`);
    if (incomingAfterBills > 0) {
        dv.paragraph(`💰 Available for extra debt payment: **$${incomingAfterBills.toFixed(2)}**`);
    }
}
```

---

## 📝 Weekly Workflow

1. **Update account balances** at top of this page
2. **Check auto-pay total** - Does EXPENSES have enough?
3. **Transfer if needed** - Move money from INCOMING to EXPENSES
4. **Pay manual bills** from INCOMING
5. **Allocate weekly budget** from INCOMING
6. **Send leftover to debt** - Whatever remains in INCOMING

---

## Future Automation

**Phase 2: Auto-Balance Checker**
- Alert when EXPENSES will be short
- Calculate optimal transfer amount
- Track transfer history

**Phase 3: Bank Integration**
- Auto-detect when bills clear
- Real-time balance updates
- Auto-flag insufficient funds

