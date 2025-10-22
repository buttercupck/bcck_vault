# Google Calendar → Supabase Mapping

**Date:** 2025-10-22
**Purpose:** Define how Google Calendar events map to Interlingo Supabase database

---

## Google Calendar Structure (Example)

```json
{
  "summary": "ASL - IN PERSON",
  "description": "MARTIN, KIMBERLY\nRED189265\t- PEI\n1\tPHOTO RED LIGHT\nRED189217 - PEI\n2\tPHOTO RED LIGHT",
  "location": "FIFE",
  "start": {
    "dateTime": "2025-12-04T08:30:00-08:00",
    "timeZone": "America/Los_Angeles"
  },
  "end": {
    "dateTime": "2025-12-04T11:30:00-08:00",
    "timeZone": "America/Los_Angeles"
  }
}
```

---

## Parsing Rules

### 1. Summary Field → Language + Modality
**Format:** `[LANGUAGE] - [MODALITY]`

**Examples:**
- `ASL - IN PERSON` → Language: ASL, Modality: In-Person
- `Spanish - ZOOM` → Language: Spanish, Modality: Remote
- `Russian - PHONE` → Language: Russian, Modality: Phone

**Modality Mapping:**
- `IN PERSON` → `In-Person`
- `ZOOM` → `Remote`
- `PHONE` → `Phone`

---

### 2. Location Field → Organization
**Format:** Organization abbreviation or name

**Examples:**
- `FIFE` → Fife Municipal Court
- `KENT` → Kent Municipal Court
- `PUYALLUP` → Puyallup Municipal Court

**Action:** Lookup organization_id from organizations table
- If not found, create new organization entry

---

### 3. Description Field → Client Requests (Can be multiple)
**Format:** Multi-line with case numbers and charges

**Pattern:**
```
[CLIENT NAME]
[CASE_NUMBER] - [PROGRAM]
[SEQUENCE]\t[CHARGE]
[CASE_NUMBER] - [PROGRAM]
[SEQUENCE]\t[CHARGE]
```

**Example Parsing:**
```
MARTIN, KIMBERLY
RED189265 - PEI
1	PHOTO RED LIGHT
RED189217 - PEI
2	PHOTO RED LIGHT
```

**Results in 2 client_requests:**

**Request 1:**
- client_name: "MARTIN, KIMBERLY"
- case_number: "RED189265"
- meeting_type: "PEI"
- charges: "PHOTO RED LIGHT"

**Request 2:**
- client_name: "MARTIN, KIMBERLY"
- case_number: "RED189217"
- meeting_type: "PEI"
- charges: "PHOTO RED LIGHT"

---

## Supabase Insert Flow

### Step 1: Create commitment_block

```sql
INSERT INTO commitment_blocks (
  start_time,
  end_time,
  duration,
  modality,
  status,
  location_id,
  interpreter_id
) VALUES (
  '2025-12-04T08:30:00-08:00',
  '2025-12-04T11:30:00-08:00',
  180,  -- calculated in minutes
  'In-Person',
  'initial',
  [LOOKUP: location_id from FIFE],
  NULL  -- not assigned yet
) RETURNING id;
```

### Step 2: Create client_request(s)

For each parsed case from description:

```sql
INSERT INTO client_requests (
  commitment_block_id,
  language_id,
  program_id,
  client_name,
  case_number,
  meeting_type,
  charges
) VALUES (
  [commitment_block_id from Step 1],
  [LOOKUP: language_id for "ASL"],
  [LOOKUP: program_id for "PEI"],
  'MARTIN, KIMBERLY',
  'RED189265',
  'PEI',
  'PHOTO RED LIGHT'
);
```

---

## Lookup Tables Needed

### 1. Languages
**Query:** Match summary field language to languages.name
- Exact match: "Spanish" → languages.id
- Fuzzy match if needed: "Span" → "Spanish"

**Example:**
```sql
SELECT id FROM languages WHERE name ILIKE 'ASL' LIMIT 1;
```

### 2. Organizations
**Query:** Match location field to organizations table
- First try: organizations.abbreviation
- Fallback: organizations.name

**Example:**
```sql
SELECT id FROM organizations
WHERE abbreviation ILIKE 'FIFE'
   OR name ILIKE '%FIFE%'
LIMIT 1;
```

