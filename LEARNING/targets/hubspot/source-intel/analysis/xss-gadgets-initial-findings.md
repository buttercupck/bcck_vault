# XSS Gadget Hunt - Initial Findings
## HubSpot Source Code Analysis

**Date**: 2025-10-23
**Files Analyzed**: apollo-sources.js, head-dlb-sources.js (47,211 total lines)
**Methodology**: Pattern matching + manual code review

---

## Cookie Handling Patterns

### Finding 1: document.cookie Access
**Files**: head-dlb-sources.js, head-dlb-indexed.js
**Lines**: 625-629, 687

```javascript
// head-dlb-sources.js:625-629
function getSeleniumCookieValue() {
  try {
    if (!(document && document.cookie)) {
      return undefined;
    }
    const match = document.cookie.match(/hs_selenium=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : undefined;
  } catch (__err) {
    return undefined;
  }
}

// head-dlb-sources.js:687
isAcceptanceTest = !!(document && document.cookie && document.cookie.includes('hs_selenium'));
```

**Analysis**:
- Cookies are accessed but only for reading
- Pattern shows defensive coding (try/catch)
- Looking for `hs_selenium` cookie specifically
- **No direct XSS vector** BUT confirms cookie access patterns

**Relevance to Cookie Counterfeiting**:
- ✅ Confirms JavaScript can read `document.cookie`
- ✅ Pattern matching on cookies is used
- ⚠️ Need to find WHERE session cookies are validated
- 🎯 **ACTION**: Search for `hubspotapi` cookie validation

---

## location.href Usage Patterns

### Finding 2: URL Tracking & Navigation
**Files**: head-dlb-sources.js
**Lines**: 1035, 2172, 2590, 2926, 3784

```javascript
// head-dlb-sources.js:1035
this._lastHref = this._location && this._location.href;

// head-dlb-sources.js:2172
var parsedLoc = parseUrl(this._location.href);

// head-dlb-sources.js:2590
var currentHref = self._location.href;

// head-dlb-sources.js:2926
httpData.url = redactSensitiveUrlParams(_document.location.href);

// head-dlb-sources.js:3784
return document.location.href;
```

**Analysis**:
- Multiple reads of `location.href` for tracking
- **INTERESTING**: `redactSensitiveUrlParams()` function exists
- URL parsing happens frequently
- Mostly READS, not dangerous assignments

**Potential Vectors**:
- ❌ No `location.href = userInput` patterns found (safe)
- ✅ URL parsing could have injection points
- 🎯 **ACTION**: Find `redactSensitiveUrlParams` implementation
- 🎯 **ACTION**: Search for URL parameter reflection

---

## Dangerous Sinks Found

### Finding 3: window.open / assign / replace Usage
**Files**: All 4 files matched
**Status**: PENDING DETAILED ANALYSIS

**Next Steps**:
1. Extract exact usages of these sinks
2. Check if user input flows into them
3. Trace data flow from URL params → sinks

---

## Missing Patterns (Not Found Yet)

❌ **innerHTML / outerHTML** - Not found in initial grep
❌ **document.write** - Not found
❌ **dangerouslySetInnerHTML** - Not found
❌ **postMessage handlers** - Not found in initial grep
❌ **eval()** - Not found in initial grep

**Interpretation**:
- HubSpot frontend appears relatively hardened
- React/Apollo stack likely uses safe rendering
- May need to look for:
  - Template injection in GraphQL responses
  - Unsafe JSON parsing
  - Client-side routing XSS
  - Proto type pollution

---

## Next Analysis Tasks

### Priority 1: Cookie Session Validation
```bash
grep -n "hubspotapi\|X-HubSpot-CSRF\|sessionId" extracted/*.js
```
**Goal**: Find WHERE authentication cookies are validated

### Priority 2: GraphQL Response Handling
```bash
grep -n "response\.data\|query\.data\|mutation\.data" extracted/apollo*.js
```
**Goal**: See if GraphQL responses are rendered unsafely

### Priority 3: Error Message Rendering
```bash
grep -n "error\.message\|errorMessage\|err\.toString" extracted/*.js
```
**Goal**: Find if error messages from server are reflected

### Priority 4: PostMessage Handlers (Deeper Search)
```bash
grep -n "window.*message\|parent\.postMessage\|iframe" extracted/*.js
```
**Goal**: Find cross-frame communication

### Priority 5: URL Parameter Usage
```bash
grep -n "URLSearchParams\|getParameter\|query\[" extracted/*.js
```
**Goal**: Find where URL params are used

---

## Attack Surface Map (From Videos)

### Cookie Counterfeiting Requirements:
1. ✅ **XSS on subdomain** - NEED TO FIND
2. ⚠️ **Cookie manipulation** - document.cookie access confirmed
3. ⚠️ **Authenticated endpoint** - GraphQL/CHIRP/Presence known
4. ❓ **Server validation weakness** - NEED TO TEST

### Subdomain XSS Hunting Priorities:
Based on previous research, test these for XSS:
- `exceptions.hubspot.com` - Error reporting endpoint
- `app-na2.hubspot.com` - Main app
- Any QA/dev subdomains found in source

### Test Vectors:
1. **Error injection**: Send malformed requests to CHIRP → check error reflection
2. **GraphQL errors**: Malformed queries → check error messages
3. **URL reflection**: Test all URL params for reflection
4. **Stored XSS**: Contact names, company names, custom properties

---

## Recommendations for Next Phase

### Immediate Actions:
1. ✅ Run Priority grep searches above
2. 📝 Create detailed gadget catalog with line numbers
3. 🧪 Start testing live subdomains for XSS
4. 🔍 Analyze GraphQL/Apollo response rendering code

### Tools to Build:
1. **xss_gadget_extractor.ts** - Automated gadget finder
2. **cookie_flow_tracer.ts** - Track cookie validation flow
3. **error_injector.ts** - Test error message reflection

### Success Metrics:
- [ ] Complete gadget catalog with exploitability ratings
- [ ] Cookie validation flow fully mapped
- [ ] At least 3 XSS test vectors identified
- [ ] Ready to start live testing phase

---

## Status: Phase 1 In Progress
**Next**: Deep dive into cookie validation + GraphQL response handling
