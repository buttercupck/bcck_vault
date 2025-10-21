# HubSpot Bundle Analysis - Bug Bounty Recon

**Target:** HubSpot
**Date:** October 15, 2025
**Files Analyzed:**
- `head-dlb.bundle.production.js` (53KB, 758 lines)
- `head-dlb.bundle.production.js.map` (227KB)
**Recon Type:** Client-Side JavaScript Analysis

---

## 🎯 Executive Summary

These files are HubSpot's error monitoring and observability system loaded on every page. For bug bounty hunters, this is a **goldmine of reconnaissance data** revealing internal architecture, undocumented endpoints, environment detection mechanisms, and client-side storage patterns.

**High-Value Findings:**
- 3+ undocumented API endpoints
- Internal RPC framework (CHIRP) exposed
- QA/testing environment access patterns
- Portal ID extraction mechanisms
- Session tracking implementation
- 28 source files via source map

---

## 🔍 Attack Surface Discovery

### 1. **Endpoint Discovery**

**Error Reporting Endpoints:**
```
POST https://exceptions.hubspot.com/.../api/{project}/store/
POST https://exceptions[-{hublet}].hubspot[{env}].com/.../api/.../store/
POST https://exceptions.hubspot.com/frontend/observability/page-tracking/store/
```

**Environment Variations Detected:**
- `exceptions.hubspot.com` (production)
- `exceptions-na1.hubspot.com` (North America)
- `exceptions-eu1.hubspot.com` (Europe)
- `exceptions.hubspotqa.com` (QA environment)

**Bug Bounty Tests:**
- Test these endpoints for injection (XSS, SQLi, NoSQLi)
- Try SSRF via crafted error payloads
- Test authentication/authorization on page-tracking endpoint
- Enumerate other hublets (ap1, ap2, etc.)
- Test if `hubspotqa.com` has weaker security

### 2. **Subdomain Enumeration Intel**

**Patterns Found:**
```
{service}-{hublet}.{brand}{env}.{tld}
```

**Service Prefixes:** api, local, app, private, platform, tools, meetings, payments, mcp

**Brand Domains:** hubspot, hubteam, grader, getsignals, getsidekick, gettally, hubspotemail, customer-hub, hubspotservicehub, hubspotquote, hubspotdocuments, hs-data-privacy

**Hublets:** na1, eu1, (likely ap1, ap2, etc.)

**Example Subdomains to Test:**
```
api-na1.hubspot.com
app-eu1.hubspot.com
private-na1.hubspotqa.com
meetings-na1.hubspot.com
payments-na1.hubspot.com
```

### 3. **Internal Architecture Revealed**

**CHIRP RPC Framework**
- HubSpot's internal microservices communication system
- Service-to-service RPC calls
- Error structure reveals service names, method names, error types

**What This Means:**
- Map internal microservices by triggering CHIRP errors
- Test for IDOR by manipulating service calls
- Look for method enumeration opportunities
- Check if you can call internal methods directly

**CHIRP Error Pattern:**
```javascript
Error: CHIRP RPC failed for {methodName}
  cause: {
    cause: ChirpError | ChirpInternalError {
      serviceName: "...",
      type: "...",
      chirpErrorMessage: "..."
    }
  }
```

**Extraction Strategy:**
Search all HubSpot JS files for `CHIRP RPC failed` to map services.

### 4. **BPM Package Manager**

**Discovery:** HubSpot uses internal package manager called BPM

**Source Path Format:**
```
bpm:///PackageName@Version/js/path/to/file.js
```

**28 Packages Found:**
- HeadJS@2.587
- raven-hubspot@1.5344
- raven@3.5037
- head-dlb@1.4210
- PortalIdParser@2.291
- enviro@4.313
- hs-promise-rejection-tracking@1.4568
- (21 more in source map)

**Bug Bounty Value:**
- Check for outdated vulnerable versions (especially raven@3.5037 from 2017)
- Test for prototype pollution in old libraries
- Look for known CVEs in dependencies

---

## 🚪 Access Control & Authentication Vectors

### 1. **Portal ID System**

**How Portal IDs Are Extracted:**
```javascript
// From URL path: /portal-name/123456/...
pathRegex: /^\/(?:[A-Za-z0-9-_]*)\/(\d+)(?:\/|$)/

// From query param: ?portalid=123456
queryParamRegex: /(?:\?|&)portalid=(\d+)/i
```

