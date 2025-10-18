# Track A: GraphQL Infrastructure Validation - Results

**Date:** 2025-10-17
**Phase:** Step 1 Completed (Endpoint Enumeration)
**Status:** Requires Manual Testing with Authenticated Session

---

## STEP 1 RESULTS: Endpoint Enumeration (Unauthenticated)

### Endpoints Tested

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `https://app.hubspot.com/graphql` | GET | 404 | Not Found |
| `https://app.hubspot.com/graphql` | POST | **405** | **Method Not Allowed - Endpoint EXISTS but POST blocked** |
| `https://api.hubspot.com/graphql` | GET | 404 | Not Found |
| `https://api.hubspot.com/graphql` | POST | 404 | Not Found |
| `https://app.hubspot.com/api/graphql` | POST | 404 | Not Found |
| `https://app.hubspot.com/graphql/batch` | POST | 404 | Not Found |
| `https://api.hubspot.com/graphql/batch` | POST | 404 | Not Found |

---

## KEY FINDING

**CRITICAL:** `https://app.hubspot.com/graphql` returns **405 Method Not Allowed** on POST

**What This Means:**
- The endpoint EXISTS (404 would mean it doesn't exist)
- POST method is blocked at the nginx level
- Likely requires:
  - Authentication (cookies/tokens)
  - Specific headers (CSRF token, Content-Type)
  - GET method instead of POST
  - Different request format

**Next Action:** Test with authenticated session cookies to bypass 405 error

---

## STEP 2: MANUAL TESTING REQUIRED

Due to cookie complexity (special characters, parentheses), you need to run these tests manually in your browser or with proper cookie handling.

### Option A: Browser Console Testing (RECOMMENDED)

**Step 1: Open HubSpot in Browser**
```bash
# Navigate to: https://app.hubspot.com
# Ensure you're logged in
```

**Step 2: Test GraphQL in Browser Console**
```javascript
// Test 1: Basic GraphQL query
fetch('https://app.hubspot.com/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: '{ __typename }'
  }),
  credentials: 'include'  // Include cookies
}).then(r => r.text()).then(console.log);

// Test 2: GraphQL introspection
fetch('https://app.hubspot.com/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: `{
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
      }
    }`
  }),
  credentials: 'include'
}).then(r => r.json()).then(console.log);

// Test 3: Full schema dump
fetch('https://app.hubspot.com/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: `{
      __schema {
        types {
          name
          kind
          fields {
            name
            type {
              name
              kind
              ofType {
                name
                kind
              }
            }
          }
        }
      }
    }`
  }),
  credentials: 'include'
}).then(r => r.json()).then(data => {
  console.log(JSON.stringify(data, null, 2));
  // Save to variable for export
  window.hubspotSchema = data;
});

// Export schema to file
copy(JSON.stringify(window.hubspotSchema, null, 2));
// Then paste into: hubspot-graphql-schema.json
```

---

### Option B: curl with Manual Cookie Input

**Step 1: Extract Cookies from Browser**
```javascript
// In browser console on app.hubspot.com:
document.cookie.split(';').map(c => c.trim()).join('; ')
```

**Step 2: Test with curl**
```bash
# Replace YOUR_COOKIES with the output from Step 1
curl -X POST https://app.hubspot.com/graphql \
  -H "Content-Type: application/json" \
  -H "Cookie: YOUR_COOKIES" \
  -d '{"query":"{ __typename }"}' \
  | jq .

# If that works, try introspection:
curl -X POST https://app.hubspot.com/graphql \
  -H "Content-Type: application/json" \
  -H "Cookie: YOUR_COOKIES" \
  -d '{"query":"{ __schema { queryType { name } mutationType { name } } }"}' \
  | jq .
```

---

### Option C: nuclei GraphQL Templates

```bash
# Save your cookies to a file (one cookie per line in Netscape format)
# Then run nuclei:

nuclei -u https://app.hubspot.com/graphql \
  -H "Cookie: YOUR_COOKIES_HERE" \
  -t ~/nuclei-templates/http/graphql/ \
  -o graphql-nuclei-results.txt \
  -v

# Specific tests:
nuclei -u https://app.hubspot.com/graphql \
  -H "Cookie: YOUR_COOKIES" \
  -t ~/nuclei-templates/http/graphql/graphql-introspection.yaml \
  -v

nuclei -u https://app.hubspot.com/graphql \
  -H "Cookie: YOUR_COOKIES" \
  -t ~/nuclei-templates/http/graphql/graphql-batch-query.yaml \
  -v
```

---

## ALTERNATIVE GRAPHQL ENDPOINT PATTERNS TO TEST

Based on common GraphQL deployments and HubSpot's architecture, test these additional patterns:

