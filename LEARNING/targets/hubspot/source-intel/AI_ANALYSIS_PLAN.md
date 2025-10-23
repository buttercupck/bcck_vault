# HubSpot Source Code AI Analysis Plan
## Based on XSS Doctor + Cookie Counterfeiting Methodology

**Goal**: Systematically analyze 47,211 lines of extracted HubSpot source code to find XSS gadgets and chain them with cookie counterfeiting attacks.

---

## Phase 1: Functionality Mapping

### Target Files:
- `apollo-sources.js` (18,496 lines) - Apollo GraphQL client
- `head-dlb-sources.js` (5,200 lines) - Main DLB bundle
- `apollo-indexed.js` (18,341 lines) - Indexed version
- `head-dlb-indexed.js` (5,174 lines) - Indexed version

### AI Analysis Prompts:

#### Prompt 1: File Overview
```
You are an expert JavaScript security analyst and bug bounty hunter.

Analyze this JavaScript file from HubSpot's production bundle and provide:

1. ONE SENTENCE SUMMARY: What this file does
2. TECH STACK: Libraries, frameworks, patterns used
3. KEY FUNCTIONALITY: List all major functions/features (bullet points)
4. ENDPOINTS DISCOVERED: Any API endpoints, RPC calls, or external requests
5. SECURITY-RELEVANT CODE: Authentication, authorization, data handling
6. INTERESTING PATTERNS: Anything unusual or security-relevant

Format as markdown.
```

#### Prompt 2: Endpoint Mapping
```
You are a penetration tester analyzing client-side code for API endpoints.

Extract ALL endpoints from this code including:
- GraphQL queries/mutations
- REST API calls
- RPC/CHIRP service calls
- WebSocket connections
- PostMessage targets
- External requests

For each endpoint provide:
1. Endpoint URL/path
2. HTTP method
3. Parameters expected
4. Authentication mechanism
5. Purpose/functionality

Format as a table.
```

#### Prompt 3: XSS Gadget Hunting
```
You are an XSS specialist hunting for client-side vulnerabilities.

Analyze this code for XSS gadgets and sinks:

**DOM-Based XSS Sinks:**
- innerHTML, outerHTML
- document.write, document.writeln
- eval, Function, setTimeout, setInterval (with string args)
- location.href, location.assign, location.replace
- jQuery html(), append(), after(), etc.

**PostMessage Vulnerabilities:**
- window.addEventListener('message') without origin validation
- Unsafe message data handling

**Client-Side Path Traversal:**
- File/path operations on user input
- URL construction from user data

**DOM Clobbering:**
- Global variable access patterns
- document.getElementById without validation

For each finding provide:
1. Line number
2. Sink type
3. Code snippet
4. Exploitability assessment
5. Potential impact

Format as markdown with code blocks.
```

#### Prompt 4: Cookie/Session Handling
```
You are analyzing authentication and session management code.

Find all cookie-related code:
- Cookie reading (document.cookie, Cookie header)
- Cookie writing/setting
- Session token handling
- Authentication state management
- CSRF token usage

Look for:
1. Which cookies are used for authentication
2. How cookies are validated
3. Any cookie manipulation logic
4. Subdomain cookie behavior
5. Path-specific cookies

Assess if cookie counterfeiting is possible.
```

---

## Phase 2: XSS Subdomain Testing

### Subdomain Enumeration:
```bash
# Already known from research:
app-na2.hubspot.com
exceptions.hubspot.com
[QA environments from source]
```

### Test Vectors:
1. **Reflected XSS** - URL parameters, error messages
2. **Stored XSS** - Contact names, company names, custom properties
3. **DOM-Based XSS** - Using gadgets from Phase 1
4. **PostMessage XSS** - Using postMessage handlers from Phase 1

### Testing Checklist:
- [ ] Test error reporting endpoint (exceptions.hubspot.com)
- [ ] Test CHIRP error messages with XSS payloads
- [ ] Test GraphQL error responses
- [ ] Test subdomain reflection in responses
- [ ] Test custom property fields for storage