**Bug Bounty Tests:**
- IDOR: Can you access other portal data by changing the ID?
- Privilege escalation: What happens with portal ID 0, -1, or 999999999?
- Does portal context carry across requests?
- Can you inject into the portal ID field?

### 2. **Environment Switching**

**localStorage Keys That Control Behavior:**
```javascript
ENV                    // Override environment (qa, prod, development)
HUBLET                 // Override data center location
DEBUG                  // Enable verbose logging
DEPLOYED              // Deployment flag
HUBSPOT_DEBUG_DEFINE  // Module loading debug
```

**Bug Bounty Tests:**
1. Open HubSpot production site
2. Open console and run:
```javascript
localStorage.setItem('ENV', 'qa');
localStorage.setItem('DEBUG', 'true');
localStorage.setItem('HUBSPOT_DEBUG_DEFINE', 'true');
location.reload();
```
3. Check if:
   - You access QA-only features
   - Debug endpoints are exposed
   - Error messages leak more info
   - Rate limiting is disabled

### 3. **Test Detection Bypass**

**Selenium Cookie:**
```javascript
// Checks for: hs_selenium cookie
// Used to identify automated testing
```

**Bug Bounty Tests:**
- Set `hs_selenium` cookie - does rate limiting disappear?
- Do test-only endpoints become available?
- Does authentication behave differently?

---

## 🔐 Client-Side Storage Analysis

### localStorage/sessionStorage Keys

```javascript
// Environment Control
'ENV'                      // qa, prod, development
'HUBLET'                   // na1, eu1, ap1, etc.
'DEPLOYED'                 // true/false
'DEBUG'                    // true/false
'HUBSPOT_DEBUG_DEFINE'     // true/false

// Session Tracking
'__hmpl'                   // Amplitude analytics session
                          // Contains: { session_id, ... }
```

### Cookies

```javascript
'hs_selenium'             // Test automation marker
```

### Bug Bounty Tests

**Session Fixation:**
- Can you set `__hmpl` session_id for another user?
- Does session ID from localStorage override server session?

**Storage Injection:**
- Try XSS payloads in localStorage keys
- Test for prototype pollution via localStorage

**Debug Mode Exploitation:**
- Enable all debug flags, look for exposed secrets/endpoints

---

## 🌐 Network Request Interception

### What Gets Monitored

The code wraps:
- `XMLHttpRequest` (XHR)
- `fetch()` API
- `setTimeout` / `setInterval`
- Browser history API
- DOM event listeners

### Correlation ID System

**Headers Tracked:**
```
X-HubSpot-Correlation-Id
Server-Timing: hcid;desc="..."
```

**Bug Bounty Tests:**
- Can you forge correlation IDs to link your requests to another user?
- Do correlation IDs grant any special access?
- Test for IDOR using correlation IDs from error messages

---

## 💉 Injection Points

### 1. **Error Reporting Injection**

**User-Controlled Data in Error Reports:**
- URLs (with query params)
- Console messages
- Breadcrumbs (user actions)
- Stack traces
- Custom error messages

**Tests:**
```javascript
// Try XSS in console
console.error('<img src=x onerror=alert(1)>');

// Try injection in URL
window.location = 'https://app.hubspot.com/dashboard?xss=<script>alert(1)</script>';

// Trigger error with malicious message
throw new Error('"><img src=x onerror=alert(1)>');
```

Check if your payload appears in:
- Sentry dashboard (for HubSpot employees)
- Error response bodies
- Reflected anywhere

### 2. **Breadcrumb Injection**

**What Gets Logged:**
- Clicked elements (DOM selectors)
- Keypresses (form inputs)
- Navigation (URLs)
- Network requests

**Tests:**
- Create DOM element with XSS payload in attributes:
```html
<button data-test-id='"><script>alert(1)</script>'>Click</button>
```
- See if payload appears in breadcrumb trail

### 3. **Header Injection**

**Server-Timing Header Parsing:**
```javascript
// Parses: Server-Timing: hcid;desc="..."
```

**Test:**
Try to inject malicious Server-Timing headers if you control a server HubSpot makes requests to (SSRF chain).

---

## 🔄 Source Map Exploitation

### What You Can Do

The `.map` file contains **28 original source files**. These are the unminified, readable versions.

