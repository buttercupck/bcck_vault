# Track B: Source Map Analysis - Findings Report

**Date:** 2025-10-17
**Analyst:** Chavvo
**Source Maps Analyzed:** 2 (apollo.bundle, head-dlb.bundle)
**Total Source Files Extracted:** 185 files (157 + 28)
**Total Lines Analyzed:** 23,696 lines

---

## Executive Summary

Extracted and analyzed 185 source files from HubSpot's production JavaScript bundles. While no critical secrets (API keys, tokens) were found hardcoded, the analysis revealed significant architectural intelligence including CHIRP RPC error handling, Portal ID extraction mechanisms, error reporting infrastructure, and localStorage-based configuration systems.

---

## HIGH SEVERITY FINDINGS

### 1. Error Reporting Infrastructure Exposed

**Type:** Information Disclosure
**File:** `head-dlb-indexed.js:2683`
**Severity:** Medium-High
**Confidence:** High

**Finding:**
```javascript
if (uri.host === 'exceptions.hubspot.com') {
  var hubletSuffix = hublet === 'na1' ? '' : `-${hublet}`;
  var envSuffix = env === 'prod' ? '' : `${env}`;
```

**Details:**
- Confirmed error reporting endpoint: `exceptions.hubspot.com`
- Dynamic construction based on hublet (na1, eu1, etc.) and environment (prod, qa)
- Patterns: `exceptions[-{hublet}].hubspot[{env}].com`

**Attack Vectors:**
- Test error injection for XSS/SSRF
- Enumerate hublet-specific endpoints
- Access QA environment endpoints for weaker security
- Information disclosure through error messages

**Recommended Tests:**
```bash
# Test error endpoints
curl -X POST https://exceptions.hubspot.com/frontend/observability/page-tracking/store/ \
  -H "Content-Type: application/json" \
  -d '{"test":"payload"}'

# Test hublet variations
curl -X POST https://exceptions-eu1.hubspot.com/...
curl -X POST https://exceptions.hubspotqa.com/...
```

---

### 2. CHIRP RPC Error Enhancement Framework

**Type:** Internal Architecture Disclosure
**File:** `head-dlb-indexed.js:1004-1860`
**Severity:** Medium
**Confidence:** High

**Finding:**
Complete CHIRP RPC error handling framework exposed in source including:
- Error detection patterns
- Service name extraction
- Method name extraction
- Error type classification
- Structured metadata attachment

**Key Code Sections:**

```javascript
// CHIRP error detection
_isChirpError: function (error) {
  return (error.message.includes('CHIRP RPC failed')) ||
    this._hasChirpErrorStructure(error) ||
    this._containsChirpErrorInstance(error)
}

// Error enhancement
_enhanceChirpError: function (error) {
  const chirpContext = this._extractChirpContext(error);
  if (chirpContext) {
    this.setExtraContext({
      chirpServiceName: chirpContext.serviceName,
      chirpMethodName: chirpContext.methodName,
      chirpErrorType: chirpContext.errorType,
      chirpUserDefinedError: chirpContext.userDefinedError,
```

**Attack Implications:**
- ==Map internal microservices by triggering CHIRP errors==
- Enumerate service methods
- Test for IDOR via service/method manipulation
- Identify internal RPC call patterns

**Recommended Actions:**
1. Grep all HubSpot JS files for `CHIRP RPC failed` patterns
2. Trigger errors to enumerate services in error responses
3. Test direct RPC method invocation if endpoints are discovered
4. Monitor error responses for service name leakage

---

### 3. Portal ID Extraction Implementation

**Type:** Multi-Tenant Isolation Logic Disclosure
**File:** `head-dlb-indexed.js:4500-4545` (PortalIdParser@2.291)
**Severity:** High
**Confidence:** High

**Finding:**
Complete Portal ID extraction logic exposed:

