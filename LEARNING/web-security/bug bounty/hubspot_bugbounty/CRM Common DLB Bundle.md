---
date_created: 2025-07-15 14:47
modified: Tuesday 15th July 2025 14:47:56
silo: bug_bounty
"document_type:": .js
topic: hubspot
sub_topics:
  - crm-common-dlb
tools used: chrome, caido
---
---

**File Name:** `bundle.production.js`
**Purpose:** Core CRM functionalities, UI components, data handling (general).

## Current Version: static-1.3890

* **Full URL:** `https://app-na2.hubspot.com/crm-common-dlb/static-1.3890/bundle.production.js`
* **Source Map URL:** `https://app-na2.hubspot.com/crm-common-dlb/static-1.3890/bundle.production.js.map`

### Version History:

* **static-1.3890 (2025-07-15):** Current active version.
* **static-1.3885 (Previous Date):** (Optional: Note when you last saw this version, or if it was superseded)

### Related Source Files (from .map):

* `bpm:///atom@1.3826/js/connect.js`
* `bpm:///general-store@6.20/index.js`
* `bpm:///planout@5.12/index.js`
* **[[CRM Common DLB Index.js - 1.3890]]** <-- **ADD THIS LINK!**
- [[crm_v3_objects_batch]]
- [[Dataset Permissions and Access Control]]
### Deep Dives / Current Focus:

* **Currently analyzing `[[CRM Common DLB Index.js - 1.3890]]` for import-related API endpoints and permission checks.**

### Findings/Notes:

* Identified potential API call for object creation in `[link to relevant section/function in the readable code, or a sub-note if complex]`.
* Client-side permission check for 'Import' appears to be handled by a function in `[link to relevant permission logic]`.

### Potential Vulnerabilities:

* Client-side permission bypass for import feature. (Link to specific finding note: `[[CRM Import Bypass 2025-07-15]]`)
* Excessive data exposure through `general-store` if not properly scoped.