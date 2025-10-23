# REST API Attack Surface

**Status:** Active Testing
**Primary APIs:** Presence API, CHIRP RPC
**Hublet:** na2

## Attack Surfaces

### 1. Presence API
- **Endpoint:** `/api/presence/v1/presence/portal/{PORTAL_ID}/user/{USER_ID}`
- **Method:** PUT
- **Vulnerability:** Portal ID enumeration, IDOR potential
- **Custom Error:** HTTP 488 with hublet disclosure

### 2. CHIRP RPC
- **Endpoint:** `/api/chirp-frontend-app/v1/gateway/{SERVICE}/{METHOD}`
- **Method:** POST
- **Vulnerability:** Internal service enumeration
- **Finding:** Error messages expose service names

## Quick Start

### Test Presence API
```bash
cd presence/tools/
python3 test_presence_api.py
```

### Test CHIRP RPC
```bash
cd chirp/tools/
python3 cross_portal_idor_test.py
```

## Files

- `presence/` - Presence API testing (user status endpoints)
- `chirp/` - CHIRP RPC testing (internal microservices)
- `endpoints.md` - Discovered REST endpoints catalog
- `endpoints-analysis.md` - Method analysis and attack vectors

## Key Findings

⚠️ **HTTP 488 Error** - Exposes correct hublet in error message
⚠️ **Portal ID Enumeration** - Error codes differ for valid/invalid portals
⚠️ **CHIRP Service Exposure** - Internal RPC methods discoverable
✅ **Multi-Tenant Routing** - Hublet routing logic understood

## Testing Workflow

1. **Presence API IDOR** - Test cross-portal/cross-user access
2. **CHIRP Enumeration** - Map internal microservices
3. **Error Analysis** - Collect information disclosure
4. **Hublet Testing** - Test routing across na1/na2/eu1

## Next Steps

- Enumerate all CHIRP services
- Test Presence API with low-priv credentials
- Map complete REST API surface
- Test for horizontal privilege escalation
