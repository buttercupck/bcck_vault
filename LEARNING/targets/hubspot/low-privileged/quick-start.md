# Low-Privileged Testing Quick Start Guide

**Purpose:** Complete guide for replicating Track A & B with your low-privileged account
**Date:** 2025-10-17
**Status:** Ready for Testing ✅

---

## Quick Navigation

- **Instruction Manual:** `Testing-Instruction-Manual.md` (Full details)
- **Scripts Location:** `./manuals/` (All testing scripts)
- **Templates:** `TEMPLATE_lowpriv_*.py` (Start here)

---

## What We Accomplished (Session Summary)

### Track A: GraphQL ✅ COMPLETE
```
Endpoint: /api/graphql/crm on app-na2.hubspot.com
Status: Full schema extracted (772 types)
Schema File: graphql_schema.json
Attack Vectors: 10+ identified
```

**Key Discoveries:**
- ✅ GraphQL endpoint found and working
- ✅ Schema introspection enabled (all types exposed)
- ✅ CSRF token required (X-HubSpot-CSRF-hubspotapi)
- ✅ 533 object types (Contact, Company, Deal, User, etc.)
- ✅ Mutations available (update, create, delete operations)

### Track B: API Testing ✅ VALIDATED
```
APIs Tested:
- Presence API: /api/presence/v1/presence/portal/{id}/user/{id}
- CHIRP RPC: /api/chirp-frontend-app/v1/gateway/{service}/{method}

Status: Frameworks validated, IDOR testing ready
```

**Key Discoveries:**
- ✅ Portal ID confirmed: 242862774
- ✅ User ID confirmed: 159548558
- ✅ Hublet routing: app-na2.hubspot.com
- ✅ Error messages leak infrastructure info (HTTP 488)
- ✅ CHIRP framework active and accessible
- ✅ Multi-tenant isolation via portalId parameter

### Combined Findings
```
Total Attack Vectors: 20+
Critical Findings: 8
High Findings: 12
Bug Bounty Potential: CRITICAL
```

---

## Your Low-Privileged Testing Plan

### Phase 1: Setup (5 minutes)

#### 1. Gather Your Credentials

Login to HubSpot with your **low-privileged account** and extract:

```
Portal ID: [Check URL after login]
  Example: app-na2.hubspot.com/contacts/123456789/...
                                           ^^^^^^^^^ This is your portal ID

User ID: [From Network tab or browser console]
  Method 1: F12 → Network → Filter "presence" → Look for /user/{ID}
  Method 2: Console → window.hubspot?.bender?.currentUser?.user_id

Hublet: [From URL]
  app-na2.hubspot.com → Hublet is "na2"
  app-na1.hubspot.com → Hublet is "na1"
```

#### 2. Capture Fresh Cookies

**Method A: GraphQL Request (for Track A)**
1. Navigate to Contacts page
2. F12 → Network tab → Clear all
3. Filter for "graphql"
4. Find POST to `/api/graphql/crm`
5. Right-click → Copy → Copy as cURL
6. Extract Cookie header and CSRF token

**Method B: Presence Request (for Track B)**
1. Navigate to Settings page
2. F12 → Network → Filter "presence"
3. Find PUT to `/api/presence/v1/presence/portal/...`
4. Copy Cookie header

**Cookie Format:**
```
Cookie: FPID=...; hubspotapi=...; csrf.app=...; __cf_bm=...
```

**CSRF Token (from cookies):**
```
csrf.app=AAccUft...  ← This value
```

---

### Phase 2: Track A - GraphQL Testing (15 minutes)

#### Script: `TEMPLATE_lowpriv_graphql.py`

**Location:** `./manuals/TEMPLATE_lowpriv_graphql.py`

**Steps:**
1. Open the file in editor
2. Replace configuration values:
   ```python
   HUBLET = "na2"  # Your hublet
   PORTAL_ID = "YOUR_PORTAL_ID"  # Your portal ID
   COOKIE_HEADER = """
   PASTE_COOKIES_HERE
   """
   CSRF_TOKEN = "YOUR_CSRF_TOKEN"
   ```
3. Save and run:
   ```bash
   python3 ./manuals/TEMPLATE_lowpriv_graphql.py
   ```

**Expected Results:**
- ✅ Test 1: Basic typename → Should return `{"__typename": "Query"}`
- ✅ Test 2: Schema metadata → Shows Query/Mutation types
- ✅ Test 3: Contact search → Returns your contacts (or error if no permission)
- ✅ Test 4: Permissions check → Shows currentUserCanView/Edit flags