```javascript
// Regex patterns
pathRegex: /^\/(?:[A-Za-z0-9-_]*)\/(\d+)(?:\/|$)/,
queryParamRegex: /(?:\?|&)portalid=(\d+)/i,

// Extraction methods
getPortalIdFromPath(regex) {
  return this.parsePortalIdFromString(document.location.pathname, regex);
}

getPortalIdFromQueryParam() {
  return this.parsePortalIdFromString(document.location.search, this.queryParamRegex);
}

// Global assignment
if (window.hubspot.portal.id == null) {
  window.hubspot.portal.id = id;
}
```

**Attack Vectors:**
- **IDOR Testing:** Change portal ID in URL path or query params
- **Edge Case Testing:** Try portal ID values: -1, 0, 1, 999999999, null, undefined
- **Context Bypass:** Test if portal context persists across origins
- **Injection:** Test for injection in portal ID field

**Critical Test Cases:**
```bash
# URL path manipulation
https://app.hubspot.com/contacts/123456/...  → change 123456
https://app.hubspot.com/contacts/0/...       → test zero
https://app.hubspot.com/contacts/-1/...      → test negative

# Query param manipulation
?portalid=123456 → ?portalid=999999999
```

**Potential Impact:**
Breaking portal isolation = access to other customers' data (CRITICAL finding)

---

## MEDIUM SEVERITY FINDINGS

### 4. localStorage Configuration System

**Type:** Client-Side Configuration Exposure
**Files:** Multiple locations
**Severity:** Medium
**Confidence:** High

**Finding:**
localStorage keys used for environment control:

```javascript
// DEBUG flag manipulation
localStorage.setItem(`${service.toUpperCase()}_DEBUG`, JSON.stringify(true));
localStorage.setItem('DEBUG', JSON.stringify(val));

// Session tracking
var hmplData = _window.localStorage.getItem('__hmpl');

// Generic localStorage access
result = window.localStorage.getItem(key);
```

**Discovered Keys:**
- `DEBUG` - Enable verbose logging
- `{SERVICE}_DEBUG` - Service-specific debug mode
- `__hmpl` - Amplitude analytics session (contains session_id)

**Attack Vectors:**
1. **Debug Mode Exploitation:**
   ```javascript
   localStorage.setItem('DEBUG', 'true');
   location.reload();
   ```
   - Check for exposed endpoints
   - Monitor for verbose error messages
   - Look for development-only features

2. **Session Manipulation:**
   - Test session fixation via `__hmpl` manipulation
   - Check if localStorage session overrides server session

3. **Environment Switching:**
   Based on documentation patterns (ENV, HUBLET, DEPLOYED keys mentioned in analysis docs but not found hardcoded)

**Recommended Tests:**
```javascript
// In browser console on app.hubspot.com
localStorage.setItem('DEBUG', 'true');
localStorage.setItem('ENV', 'qa');  // If key exists
localStorage.setItem('HUBLET', 'eu1');
location.reload();
// Monitor Network tab for changes
```

---

## INFORMATIONAL FINDINGS

### 5. Module System Architecture

**Type:** Build System Information
**Severity:** Low
**Confidence:** High

**Finding:**
Internal module system exposed:

```javascript
_hubspot.default.modules.useGlobals = ns =>
  ns !== 'raven-hubspot/configure' &&
  ns !== 'PortalIdParser' &&
  ns !== 'enviro';

_hubspot.default.define('PortalIdParser', [], () => {
  const PortalIdParserModule = require('PortalIdParser');
  return PortalIdParserModule.default || PortalIdParserModule;
});
```

**Intelligence Value:**
- Internal package names: `PortalIdParser@2.291`, `raven-hubspot`, `enviro`
- Module loading patterns
- BPM package manager usage confirmed

---

## NEGATIVE FINDINGS (No Results)

The following high-value patterns were NOT found (which is good security):

- ❌ API keys (32-64 char patterns)
- ❌ Authentication tokens
- ❌ Sentry DSN
- ❌ Ably API keys
- ❌ AWS access keys (AKIA...)
- ❌ Private keys (PEM format)
- ❌ Hardcoded GraphQL endpoints
- ❌ Direct URLs to internal APIs