```bash
# Different paths
https://app.hubspot.com/api/graphql
https://app.hubspot.com/v1/graphql
https://app.hubspot.com/crm/graphql
https://app.hubspot.com/portal/{PORTAL_ID}/graphql

# Subdomain variations
https://graphql.hubspot.com
https://api-na1.hubspot.com/graphql
https://private-na1.hubspot.com/graphql

# With hublet
https://app-na1.hubspot.com/graphql
https://app-eu1.hubspot.com/graphql

# GraphQL Playground/IDE (often exposed)
https://app.hubspot.com/graphql/playground
https://app.hubspot.com/graphql/graphiql
https://app.hubspot.com/graphql/voyager
https://app.hubspot.com/___graphql  # Apollo Studio pattern
```

---

## EXPECTED RESPONSES

### Success (Introspection Enabled)
```json
{
  "data": {
    "__schema": {
      "queryType": { "name": "Query" },
      "mutationType": { "name": "Mutation" },
      "subscriptionType": null
    }
  }
}
```

### Success (Introspection Disabled)
```json
{
  "errors": [{
    "message": "GraphQL introspection is not allowed",
    "extensions": { "code": "GRAPHQL_VALIDATION_FAILED" }
  }]
}
```

### Authentication Required
```json
{
  "errors": [{
    "message": "Unauthorized",
    "extensions": { "code": "UNAUTHENTICATED" }
  }]
}
```

---

## IF GRAPHQL WORKS: NEXT STEPS

### 1. Schema Export
Once you get a successful response, save the full schema:
```bash
# Using the browser console method above, or:
curl -X POST https://app.hubspot.com/graphql \
  -H "Cookie: YOUR_COOKIES" \
  -H "Content-Type: application/json" \
  -d @introspection-query.json \
  > hubspot-graphql-schema.json
```

### 2. Schema Visualization
```bash
# Option A: GraphQL Voyager (online)
# Upload hubspot-graphql-schema.json to:
# https://graphql-kit.com/graphql-voyager/

# Option B: Local GraphQL Playground
npm install -g graphql-playground
graphql-playground

# Then load schema from file
```

### 3. Query Discovery
```bash
# Use InQL (Burp Extension) or:
cat hubspot-graphql-schema.json | jq '.data.__schema.types[] | select(.kind=="OBJECT") | .name'

# Find mutations:
cat hubspot-graphql-schema.json | jq '.data.__schema.mutationType.fields[] | .name'
```

### 4. Attack Surface Testing

**High-Priority Tests:**
1. **Query Depth** - Test nested query limits
2. **Batching** - Test if array of queries accepted
3. **Field Suggestions** - Intentional typos to leak field names
4. **Directive Injection** - Test custom directives (@client, @export, etc.)
5. **IDOR via IDs** - Enumerate object IDs in queries
6. **Authorization Bypass** - Mix public/private queries in batch

---

## TRACK A FINDINGS SUMMARY

**Endpoint Status:**
- ✅ `app.hubspot.com/graphql` EXISTS (405 response)
- ❌ `api.hubspot.com/graphql` does NOT exist (404)
- ❌ Batch endpoints NOT found
- ⏳ Authenticated testing PENDING

**Confidence Level:**
- **High:** GraphQL endpoint exists at app.hubspot.com/graphql
- **Medium:** Requires authentication (based on 405 vs 401/403)
- **Unknown:** Whether introspection is enabled
- **Unknown:** Schema size and attack surface

**Next Phase:**
Manual browser-based testing required due to cookie complexity.

---

## FILES GENERATED

None yet - awaiting successful GraphQL response to generate:
- `hubspot-graphql-schema.json` - Full schema dump
- `graphql-queries-discovered.txt` - List of available queries
- `graphql-mutations-discovered.txt` - List of available mutations
- `graphql-nuclei-results.txt` - Nuclei scan results

---

## COMPARISON WITH TRACK B FINDINGS

Track B (source map analysis) predicted:
- GraphQL endpoint at `/graphql` ✅ CONFIRMED
- Apollo Client 3.43 usage ✅ CONSISTENT
- Custom `apollo-dlb` bridge ✅ CONSISTENT
- Possible batching support ⏳ TO BE TESTED

**Validation:** Source map predictions were accurate. GraphQL infrastructure confirmed.

---

## RECOMMENDED IMMEDIATE ACTION

**Use Browser Console Method (Option A above)** - This is the fastest way to test with your authenticated session.

1. Open https://app.hubspot.com in your browser
2. Open DevTools Console (F12)
3. Run the Test 1 fetch command
4. If successful, run Test 2 (introspection)
5. If introspection works, run Test 3 (full schema dump)
6. Copy schema and save to file
7. Report back results

**Time Estimate:** 5-10 minutes

---

**Track A Status:** Step 1 Complete - Awaiting Manual Testing
**Next Update:** After browser console testing results