**If not found:** Create new organization
```sql
INSERT INTO organizations (name, abbreviation)
VALUES ('Fife Municipal Court', 'FIFE')
RETURNING id;
```

### 3. Locations
**Query:** Get location_id from organization_id
```sql
SELECT id FROM locations WHERE organization_id = [org_id] LIMIT 1;
```

**If not found:** Create new location
```sql
INSERT INTO locations (organization_id, name)
VALUES ([org_id], 'Fife Municipal Court')
RETURNING id;
```

### 4. Court Programs
**Query:** Match meeting_type from description (e.g., "PEI")
```sql
SELECT id FROM court_programs WHERE name = 'PEI' LIMIT 1;
```

**If not found:** Create or use NULL

---

## Data Quality Rules

### Required Fields (Must Parse Successfully)
- ✅ start_time (from calendar.start.dateTime)
- ✅ end_time (from calendar.end.dateTime)
- ✅ language (from summary)
- ✅ modality (from summary)
- ✅ organization (from location)

### Optional Fields (Can be NULL)
- client_name (from description)
- case_number (from description)
- charges (from description)
- interpreter_id (NULL on creation)
- program_id (lookup from description, NULL if not found)

### Error Handling
If parsing fails:
1. Log the full calendar event JSON
2. Insert basic commitment_block with available data
3. Mark status as 'error' or 'needs_review'
4. Send notification to user for manual review

---

## n8n Implementation Notes

### Workflow Structure
```
1. Google Calendar Trigger (Watch Events)
   ↓
2. JavaScript: Parse summary → language + modality
   ↓
3. Supabase: Lookup language_id
   ↓
4. Supabase: Lookup/create organization
   ↓
5. Supabase: Lookup/create location
   ↓
6. JavaScript: Parse description → client requests array
   ↓
7. Supabase: Insert commitment_block
   ↓
8. Loop: For each client request
   ↓
9. Supabase: Insert client_request
   ↓
10. Done (job now visible in Interlingo web app)
```

### Key Functions Needed

**Function 1: Parse Summary**
```javascript
function parseSummary(summary) {
  const parts = summary.split(' - ');
  return {
    language: parts[0].trim(),
    modality: parts[1]?.trim().replace('IN PERSON', 'In-Person')
                             .replace('ZOOM', 'Remote')
                             .replace('PHONE', 'Phone')
  };
}
```

**Function 2: Parse Description**
```javascript
function parseDescription(description) {
  const lines = description.split('\n');
  const clientName = lines[0].trim();
  const requests = [];

  let currentCase = null;

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();

    // Check if it's a case number line
    if (line.includes(' - ')) {
      const [caseNumber, program] = line.split(' - ');
      currentCase = {
        clientName,
        caseNumber: caseNumber.trim(),
        program: program.trim(),
        charges: []
      };
      requests.push(currentCase);
    }
    // Check if it's a charge line
    else if (line.match(/^\d+\t/)) {
      const charge = line.split('\t')[1]?.trim();
      if (currentCase && charge) {
        currentCase.charges.push(charge);
      }
    }
  }

  // Combine charges into single string per request
  requests.forEach(req => {
    req.charges = req.charges.join(', ');
  });

  return requests;
}
```

---

## Testing Checklist

- [ ] Parse simple event (1 language, 1 modality, 1 client)
- [ ] Parse complex event (multiple cases for same client)
- [ ] Parse event with new organization (should auto-create)
- [ ] Parse event with missing description (should create block only)
- [ ] Parse event with unknown language (should error gracefully)
- [ ] Verify commitment_block created with correct times
- [ ] Verify all client_requests linked to same block
- [ ] Verify job appears in Interlingo web app dashboard
- [ ] Test duplicate event prevention (don't re-create if already exists)

---

## Future Enhancements

1. **Interpreter Assignment from Calendar**
   - Add interpreter name to summary or description
   - Parse and lookup interpreter_id
   - Auto-assign on creation

2. **Status Updates via Calendar**
   - Update event title to include status
   - Sync status changes back to Supabase

3. **Bidirectional Sync**
   - Changes in Interlingo → Update Google Calendar
   - Keep systems in sync

---

**Next Steps:**
1. Populate organizations table with your common courts
2. Build n8n workflow using this mapping
3. Test with sample calendar events
4. Deploy and monitor for errors
