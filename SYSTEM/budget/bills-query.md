---
type: budget-helper
category: automation
---

# Bills Due This Week - Auto Query

This query automatically calculates which bills are due in the current week.

```dataviewjs
// Get today's date
const today = dv.date("today");
const currentDay = today.day;
const currentMonth = today.month;
const currentYear = today.year;

// Calculate the current week of the month (1-5)
const weekOfMonth = Math.ceil(currentDay / 7);

// Get start and end of current week
const startOfWeek = currentDay - (currentDay % 7) + 1; // Start on day 1, 8, 15, 22, or 29
const endOfWeek = startOfWeek + 6;

// Query all bills
const bills = dv.pages('"SYSTEM/budget/bills"')
    .where(p => p.type === "bill")
    .sort(p => p["due-date"], 'asc');

// Filter bills due this week
const billsDueThisWeek = bills.where(b => {
    const dueDate = b["due-date"];
    return dueDate >= startOfWeek && dueDate <= endOfWeek;
});

// Display header
dv.header(3, "💸 Bills Due This Week");
dv.paragraph(`**Week ${weekOfMonth} of ${currentMonth}/${currentYear}** (Days ${startOfWeek}-${endOfWeek})`);
dv.paragraph("---");

// Check if there are bills due
if (billsDueThisWeek.length === 0) {
    dv.paragraph("✅ **No bills due this week!**");
} else {
    // Display bills as checklist
    let total = 0;

    for (let bill of billsDueThisWeek) {
        const name = bill["bill-name"];
        const amount = bill.amount || 0;
        const dueDate = bill["due-date"];
        const autoPay = bill["auto-pay"] ? "🔄 Auto-Pay" : "💳 Manual";
        const account = bill.account || "unknown";

        total += amount;

        // Display as list item with link to bill
        dv.paragraph(`- [ ] **${name}** - $${amount.toFixed(2)} (Due: Day ${dueDate}) - ${autoPay} - ${account}`);
    }

    dv.paragraph("---");
    dv.paragraph(`**Total Due This Week:** $${total.toFixed(2)}`);
}

// Show next week's bills preview
dv.paragraph("---");
dv.header(4, "📅 Next Week Preview");

const nextWeekStart = endOfWeek + 1;
const nextWeekEnd = nextWeekStart + 6;

const nextWeekBills = bills.where(b => {
    const dueDate = b["due-date"];
    return dueDate >= nextWeekStart && dueDate <= Math.min(nextWeekEnd, 31);
});

if (nextWeekBills.length === 0) {
    dv.paragraph("No bills due next week");
} else {
    let nextTotal = 0;
    for (let bill of nextWeekBills) {
        const name = bill["bill-name"];
        const amount = bill.amount || 0;
        const dueDate = bill["due-date"];
        nextTotal += amount;
        dv.paragraph(`- ${name} - $${amount.toFixed(2)} (Due: Day ${dueDate})`);
    }
    dv.paragraph(`**Next Week Total:** $${nextTotal.toFixed(2)}`);
}
```

---

## How This Works

**Current Week Calculation:**
- Takes today's date
- Calculates which week of the month (1-5)
- Week 1: Days 1-7
- Week 2: Days 8-14
- Week 3: Days 15-21
- Week 4: Days 22-28
- Week 5: Days 29-31

**What It Shows:**
- All bills with `due-date` falling in current week range
- Total amount due this week
- Preview of next week's bills

**Future Enhancements:**
- Add "Mark as Paid" button (requires custom plugin)
- Calculate hours needed to work per bill
- Send notifications 3 days before due date
- Track payment history automatically

