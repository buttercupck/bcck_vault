---
type: budget-dashboard
category: overview
---

# Budget Dashboard

**Quick Links:**
- [[SYSTEM/budget/bills|📋 Bills Master List]]
- [[SYSTEM/budget/accounts|💳 Account Balances]]
- [[SYSTEM/budget/2025/2025-W41|📅 This Week's Budget]]

---

## This Week at a Glance

```dataviewjs
// Get today's date
const today = dv.date("today");
const currentDay = today.day;
const currentMonth = today.month;
const currentYear = today.year;

// Calculate the current week of the month (1-5)
const weekOfMonth = Math.ceil(currentDay / 7);
const startOfWeek = currentDay - (currentDay % 7) + 1;
const endOfWeek = startOfWeek + 6;

// Get account balances
const accountsPage = dv.page("SYSTEM/budget/accounts");
const incomingBalance = accountsPage["incoming-balance"] || 0;

// Get current week's budget
const currentWeekNote = dv.pages('"SYSTEM/budget/2025"')
    .where(p => p.type === "weekly-budget" && p.status === "active")
    .sort(p => p.week, 'desc')
    .first();

const groceriesBudget = currentWeekNote ? (currentWeekNote["groceries-budget"] || 0) : 0;
const gasBudget = currentWeekNote ? (currentWeekNote["gas-budget"] || 0) : 0;
const miscBudget = currentWeekNote ? (currentWeekNote["misc-budget"] || 0) : 0;
const totalWeeklyBudget = groceriesBudget + gasBudget + miscBudget;

// Query bills due this week
const bills = dv.pages('"SYSTEM/budget/bills"')
    .where(p => p.type === "bill")
    .sort(p => p["due-date"], 'asc');

const billsDueThisWeek = bills.where(b => {
    const dueDate = b["due-date"];
    return dueDate >= startOfWeek && dueDate <= endOfWeek;
});

let billsTotal = 0;
for (let bill of billsDueThisWeek) {
    billsTotal += bill.amount || 0;
}

// Query bills due NEXT week
const nextWeekStart = endOfWeek + 1;
const nextWeekEnd = nextWeekStart + 6;
const nextWeekBills = bills.where(b => {
    const dueDate = b["due-date"];
    return dueDate >= nextWeekStart && dueDate <= Math.min(nextWeekEnd, 31);
});

let nextWeekTotal = 0;
for (let bill of nextWeekBills) {
    nextWeekTotal += bill.amount || 0;
}

// Create layout
dv.paragraph(`**Week ${weekOfMonth} - ${currentMonth}/${currentYear}** (Days ${startOfWeek}-${endOfWeek})`);
dv.paragraph("---");

// Build bills list
let billsListItems = [];
if (billsDueThisWeek.length === 0) {
    billsListItems.push("✅ No bills due");
} else {
    for (let bill of billsDueThisWeek) {
        const name = bill["bill-name"];
        const amount = bill.amount || 0;
        const dueDate = bill["due-date"];
        billsListItems.push(`${name}: $${amount.toFixed(2)} (Day ${dueDate})`);
    }
}

// Build budget list
let budgetListItems = [];
if (groceriesBudget > 0) budgetListItems.push(`Groceries: $${groceriesBudget.toFixed(2)}`);
if (gasBudget > 0) budgetListItems.push(`Gas: $${gasBudget.toFixed(2)}`);
if (miscBudget > 0) budgetListItems.push(`Misc: $${miscBudget.toFixed(2)}`);
if (budgetListItems.length === 0) budgetListItems.push("No budget set");

// Calculate remaining after bills and budget
const afterThisWeekBills = incomingBalance - billsTotal;
const afterThisWeekBudget = incomingBalance - totalWeeklyBudget;

// Create two-column table
const tableData = [];

// Header row
tableData.push(["💸 **Bills Due This Week**", "🛒 **This Week's Budget**"]);

// Content rows - pad to same length
const maxRows = Math.max(billsListItems.length, budgetListItems.length);
for (let i = 0; i < maxRows; i++) {
    tableData.push([
        billsListItems[i] || "",
        budgetListItems[i] || ""
    ]);
}

// Total row
tableData.push([`**Total: $${billsTotal.toFixed(2)}**`, `**Total: $${totalWeeklyBudget.toFixed(2)}**`]);

dv.table(["", ""], tableData);

dv.paragraph("---");

// Bottom calculations - two columns
const calcTableData = [];
calcTableData.push(["💵 **After This Week's Bills**", "🛍️ **After This Week's Budget**"]);
calcTableData.push([
    `INCOMING: $${incomingBalance.toFixed(2)}`,
    `INCOMING: $${incomingBalance.toFixed(2)}`
]);
calcTableData.push([
    `- Bills: $${billsTotal.toFixed(2)}`,
    `- Budget: $${totalWeeklyBudget.toFixed(2)}`
]);
calcTableData.push([
    `**= $${afterThisWeekBills.toFixed(2)}**`,
    `**= $${afterThisWeekBudget.toFixed(2)}**`
]);

dv.table(["", ""], calcTableData);

dv.paragraph("---");

dv.header(4, "📅 Next Week Preview");
if (nextWeekBills.length === 0) {
    dv.paragraph("No bills due next week");
} else {
    for (let bill of nextWeekBills) {
        const name = bill["bill-name"];
        const amount = bill.amount || 0;
        const dueDate = bill["due-date"];
        dv.paragraph(`- ${name} - $${amount.toFixed(2)} (Due: Day ${dueDate})`);
    }
    dv.paragraph(`**Next Week Total:** $${nextWeekTotal.toFixed(2)}`);
}
```

---

## 📊 Current Week Overview

```dataview
TABLE WITHOUT ID
  week as "Week",
  status as "Status",
  "[[" + file.name + "|View]]" as "Link"
FROM "SYSTEM/budget/2025"
WHERE type = "weekly-budget" AND status = "active"
SORT week DESC
LIMIT 1
```

---

## 📈 Recent Weeks

```dataview
TABLE WITHOUT ID
  week as "Week",
  week-start as "Start Date",
  status as "Status",
  "[[" + file.name + "|View]]" as "Link"
FROM "SYSTEM/budget/2025"
WHERE type = "weekly-budget"
SORT week DESC
LIMIT 8
```

---

## 💰 Monthly Debt Progress

**Manual Entry (for now):**

| Month | Total Debt | Paid Down | Progress |
|-------|------------|-----------|----------|
| Oct 2025 | $0 | $0 | - |

**Future:** This will auto-populate from account balances

---

## 🎯 Quick Actions

### This Week
1. [ ] Update hours worked in [[SYSTEM/budget/2025/2025-W41|this week's budget]]
2. [ ] Mark bills as paid
3. [ ] Update account balances in [[SYSTEM/budget/accounts|accounts.md]]
4. [ ] Calculate debt payment

### Monthly
1. [ ] Create new weekly budget notes for next month
2. [ ] Update debt snapshot in [[SYSTEM/budget/accounts|accounts.md]]
3. [ ] Review spending patterns

---

## 🔮 Future Automation Features

**Ready for Implementation:**

### Phase 2: Toggl Integration
- Auto-populate hours worked from Toggl API
- Calculate weekly pay automatically
- Show hours needed to cover bills

### Phase 3: Bill Automation
- Auto-distribute bills by week based on due dates
- Send payment reminders
- Track payment history

### Phase 4: Debt Optimization
- Calculate optimal debt paydown (avalanche vs snowball)
- Project debt-free date
- Visualize progress with obsidian-tracker

### Phase 5: Bank Integration
- Real-time account balance sync
- Transaction categorization
- Budget vs actual tracking

---

## 📝 System Notes

**Current Structure:**
```
SYSTEM/budget/
├── README.md (draft planning)
├── bills.md (master bill list)
├── accounts.md (balance tracking)
├── dashboard.md (this file)
└── 2025/
    ├── 2025-W41.md (weekly budget)
    └── templates/
        └── weekly-budget-template.md
```

**Metadata Fields:**
- All notes use frontmatter for Dataview queries
- Week numbers follow ISO 8601 (YYYY-Wnn)
- Status tracking ready for workflow automation
- Account references prepared for API integration

