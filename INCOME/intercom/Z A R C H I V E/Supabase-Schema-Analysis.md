## Database Schema Overview

### **Primary Tables & Relationships:**

#### **Core Job Management:**
```
commitment_blocks (main job container)
├── id, location_id, modality, start_time, end_time, status, duration
├── → locations (org details, zoom info)
├── → client_requests (individual cases within job)
└── → interpreters (assigned interpreter)

client_requests (individual cases)
├── id, commitment_block_id, language_id, program_id
├── client_name, case_number, meeting_type, charges
└── → languages, court_programs
```

#### **Supporting Tables:**
```
interpreters
├── id, first_name, last_name, email
└── → interpreter_languages (many-to-many with languages)

organizations
├── id, name, address, abbreviation
└── → locations (one-to-many)

locations
├── id, name, org_id, zoom_link, zoom_login, type
└── → organizations (belongs to)

languages
├── id, name
└── → interpreter_languages, client_requests

court_programs
├── id, name
└── → client_requests
```

## **Key Findings for Email Draft Interface:**

### **Data Flow for Email Templates:**
1. **Job Context**: `commitment_blocks` provides time, location, modality
2. **Client Context**: `client_requests` provides case details, language
3. **Interpreter Context**: `interpreters` provides name, contact info
4. **Organization Context**: `locations → organizations` provides court details

### **Template Placeholder Mapping:**
```javascript
// Available data for email templates:
{
  // From commitment_blocks
  start_time: "2025-09-17T10:00:00Z",
  end_time: "2025-09-17T12:00:00Z", 
  modality: "Zoom",
  status: "confirmed",
  
  // From client_requests
  client_name: "John Doe",
  case_number: "CR-2025-001",
  meeting_type: "Arraignment",
  charges: "DUI",
  
  // From interpreters
  interpreter_name: "Maria Rodriguez",
  interpreter_email: "maria@example.com",
  
  // From locations/organizations
  court_name: "Kent Municipal Court",
  zoom_link: "https://zoom.us/j/123456789",
  court_address: "220 4th Ave S, Kent, WA"
}
```

## **Current Query Patterns:**

### **Comprehensive Job Data** (from Dashboard.jsx):
```sql
SELECT 
  requests.*,
  interpreters(id, first_name, last_name),
  locations(id, name, zoom_link, organizations(id, name)),
  languages(id, name)
FROM requests
WHERE start_time BETWEEN ? AND ?
```

### **Request with Full Details** (from RequestService.js):
```sql
SELECT 
  commitment_blocks.*,
  locations(*, organizations(*)),
  client_requests(*, languages(*), court_programs(*))
FROM commitment_blocks
ORDER BY start_time
```

## **Email Interface Implementation Insights:**

### **For Our Side Panel Design:**
1. **Job Selection** → Query `commitment_blocks` with full relations
2. **Email Type** → REM/REQ/CONF templates from Obsidian
3. **Data Binding** → Map Supabase fields to template placeholders
4. **Missing Data Detection** → Check for null/empty required fields

### **Cache Strategy Implications:**
- **Hot data**: Today's `commitment_blocks` with relations
- **Template data**: Obsidian markdown files (file-watching)
- **Lookup data**: `interpreters`, `organizations`, `languages` (infrequent changes)

### **Current Status Field Values:**
From JobStatus.jsx: `"initial"`, `"pending"`, `"confirmed"`, `"billed"`

## **Gaps & Opportunities:**

### **Missing for Email Workflow:**
1. **Email tracking** - No sent/delivered status
2. **Template versioning** - No template audit trail  
3. **Interpreter preferences** - No communication preferences stored

### **Schema Strengths:**
1. **Clean separation** - Commitment blocks vs individual requests
2. **Flexible relationships** - Proper foreign keys
3. **Rich context** - Full org/location/interpreter details available

## **Recommendations for Email Interface:**

### **Query for Email Draft:**
```javascript
// Single query to get all email template data
const jobData = await supabase
  .from('commitment_blocks')
  .select(`
    *,
    locations(*, organizations(*)),
    client_requests(*, languages(*), court_programs(*)),
    interpreters(id, first_name, last_name, email)
  `)
  .eq('id', jobId)
  .single();
```

### **Template Placeholder Strategy:**
- **Flatten nested objects** for easy template access
- **Handle missing data** with warning indicators
- **Format dates/times** for email display
- **Generate smart defaults** for common fields

---
*This schema provides excellent foundation for our email interface - all necessary data relationships exist and can be efficiently queried.*