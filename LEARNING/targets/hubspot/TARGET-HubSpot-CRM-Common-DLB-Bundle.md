---
silo: LEARNING
category: HubSpot-Research
type: CRM-Bundle-Analysis
version: 1.0
date_created: 2025-07-15
modified: 2025-07-15
tools_used: [chrome, caido]
---

# TARGET-HubSpot-CRM-Common-DLB-Bundle

**File Name:** `bundle.production.js`  
**Purpose:** Core CRM functionalities, UI components, data handling

## Current Version: static-1.3890

- **Full URL:** `https://app-na2.hubspot.com/crm-common-dlb/static-1.3890/bundle.production.js`
- **Source Map URL:** `https://app-na2.hubspot.com/crm-common-dlb/static-1.3890/bundle.production.js.map`

### Version History:
- **static-1.3890 (2025-07-15):** Current active version
- **static-1.3885:** Previous version (superseded)

### Related Source Files (from .map):
- `bpm:///atom@1.3826/js/connect.js`
- `bpm:///general-store@6.20/index.js`
- `bpm:///planout@5.12/index.js`
- [[TARGET-HubSpot-CRM-Common-DLB-Index-1-3890]]
- [[TARGET-HubSpot-CRM-V3-Objects-Batch]]
- [[TARGET-HubSpot-Dataset-Permissions-Access-Control]]

### Current Research Focus:
**Analyzing Index.js for import-related API endpoints and permission checks**

### Findings/Notes:
- Identified potential API call for object creation
- Client-side permission check for 'Import' appears to be handled by specific function
- General-store integration requires scope analysis

### Potential Vulnerabilities:
- **Client-side permission bypass** for import feature
- **Excessive data exposure** through `general-store` if not properly scoped
- **Version tracking** for security regression testing

## Cross-References:
- [[TARGET-HubSpot-Frontend-Overview]]
- [[METH-Bug-Bounty-Frontend-Analysis]]
- [[LRN-JavaScript-Bundle-Analysis]]

---
*Migrated from legacy structure: 2025-09-16*