**Extraction Method:**
1. Download: `head-dlb.bundle.production.js.map`
2. Parse JSON
3. Extract `sourcesContent` array
4. Each entry is a full source file

**What to Look For:**
- Hardcoded API keys or secrets
- Commented-out code with sensitive info
- Internal API endpoints
- Authentication logic
- Vulnerable code patterns
- Developer comments revealing architecture

**Tools:**
```bash
curl -s https://static.hsappstatic.net/.../bundle.production.js.map | jq -r '.sourcesContent[]' > sources.txt
```

---

## 🎭 Reconnaissance Methodology

### Phase 1: Passive Recon (Current Phase)

✅ **Completed:**
- Downloaded and analyzed client-side bundles
- Mapped error reporting infrastructure
- Identified internal frameworks (CHIRP, BPM)
- Extracted environment detection logic
- Found localStorage manipulation vectors

### Phase 2: Active Recon (Next Steps)

**Subdomain Enumeration:**
```bash
# Generate wordlist from discovered patterns
for service in api app private platform tools meetings payments; do
  for hublet in na1 eu1 ap1 ap2; do
    for env in "" "qa"; do
      echo "${service}-${hublet}.hubspot${env}.com"
    done
  done
done | httpx -silent -status-code
```

**Endpoint Discovery:**
```bash
# Test discovered endpoints
curl -X POST https://exceptions.hubspot.com/frontend/observability/page-tracking/store/ \
  -H "Content-Type: application/json" \
  -d '{"test": "payload"}'
```

**Storage Manipulation:**
```javascript
// In browser console on app.hubspot.com
localStorage.setItem('ENV', 'qa');
localStorage.setItem('DEBUG', 'true');
sessionStorage.setItem('HUBLET', 'eu1');
location.reload();
// Observe behavior changes
```

**CHIRP Service Mapping:**
```bash
# Search all JS files for CHIRP errors
curl -s https://app.hubspot.com | grep -oP "CHIRP RPC failed for \w+" | sort -u
```

### Phase 3: Vulnerability Testing

Based on findings, test for:
1. **IDOR via Portal IDs** - Access other customer portals
2. **Environment Switching** - Access QA features in prod
3. **XSS in Error Reporting** - Inject payloads into Sentry
4. **SSRF via Error Endpoints** - Make Sentry fetch arbitrary URLs
5. **Session Fixation** - Control `__hmpl` session IDs
6. **Rate Limit Bypass** - Use `hs_selenium` cookie
7. **Subdomain Takeover** - Check orphaned subdomains from enumeration

---

## 🎯 High-Priority Targets

### Critical Findings to Test First

| Priority | Finding | Test | Potential Impact |
|----------|---------|------|------------------|
| 🔴 **P1** | Portal ID extraction | IDOR across portals | Access to other customer data |
| 🔴 **P1** | ENV localStorage override | Access QA in prod | Bypass security controls |
| 🟠 **P2** | Error reporting endpoints | XSS injection | Compromise employee accounts |
| 🟠 **P2** | CHIRP service exposure | Method enumeration | Internal API access |
| 🟠 **P2** | Correlation ID tracking | ID forgery | Session hijacking |
| 🟡 **P3** | Source map disclosure | Secret extraction | API keys, credentials |
| 🟡 **P3** | Subdomain patterns | Takeover attempts | Subdomain compromise |
| 🟡 **P3** | `hs_selenium` cookie | Rate limit bypass | Abuse protection bypass |

---

## 🛠️ Testing Checklist

### Environment Manipulation
- [ ] Set `ENV=qa` in localStorage on production
- [ ] Toggle `DEBUG=true` and capture verbose output
- [ ] Switch `HUBLET` values and observe routing changes
- [ ] Test with `hs_selenium` cookie set
- [ ] Check if `DEPLOYED=false` exposes debug endpoints

### Portal ID Testing
- [ ] Change portal ID in URL path
- [ ] Try portal ID -1, 0, 1, 999999999
- [ ] Test portal ID in different contexts (API calls, localStorage)
- [ ] Check if portal context persists across origins

### Endpoint Testing
- [ ] POST to `/frontend/observability/page-tracking/store/` with various payloads
- [ ] Test error reporting endpoints for injection
- [ ] Enumerate hublet-specific endpoints
- [ ] Test QA domain endpoints for differences