This suggests:
1. Good secrets management (not hardcoding credentials)
2. Configuration loaded at runtime from server
3. Endpoints constructed dynamically

---

## PRIORITY TESTING MATRIX

### Critical Priority (Test First)

| # | Finding | Test | Potential Impact |
|---|---------|------|------------------|
| 1 | Portal ID extraction | IDOR across portals | Access other customer data |
| 2 | CHIRP RPC framework | Service enumeration | Internal API discovery |
| 3 | exceptions.hubspot.com | Error injection | XSS/SSRF via error reporting |

### High Priority

| # | Finding | Test | Potential Impact |
|---|---------|------|------------------|
| 4 | DEBUG localStorage | Environment manipulation | Access debug features |
| 5 | __hmpl session tracking | Session fixation | Session hijacking |
| 6 | Hublet enumeration | Subdomain discovery | Find QA/dev environments |

---

## RECOMMENDED NEXT STEPS

### Immediate Actions

1. **Portal ID IDOR Testing** (CRITICAL)
   ```bash
   # Capture legitimate portal ID from authenticated session
   # Test manipulation in:
   # - URL paths: /contacts/{portalId}/...
   # - Query params: ?portalid=
   # - API requests
   ```

2. **CHIRP Service Mapping**
   ```bash
   # Search all HubSpot JS bundles for CHIRP patterns
   curl -s https://app.hubspot.com | rg "CHIRP RPC failed"

   # Trigger errors to enumerate services
   # Monitor error responses for service/method names
   ```

3. **Error Endpoint Testing**
   ```bash
   # Test exceptions.hubspot.com endpoints
   # Try injection payloads
   # Enumerate hublet variations
   ```

### Secondary Actions

4. **localStorage Manipulation**
   - Test DEBUG mode exploitation
   - Test session fixation via __hmpl
   - Check for ENV/HUBLET keys (from docs)

5. **Source Map Deep Dive**
   - Extract and read full source files (185 files)
   - Look for commented-out code with secrets
   - Map all service clients and API patterns

---

## FILES GENERATED

The following files were created during this analysis:

```bash
apollo-sources.js          # 18,496 lines - all apollo bundle sources concatenated
head-dlb-sources.js        # 5,200 lines - all head-dlb bundle sources
apollo-indexed.js          # Indexed with file names for tracking findings
head-dlb-indexed.js        # Indexed with file names for tracking findings
```

**Usage:**
```bash
# Search all sources for a pattern
rg "pattern" *-indexed.js

# Find which file a finding is from
grep -B 1 "finding text" *-indexed.js | grep "FILE:"
```

---

## TOOLS & TECHNIQUES USED

- **jq** - JSON parsing and source extraction from .map files
- **ripgrep (rg)** - High-speed regex pattern matching
- **curl** - HTTP testing
- **Custom regex patterns** - Secret detection patterns

---

## CONFIDENCE LEVELS

- **High Confidence:** Portal ID logic, CHIRP framework, exceptions.hubspot.com, localStorage usage
- **Medium Confidence:** Impact estimates for findings (need manual testing to confirm exploitability)
- **Low Confidence:** N/A (all findings backed by source code evidence)

---

## CONCLUSION

While no critical hardcoded secrets were discovered, the source map analysis revealed extensive architectural intelligence that significantly reduces the reconnaissance effort for bug bounty testing. The exposed Portal ID extraction logic, CHIRP RPC error handling, and error reporting infrastructure provide concrete attack vectors to test.

**Highest Value Finding:** Portal ID extraction logic → Test for multi-tenant IDOR

**Next Phase:** Move to authenticated testing with cookies to validate these findings against live endpoints.

---

**Analysis Complete:** 2025-10-17
**Time Investment:** ~30 minutes (automated)
**ROI:** High - Discovered 3 critical/high testing vectors without any manual code review