**What to Look For:**
1. **Successful queries** → Document what data you can access
2. **Permission flags** → Note which show `currentUserCanEdit: false`
3. **Error messages** → Any that reveal unauthorized data
4. **Query types** → Which CRM objects you can query

**IDOR Testing (Manual):**
After baseline works, test IDOR:
1. Edit the script to change `PORTAL_ID` in URL to `YOUR_PORTAL_ID + 1`
2. Run again
3. If you get data from another portal → **CRITICAL IDOR VULNERABILITY**

---

### Phase 3: Track B - Presence API IDOR (15 minutes)

#### Script: `TEMPLATE_lowpriv_presence_idor.py`

**Location:** `./manuals/TEMPLATE_lowpriv_presence_idor.py`

**Steps:**
1. Open the file
2. Replace configuration:
   ```python
   HUBLET = "na2"
   PORTAL_ID = "YOUR_PORTAL_ID"
   USER_ID = "YOUR_USER_ID"
   COOKIE_HEADER = """PASTE_COOKIES"""
   ```
3. Run:
   ```bash
   python3 ./manuals/TEMPLATE_lowpriv_presence_idor.py
   ```

**Expected Results:**
- Phase 1: Baseline (your own user) → Should succeed (200 OK)
- Phase 2: User ID tests → Tests 7 different user IDs
- Phase 3: Portal ID tests → Tests 5 different portal IDs

**Vulnerability Indicators:**
- ✅ **200 OK on other user IDs** → USER IDOR (horizontal escalation)
- ✅ **200 OK on other portal IDs** → PORTAL IDOR (multi-tenant broken)
- ⚠️ **403 Forbidden** → Resource exists but unauthorized (enumeration possible)
- ℹ️ **404 Not Found** → Resource doesn't exist

**Results to Document:**
1. How many other user IDs returned 200 OK?
2. Did any other portal IDs return 200 OK?
3. Error code differences (403 vs 404 for enumeration)

---

### Phase 4: Track B - CHIRP Testing (10 minutes)

#### Script: `TEMPLATE_lowpriv_chirp.py`

**Location:** `./manuals/TEMPLATE_lowpriv_chirp.py`

**Steps:**
1. Open and configure:
   ```python
   HUBLET = "na2"
   PORTAL_ID = "YOUR_PORTAL_ID"
   COOKIE_HEADER = """PASTE_COOKIES"""
   ```
2. Run:
   ```bash
   python3 ./manuals/TEMPLATE_lowpriv_chirp.py
   ```

**Expected Results:**
- Phase 1: Known CHIRP service → May return 200, 400, or 403
- Phase 2: Service enumeration → Tests 13 common services

**Error Code Meanings:**
- **200 OK** → Service accessible, working
- **400 Bad Request** → Service exists, needs correct payload
- **403 Forbidden** → Service exists, permission denied
- **404 Not Found** → Service doesn't exist
- **500 Server Error** → Service exists, has error (may leak info)