---

## Phase 3: Cookie Counterfeiting Attack Chain

### Requirements (from Video 1):
1. ✅ XSS on subdomain (to be found in Phase 2)
2. ✅ Authenticated endpoint with impact (GraphQL mutations, CHIRP RPC, Presence API)
3. ⚠️ Server doesn't validate specific cookie source

### Testing Methodology:

#### Step 1: Identify Target Cookies
```bash
# From headers.md - known cookies:
X-HubSpot-CSRF-hubspotapi
hubspotapi (session cookie)
[Other cookies from analysis]
```

#### Step 2: Test Cookie Duplication
```javascript
// Via XSS payload:
document.cookie = "hubspotapi=ATTACKER_SESSION; path=/; domain=.hubspot.com";
```

#### Step 3: Test Which Cookie Server Uses
```bash
# Remove cookies one at a time
# Send request to authenticated endpoint
# See if still authenticated
# Identify which cookie is actually validated
```

#### Step 4: Build Attack Chain
```
1. Find XSS on subdomain
2. XSS sets attacker's session cookie
3. Victim navigates to authenticated endpoint
4. Victim's action associates with attacker account
```

### High-Impact Targets:
- **GraphQL Mutations**: Contact creation, company updates, user modifications
- **CHIRP RPC**: Internal service calls with state changes
- **Presence API**: User status, location tracking
- **Payment/Billing**: If accessible (check source code)

---

## Phase 4: Attack Chain Documentation

### For Bug Bounty Submission:

```markdown
# [CRITICAL] Cookie Counterfeiting + XSS Chain Leading to [IMPACT]

## Summary
Chained low-severity XSS on [subdomain] with cookie counterfeiting to achieve [impact].

## Vulnerability Chain

### Finding 1: XSS on [subdomain]
- Severity if standalone: LOW/INFO
- [Details]

### Finding 2: Unvalidated Cookie Handling
- [Details from source analysis]

### Finding 3: Chained Impact
- Severity: CRITICAL
- Impact: [Account takeover/data exfiltration/privilege escalation]

## Proof of Concept
[Step-by-step reproduction]

## Impact
[Business impact assessment]

## Remediation
1. Fix XSS on subdomain
2. Validate specific cookie source server-side
3. Implement cookie SameSite attributes
```

---

## Tools & Resources

### AI Models to Use:
- **Claude (Sonnet 4.5)**: Best for security analysis
- **Gemini 2.0**: 1M token context for full file analysis
- **GPT-4**: Alternative for code analysis

### Analysis Scripts:
- Location: `LEARNING/targets/hubspot/source-intel/tools/`
- Create: `ai_analyze_sources.ts` - Systematic AI analysis runner
- Create: `xss_gadget_hunter.ts` - Extract XSS sinks from source
- Create: `cookie_tester.ts` - Test cookie counterfeiting

### Output Location:
- Analysis results: `source-intel/analysis/ai-analysis/`
- XSS findings: `source-intel/analysis/xss-gadgets.md`
- Cookie analysis: `source-intel/analysis/cookie-counterfeiting.md`

---

## Success Criteria

✅ Complete functionality map of all 47K lines
✅ All endpoints catalogued with auth mechanisms
✅ XSS gadgets identified with PoC code
✅ Cookie handling logic fully understood
✅ XSS found on HubSpot subdomain
✅ Cookie counterfeiting proven possible
✅ Attack chain documented with PoC
✅ Bug bounty submission ready

---

## Timeline Estimate

- Phase 1 (AI Analysis): 2-3 hours (mostly AI processing)
- Phase 2 (XSS Testing): 3-4 hours
- Phase 3 (Cookie Testing): 2-3 hours
- Phase 4 (Documentation): 1-2 hours

**Total**: 8-12 hours to potential critical finding

---

## Next Immediate Actions

1. ✅ Create this plan document
2. [ ] Create AI analysis runner script
3. [ ] Start Phase 1 with apollo-sources.js
4. [ ] Document all findings in real-time
5. [ ] Build attack chain as components discovered
