---
type: budget-master
category: bills
---

# Bills Master List

**Instructions:**
- Each bill is now its own note in `SYSTEM/budget/bills/` folder
- Edit individual bill notes to update amounts, due dates, etc.
- The dashboard **automatically shows** which bills are due this week
- No manual calculation needed!

---

## 📋 All Bills (Auto-Generated)

```dataview
TABLE
  bill-name as "Bill",
  "$" + amount as "Amount",
  due-date as "Due (Day)",
  auto-pay as "Auto-Pay",
  account as "Account",
  category as "Category"
FROM "SYSTEM/budget/bills"
WHERE type = "bill"
SORT due-date ASC
```

---

## ➕ How to Add a New Bill

1. Create new file in `SYSTEM/budget/bills/` folder
2. Use this template:

```yaml
---
type: bill
bill-name: Bill Name Here
amount: 0
due-date: 15
auto-pay: false
account: checking-1
category: Utilities
status: unpaid
---
```

3. The bill will automatically appear in all queries!

---

## 📊 Bills by Category

```dataview
TABLE
  "**" + Bill-Name + "**" as "Bill",
  Amount as "Amount",
  Due-Date as "Due (Day of Month)",
  Auto-Pay as "Auto-Pay",
  Account as "Account"
FROM "SYSTEM/budget"
WHERE type = "bill"
SORT Category ASC, Due-Date ASC
```

---

## 💰 Total Monthly Bills

**Quick Math:**
- Total Housing: $0.00
- Total Utilities: $0.00
- Total Insurance: $0.00
- Total Subscriptions: $0.00
- **Total Monthly:** $0.00

**Total Weekly Average:** $0.00

---

## Future: Individual Bill Notes

When ready for advanced automation, each bill can become its own note:

**Example: `bills/rent.md`**
```yaml
---
type: bill
bill-name: Rent
amount: 1200
due-date: 1
auto-pay: false
account: checking-1
category: housing
payment-history: []
---
```

Then Dataview queries will pull from all bill notes automatically.

---

## Future Automation Hooks

**This structure supports:**

### Phase 2: Auto-Week Calculation
```javascript
// Calculate which week of month based on due-date
const weekNumber = Math.ceil(dueDate / 7)
```

### Phase 3: Payment Reminders
- Check today's date against due dates
- Send notification for bills due in 3 days
- Flag overdue bills

### Phase 4: Payment History
- Track when bills were actually paid
- Compare actual vs budgeted amounts
- Trend analysis for variable bills

### Phase 5: Hours Required Calculator
```javascript
// Calculate hours needed to work to cover this bill
hoursNeeded = billAmount / hourlyRate
```