**What to Look For:**
1. Any services returning 200 OK (fully accessible)
2. Services returning 400 (exist but need payload)
3. Services returning 403 (exist but forbidden - proves they're real)
4. Error messages mentioning service/method names

---

## Results Template

### Track A Results

```markdown
## GraphQL Testing Results

**Configuration:**
- Portal ID: [YOUR_PORTAL_ID]
- Hublet: [YOUR_HUBLET]
- Test Date: 2025-XX-XX

**Test 1: Basic Typename**
- Status: [Success/Fail]
- Response: [Response data]

**Test 2: Schema Metadata**
- Status: [Success/Fail]
- Query Type: [Query/null]
- Mutation Type: [Mutation/null]

**Test 3: Contact Search**
- Status: [Success/Fail]
- Total contacts accessible: [Number]
- Sample data: [Redacted email/name]

**Test 4: Permissions**
- currentUserCanView: [true/false]
- currentUserCanEdit: [true/false]

**IDOR Test Results:**
- Tested portal ID +1: [Success/Fail/Error code]
- Data returned: [Yes/No]
- Vulnerability: [Yes/No]
```

### Track B Results

```markdown
## Presence API IDOR Results

**Baseline Test:**
- Own user access: [Success/Fail]
- Status code: [200/401/403]

**User ID IDOR Results:**
- User +1: [200/403/404]
- User +2: [200/403/404]
- User +10: [200/403/404]
- Vulnerable: [Yes/No]

**Portal ID IDOR Results:**
- Portal +1: [200/403/404/488]
- Portal +2: [200/403/404/488]
- Vulnerable: [Yes/No]

**CHIRP Framework Results:**
- Known service: [200/400/403/404]
- Services accessible (200): [List]
- Services exist (400/403): [List]
- Framework active: [Yes/No]
```

---

## Troubleshooting

### Issue: HTTP 401 Unauthorized

**Cause:** Cookies expired

**Solution:**
1. Cookies typically expire in 1-2 hours
2. Recapture cookies from browser
3. Make sure you're logged into the low-privileged account
4. Copy fresh Cookie header

### Issue: HTTP 403 Forbidden (GraphQL)

**Cause:** CSRF token missing/expired

**Solution:**
1. Extract fresh CSRF token from `csrf.app` cookie
2. Ensure it matches the cookie value exactly
3. Add header: `X-HubSpot-CSRF-hubspotapi: [TOKEN]`

### Issue: HTTP 404 Not Found

**Cause:** Wrong endpoint or hublet

**Solution:**
1. Verify hublet matches your login URL
2. Check endpoint paths:
   - GraphQL: `/api/graphql/crm` (not `/graphql`)
   - Presence: `/api/presence/v1/presence/portal/...`
   - CHIRP: `/api/chirp-frontend-app/v1/gateway/...`

### Issue: HTTP 488 Wrong Hublet

**Cause:** Portal exists on different hublet

**Solution:**
1. Check error message for `correctHublet` field
2. Update `HUBLET` variable to the correct value
3. Example: Error says "na2" → Use `HUBLET = "na2"`

### Issue: Baseline test fails

**Cause:** Configuration values incorrect

**Solution:**
1. Double-check Portal ID from URL
2. Verify User ID from presence request
3. Confirm hublet matches login domain
4. Test cookies with simple request first

---

## All Available Scripts

### Templates (Start Here)
1. `TEMPLATE_lowpriv_graphql.py` - GraphQL testing
2. `TEMPLATE_lowpriv_presence_idor.py` - Presence API IDOR
3. `TEMPLATE_lowpriv_chirp.py` - CHIRP RPC testing

### Working Scripts (Reference)
4. `graphql_schema_introspection.py` - Full schema extraction (used in session)
5. `test_graphql_formats.py` - Body format validation (used in session)

### Authentication Scripts
6. `test_auth.py` - Basic cookie test
7. `test_auth_v2.py` - Netscape cookie parser
8. `verify_cookies_track_a.py` - Cookie validation

### Track A Scripts
9. `test_graphql_auth.py` - GraphQL with auth
10. `test_graphql_with_params.py` - GraphQL with parameters
11. `test_graphql_final.py` - Complete GraphQL test

### Track B Scripts
12. `test_presence_api.py` - Presence API basic
13. `test_presence_api_hublet.py` - Multi-hublet testing
14. `test_track_b_presence_idor.py` - Comprehensive IDOR
15. `validate_track_b.py` - Track B validation
16. `final_validation.py` - Final checks

---

## Documentation Reference

### Main Documents
1. `Testing-Instruction-Manual.md` - **Complete instruction manual**
2. `Track-A-GraphQL-Complete-Report.md` - Track A findings & attack vectors
3. `Track-B-Peer-Review-Validation.md` - Track B validation results
4. `Presence-API-Testing-Report.md` - Presence API findings
5. `Method-Endpoints-Analysis.md` - API endpoint analysis

### Schema Data
6. `graphql_schema.json` - Full GraphQL schema (772 types)

### Source Files
7. `graphql_headers.md` - Captured GraphQL request
8. `presence_headers.md` - Captured presence request
9. `method_endpoints.md` - Captured API endpoints
10. `cookies.txt` - Cookie file (Netscape format)

---

## Testing Workflow

### Recommended Order

**Day 1: Setup & Baseline**
1. ✅ Extract your portal ID, user ID, hublet
2. ✅ Capture fresh cookies and CSRF token
3. ✅ Run `TEMPLATE_lowpriv_graphql.py` baseline
4. ✅ Run `TEMPLATE_lowpriv_presence_idor.py` baseline

**Day 2: GraphQL Deep Dive**
1. ✅ Analyze GraphQL test results
2. ✅ Document accessible queries
3. ✅ Test IDOR with portal ID +1
4. ✅ Test different CRM object types

**Day 3: API IDOR Testing**
1. ✅ Run full IDOR tests (user + portal)
2. ✅ Document successful IDOR attempts
3. ✅ Test CHIRP framework
4. ✅ Map accessible services

**Day 4: Documentation & Reporting**
1. ✅ Compile all findings
2. ✅ Calculate severity scores
3. ✅ Create bug bounty reports
4. ✅ Prepare evidence (screenshots, logs)

---

## Expected Outcomes

### Low-Privileged User (Normal Behavior)

**Should Have Access To:**
- ✅ Own contact data
- ✅ Contacts assigned to them
- ✅ Own user presence
- ✅ Limited company data they own

**Should NOT Have Access To:**
- ❌ Other portals' data
- ❌ Other users' presence
- ❌ Admin mutations
- ❌ Restricted CRM fields

### Vulnerability Indicators

**Critical Findings:**
- 🚨 Access to other portal IDs → Multi-tenant isolation broken
- 🚨 Access to other user IDs → Horizontal privilege escalation
- 🚨 Mutation access when should be read-only → Vertical escalation

**High Findings:**
- ⚠️ User enumeration via error codes (403 vs 404)
- ⚠️ Portal enumeration via HTTP 488 errors
- ⚠️ Service enumeration via CHIRP error codes

**Medium Findings:**
- ℹ️ Information disclosure in error messages
- ℹ️ Schema introspection enabled
- ℹ️ Internal service names exposed

---

## Bug Bounty Reporting

### When to Report

Report if you find:
1. ✅ Successful IDOR (access to other portal/user data)
2. ✅ Unauthorized mutations (create/update/delete)
3. ✅ Horizontal privilege escalation
4. ✅ Multi-tenant isolation bypass
5. ✅ Significant information disclosure

### Evidence to Collect

1. **Screenshots:**
   - Successful requests showing unauthorized access
   - Response data (redact PII)
   - Error messages with correlation IDs

2. **Request/Response Logs:**
   - Full HTTP request (redact cookies)
   - Full HTTP response
   - Timestamp of test

3. **Step-by-Step Reproduction:**
   - Exact configuration used
   - Portal IDs tested
   - Commands run

4. **Impact Assessment:**
   - What data was accessed
   - How many records affected
   - Potential for mass exploitation

---

## Next Steps After Testing

1. **Review Results:**
   - Check all test outputs
   - Identify successful attacks
   - Document vulnerabilities

2. **Severity Assessment:**
   - CRITICAL: Multi-tenant IDOR
   - HIGH: User IDOR, unauthorized mutations
   - MEDIUM: Enumeration, info disclosure

3. **Create Report:**
   - Use results template above
   - Include evidence
   - Explain impact
   - Suggest remediation

4. **Submit to HubSpot:**
   - Via bug bounty platform
   - Include all evidence
   - Be responsive to questions

---

## Success Metrics

**Testing Complete When:**
- ✅ All 3 templates run successfully
- ✅ Baseline tests pass (own user/portal)
- ✅ IDOR tests completed
- ✅ Results documented
- ✅ Evidence collected

**Bug Bounty Ready When:**
- ✅ Vulnerability confirmed
- ✅ Reproduction steps documented
- ✅ Impact quantified
- ✅ Evidence prepared
- ✅ Report drafted

---

## Quick Commands Reference

```bash
# Navigate to scripts directory
cd ./LEARNING/targets/hubspot/manuals

# Run GraphQL template
python3 TEMPLATE_lowpriv_graphql.py

# Run Presence IDOR template
python3 TEMPLATE_lowpriv_presence_idor.py

# Run CHIRP template
python3 TEMPLATE_lowpriv_chirp.py

# View schema
less ../graphql_schema.json

# Check documentation
cat ../Testing-Instruction-Manual.md
```

---

## Support & Resources

**Documentation:**
- `Testing-Instruction-Manual.md` - Full manual
- `Track-A-GraphQL-Complete-Report.md` - GraphQL details
- `Presence-API-Testing-Report.md` - API testing details

**If You Get Stuck:**
1. Check Troubleshooting section
2. Review Testing-Instruction-Manual.md
3. Verify configuration values
4. Recapture fresh cookies
5. Check error messages carefully

---

**Quick Start Version:** 1.0
**Last Updated:** 2025-10-17
**Status:** Ready for Low-Privileged Testing ✅

**Good luck with your testing! 🎯**