### Injection Testing
- [ ] XSS in console.error() messages
- [ ] XSS in URL parameters logged as breadcrumbs
- [ ] XSS in DOM element attributes (data-test-id, etc.)
- [ ] SSRF via error message URLs
- [ ] Header injection in Server-Timing parsing

### CHIRP Framework
- [ ] Trigger CHIRP errors to map services
- [ ] Collect service names and methods
- [ ] Test for direct RPC method invocation
- [ ] Look for CHIRP endpoints in other JS files

### Source Map Analysis
- [ ] Extract all 28 source files from .map
- [ ] Search for hardcoded secrets (API keys, tokens)
- [ ] Map out function logic for vulnerabilities
- [ ] Check for vulnerable library versions

---

## 📊 Information Leakage Summary

### What Error Reports Contain

Every error sent to `exceptions.hubspot.com` includes:

```json
{
  "portal_id": 123456,
  "hublet": "na1",
  "environment": "prod",
  "project": "deployable-name",
  "session_duration": 45000,
  "session_id": "...",
  "amplitude_session_id": "...",
  "correlation_id": "...",
  "user": {...},
  "breadcrumbs": [
    {"category": "navigation", "data": {"from": "...", "to": "..."}},
    {"category": "ui.click", "message": "button#submit"},
    {"category": "xhr", "data": {"method": "POST", "url": "...", "status_code": 200}}
  ],
  "stacktrace": {
    "frames": [
      {"filename": "...", "function": "...", "lineno": 123}
    ]
  }
}
```

**Sensitive Data Risk:**
- URLs may contain tokens in query params (despite redaction attempts)
- Breadcrumbs log all user actions
- Stack traces reveal code structure
- Session IDs link requests together

---

## 🔗 Cross-Reference with Other Assets

### Related Files to Analyze

If you find references to these in other JS files, prioritize them:

```
bpm:///chirp-client@*       // CHIRP RPC client code
bpm:///hubspot-auth@*       // Authentication logic
bpm:///api-client@*         // API wrapper code
bpm:///session-manager@*    // Session handling
```

### Grep Patterns for Reconnaissance

```bash
# Find CHIRP service calls
grep -r "chirp/" *.js

# Find API endpoints
grep -rE "(https?://[a-z0-9-]+\.hubspot[^\"']*)" *.js

# Find authentication headers
grep -rE "(Authorization|X-Auth|X-Token)" *.js

# Find localStorage usage
grep -r "localStorage\." *.js
```

---

## 🎓 Key Takeaways for Bug Bounty

1. **Error monitoring systems are goldmines** - They reveal internal architecture, endpoints, and data flows

2. **Source maps = free code review** - Download them to find vulnerabilities in original source

3. **Environment switching = attack surface expansion** - QA environments often have weaker security

4. **Client-side storage = potential privilege escalation** - localStorage controls can bypass server checks

5. **Internal frameworks = unique vulnerabilities** - CHIRP is custom to HubSpot, so standard tools won't catch issues

6. **Correlation IDs = session tracking** - Test for IDOR and session hijacking

7. **Portal IDs = multi-tenant isolation** - Breaking portal isolation is a critical finding

---

## 📝 Report Template

If you find a vulnerability based on this recon:

```markdown
**Title:** [Specific Vulnerability] via Error Monitoring Infrastructure

**Severity:** [Critical/High/Medium/Low]

**Asset:** exceptions.hubspot.com or app.hubspot.com

**Description:**
Analysis of HubSpot's client-side error monitoring bundle (head-dlb.bundle.production.js)
revealed that [specific finding]. By [exploitation method], an attacker can [impact].

**Proof of Concept:**
1. Navigate to https://app.hubspot.com
2. Open browser console
3. [Steps to reproduce]
4. Observe: [expected result]

**Impact:**
[Specific impact: data access, privilege escalation, etc.]

**Remediation:**
[Specific fix recommendation]

**References:**
- head-dlb.bundle.production.js (analyzed Oct 15, 2025)
- [Relevant OWASP/CWE references]
```

---

**Analysis by Chavvo - Bug Bounty Edition**
**Methodology:** Client-side reconnaissance via static analysis, source map extraction, endpoint discovery, and architecture mapping
**Next Phase:** Active testing of discovered attack surfaces
