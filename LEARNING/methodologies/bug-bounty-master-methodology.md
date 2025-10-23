# Bug Bounty Master Methodology
## From $100K+ Earning Researchers

**Date Created**: 2025-10-23
**Sources**:
- Video 1: Cookie Counterfeiting/Privilege Hijacking (Namcon Talk)
- Video 2: AI-Assisted Frontend Hacking (XSS Doctor)

**Application**: HubSpot Bug Bounty Research

---

## Table of Contents
1. [Cookie Counterfeiting Methodology](#cookie-counterfeiting-methodology)
2. [AI-Assisted JavaScript Analysis](#ai-assisted-javascript-analysis)
3. [Combined Attack Strategy](#combined-attack-strategy)
4. [HubSpot-Specific Application](#hubspot-specific-application)
5. [Tools & Scripts](#tools--scripts)
6. [Success Checklist](#success-checklist)

---

# Cookie Counterfeiting Methodology

## Overview
**"The most undervalued bug class in bug bounty"** - Found on EVERY program tested, $100K+ in 2 years.

### The Core Concept
Chain low-severity XSS on subdomains with cookie manipulation to achieve critical impact. Turn "crumbs into crits."

### Why It's Undervalued
- XSS on unimportant subdomains usually gets rated LOW or INFORMATIONAL
- Researchers don't chain it with the real impact
- Programs don't realize subdomain XSS can affect main app authentication

---

## Attack Pattern: Cookie Counterfeiting

### Requirements Checklist
- [ ] **XSS on ANY subdomain** (even "unimportant" ones)
- [ ] **Authenticated endpoint** with state-changing actions
- [ ] **Duplicate cookie handling** - Server doesn't validate which cookie it uses
- [ ] **Impact target** - Payment, profile, sensitive data

### How Cookies Work (Refresher)
```
Cookie Attributes:
- Domain: .example.com (wildcard - sent to all subdomains)
- Path: / or /specific/path
- Name: sessionId

Browser Behavior:
- Multiple cookies with SAME NAME are allowed
- Browser sends cookie with MOST SPECIFIC path first
- Server often uses FIRST cookie it receives
```

### The Attack Flow

#### Step 1: Find XSS on Subdomain
```
Target subdomains:
- errors.target.com
- static.target.com
- cdn.target.com
- old.target.com
- qa.target.com
- Any subdomain with reflection
```

Test vectors:
- Reflected XSS in error messages
- Stored XSS in headers, referer
- DOM-based XSS in URL parsing
- PostMessage XSS

#### Step 2: Identify Target Endpoint
Look for authenticated endpoints that:
- Accept data from user
- Associate data with account
- Have business impact

Examples:
- Payment information submission
- Profile updates
- Contact/CRM data creation
- Meeting/calendar invitations
- Cryptocurrency deposit addresses

#### Step 3: Test Cookie Duplication
```javascript
// Via XSS payload on subdomain.target.com
document.cookie = "sessionId=ATTACKER_SESSION; domain=.target.com; path=/";

// Now victim has TWO sessionId cookies:
// 1. Their legitimate cookie
// 2. Attacker's cookie (set via XSS)
```

#### Step 4: Determine Which Cookie Server Uses
Method: Remove cookies one at a time in DevTools

```bash
# In browser DevTools:
1. Open authenticated page
2. Delete cookies one at a time
3. Refresh after each deletion
4. Note which deletion causes 401/403
5. That's the cookie the server validates
```

If server uses FIRST cookie → Attack works! ✅

#### Step 5: Build Attack Chain
```
1. Victim visits attacker-controlled page
2. Page loads iframe: https://subdomain.target.com/xss?payload=...
3. XSS executes: document.cookie = "sessionId=ATTACKER; domain=.target.com"
4. Page redirects victim to target action: https://target.com/deposit
5. Victim fills in deposit info (crypto address, bank details, etc)
6. Server receives: sessionId=ATTACKER (first cookie)
7. Server associates victim's data with ATTACKER's account
8. Attacker now has victim's payment info / crypto sent to attacker
```

---

## Real-World Examples (From Video)

### Example 1: Cryptocurrency Exchange
**Attack**: Victim deposits crypto, but address is attacker's

**Flow**:
1. XSS on `errors.cryptoexchange.com`
2. Sets attacker's session cookie
3. Victim navigates to `/deposit`
4. Victim's deposit address shown is ATTACKER's address
5. Victim deposits $10,000 in crypto
6. Goes to attacker's wallet

**Impact**: Direct financial theft
**Bounty**: Critical severity

### Example 2: Meeting Platform
**Attack**: Force victim into attacker's meeting room

**Flow**:
1. XSS on subdomain sets attacker's meeting session
2. Victim clicks "Join Meeting" link
3. Desktop client opens in ATTACKER's meeting
4. Attacker sees victim's webcam, screen share
5. Victim thinks they're in their own private meeting

**Impact**: Privacy violation, corporate espionage
**Bounty**: High severity

### Example 3: E-Commerce Platform
**Attack**: Victim's credit card added to attacker's account

**Flow**:
1. XSS sets attacker's session
2. Victim tries to purchase something
3. Enters credit card details
4. Card saved to ATTACKER's account
5. Attacker can now use victim's card

**Impact**: Payment fraud
**Bounty**: Critical severity

---

## Finding Cookie Counterfeiting Vulnerabilities

### Step-by-Step Process

#### 1. Subdomain Enumeration
```bash
# Use tools:
subfinder -d target.com
amass enum -d target.com
assetfinder target.com

# Or from source code (what we did for HubSpot):
grep -r "\.hubspot\.com" extracted/
```

#### 2. XSS Hunting on Subdomains
Focus on:
- Error pages (404, 500, custom errors)
- Search functionality
- URL parameter reflection
- Headers (User-Agent, Referer) reflection
- Old/deprecated endpoints

Quick test payloads:
```html
"><script>alert(document.domain)</script>
'><svg/onload=alert(1)>
javascript:alert(1)
```

#### 3. Identify Authenticated Endpoints
```bash
# From browser DevTools, capture requests to:
- /api/* endpoints
- GraphQL endpoints
- RPC/internal service calls
- Form submissions
- AJAX requests

# Note which cookies are sent with each request
```

#### 4. Test Cookie Handling
```javascript
// In DevTools Console on main domain:
document.cookie = "testcookie=value1; path=/; domain=.target.com";
document.cookie = "testcookie=value2; path=/; domain=target.com";

// Then inspect request headers to see which is sent first
// Use Network tab → Request Headers → Cookie
```

#### 5. Validate Server Behavior
```bash
# Test scenarios:
1. No session cookie → 401 Unauthorized
2. Valid session cookie → 200 OK
3. Valid + Invalid cookie (both with same name) → ???

# If #3 = 200 OK → Server uses first cookie → VULNERABLE ✅
```

---

# AI-Assisted JavaScript Analysis

## Overview
**"Don't look for vulnerabilities, look for functionality first"** - XSS Doctor

Master the app before hunting bugs. Use AI to reduce friction and speed up analysis 10x.

---

## The Methodology

### Phase 1: Fingerprinting
**Before diving into code**, understand the stack.

Questions to answer:
- What framework? (React, Vue, Angular, vanilla JS)
- What libraries? (Apollo, Axios, jQuery)
- What bundler? (Webpack, Vite, Rollup)
- What services? (GraphQL, REST, RPC)
- Is it obfuscated?

**AI Prompt**:
```
You are a web security researcher analyzing a target application.

Based on this JavaScript bundle/file, identify:
1. Framework/library used
2. Bundler configuration
3. Major dependencies
4. Architecture pattern (SPA, MPA, etc)
5. API communication methods

Provide a concise tech stack summary.
```

### Phase 2: Deobfuscation
If code is webpack-packed or minified, extract source files.

**Tools**:
- Source maps (if available) - BEST option
- `extract-source-maps` npm package
- Manual webpack extraction
- AI deobfuscation

**AI Prompt for Obfuscated Code**:
```
You are an expert JavaScript analyst.

This code is obfuscated/minified. Please:
1. Deobfuscate and reformat it
2. Add meaningful variable names
3. Add comments explaining logic
4. Identify the purpose of each function

Provide clean, readable code.
```

### Phase 3: Functionality Mapping
**CRITICAL**: Map ALL functionality before looking for bugs.

Create a table of contents of the app:
- All endpoints (API calls)
- All user interactions
- All data flows
- All authentication mechanisms

**AI Prompt (Use with large context models like Gemini 2.0)**:
```
You are a JavaScript security analyst.

Analyze this entire JavaScript file and create a comprehensive functionality map.

For each major function/module, provide:
1. Function name and line number
2. One-sentence purpose
3. Inputs/outputs
4. API endpoints called
5. Security implications

Format as a markdown table.
```

**Why This Works**:
- Models like Gemini 2.0 have 1M+ token context
- Can analyze entire 50K+ line files at once
- Faster than manual review
- Catches functionality you'd miss

### Phase 4: Endpoint Extraction
Extract ALL API endpoints for testing.

**AI Prompt**:
```
You are a penetration tester analyzing client-side code.

Extract ALL endpoints from this code including:
- GraphQL queries/mutations
- REST API calls
- WebSocket endpoints
- RPC/internal service calls
- External requests

For each endpoint provide:
| Endpoint | Method | Parameters | Auth Required | Purpose |
```

### Phase 5: Gadget Hunting
Now hunt for specific vulnerability types.

**AI Prompts by Vulnerability Class**:

#### XSS Gadgets
```
You are an XSS specialist.

Find all potential XSS sinks in this code:
- innerHTML, outerHTML
- document.write
- eval, Function, setTimeout (with string args)
- dangerouslySetInnerHTML (React)
- Template literals with user input
- URL assignments (location.href =)

For each finding:
1. Line number
2. Sink type
3. Code snippet
4. Data flow from user input
5. Exploitability (High/Medium/Low)
```

#### PostMessage Vulnerabilities
```
Find all postMessage handlers in this code.

For each:
1. Does it validate origin?
2. What data does it accept?
3. What actions does it perform?
4. Is data sanitized before use?

Assess exploitability.
```

#### Client-Side Path Traversal
```
Find file/path operations in this code:
- File reads/writes
- Path construction from user input
- URL building with user data

Assess if path traversal is possible.
```

---

## Tools Mentioned in Video

### Fabric (Daniel Miessler)
AI prompt pattern system for content analysis.

```bash
# Install
go install github.com/danielmiessler/fabric@latest

# Use pattern for JS analysis
fabric -p analyze_code < source.js

# Custom pattern for security
fabric -p xss_gadget_hunt < bundle.js
```

### Custom Scripts
**get-webpack** - Download all webpack chunks
```bash
# Concept (from video):
1. Load app in browser
2. Open DevTools → Network
3. Capture all .js file URLs
4. Download each one
5. Save to local directory for analysis
```

### AI Models Recommended
- **Gemini 2.0 Flash** - 1M token context window (BEST for large files)
- **Claude Sonnet 4.5** - Best for security analysis
- **GPT-4** - Good alternative
- **ChatGPT Operator** - Can click around app for you

---

## Advanced Techniques

### Dynamic Analysis
While AI analyzes static code, use browser to:
1. Click every button
2. Fill every form
3. Navigate every page
4. Trigger every error
5. Monitor Network tab

**Fabric Pattern** (from video):
```
Create a "js_collab" pattern that:
1. Analyzes JavaScript file
2. Outputs:
   - Summary
   - Tech stack
   - Endpoints
   - Security concerns
   - Suggested test vectors
```

### Combining Static + Dynamic
```
1. AI analyzes source → finds all endpoints
2. You test each endpoint manually
3. AI analyzes responses → finds reflection
4. You craft exploit
5. AI helps document vulnerability
```

---

# Combined Attack Strategy

## Methodology: Cookie Counterfeiting + AI Analysis

### The Workflow

#### Stage 1: Intelligence Gathering (AI-Powered)
```
1. Extract all JavaScript bundles
2. Feed to AI for functionality mapping
3. Generate endpoint catalog
4. Identify authentication mechanisms
5. Map cookie usage patterns
```

**Deliverable**: Complete app architecture document

#### Stage 2: Gadget Hunting (AI-Assisted)
```
1. AI finds all XSS sinks
2. AI maps data flow to sinks
3. You validate exploitability
4. Document all XSS vectors
```

**Deliverable**: XSS gadget catalog with PoCs

#### Stage 3: Cookie Analysis (Manual + AI)
```
1. AI finds all cookie read/write operations
2. You test cookie validation in browser
3. Identify which cookies are actually validated
4. Map duplicate cookie behavior
```

**Deliverable**: Cookie validation flow diagram

#### Stage 4: Attack Chain Construction
```
1. Match XSS locations with cookie targets
2. Identify high-impact authenticated endpoints
3. Build PoC exploit chain
4. Test full attack flow
```

**Deliverable**: Working exploit + video PoC

#### Stage 5: Bug Bounty Submission
```
1. Document vulnerability chain
2. Explain chaining (XSS + Cookie = Critical)
3. Provide business impact assessment
4. Include remediation steps
5. Submit with PoC
```

**Deliverable**: $$$$ bounty payment

---

# HubSpot-Specific Application

## Current State of Research

### What We Have ✅
- ✅ 47,211 lines of extracted JavaScript
- ✅ Apollo GraphQL client code
- ✅ CHIRP RPC framework code
- ✅ Error handling code
- ✅ Complete schema (777 types)
- ✅ Known subdomains
- ✅ Authentication endpoints

### What We Need ❓
- ❓ XSS on HubSpot subdomain
- ❓ Cookie validation flow understanding
- ❓ Exploitable authenticated endpoint
- ❓ Proof that cookie counterfeiting works

---

## HubSpot Attack Plan

### Phase 1: Complete Source Analysis (THIS WEEK)

#### Task 1.1: AI-Powered Functionality Mapping
```
Files to analyze:
- apollo-sources.js (18,496 lines)
- head-dlb-sources.js (5,200 lines)

AI Prompt per file:
"Analyze this HubSpot production JavaScript and create:
1. Complete function catalog
2. All API endpoints
3. All GraphQL operations
4. Cookie handling logic
5. Error message rendering
6. Security-relevant patterns"

Tool: Claude or Gemini 2.0
Time: 2 hours
Output: hubspot-functionality-map.md
```

#### Task 1.2: XSS Gadget Extraction
```
AI Prompt:
"Find all XSS sinks in this HubSpot code:
- innerHTML/outerHTML
- document.write
- eval/Function
- URL assignments
- Template rendering
- Error message display

Provide line numbers and exploitability assessment."

Time: 1 hour
Output: hubspot-xss-gadgets.md
```

#### Task 1.3: Cookie Flow Analysis
```
Manual + AI:
1. AI extracts all cookie operations
2. Trace cookie validation logic
3. Map session management
4. Identify duplicate cookie handling

Time: 2 hours
Output: hubspot-cookie-analysis.md
```

### Phase 2: Live XSS Testing (NEXT WEEK)

#### Known HubSpot Subdomains to Test:
```
Priority 1 (From source code):
- exceptions.hubspot.com (error reporting)
- app-na2.hubspot.com (main app)

Priority 2 (To discover):
- *.qa.hubspot.com (QA environments from source)
- static.hubspot.com
- cdn.hubspot.com
```

#### Test Vectors by Target:

**exceptions.hubspot.com**:
```javascript
// From source: Error messages are sent here
// Test: Can we inject into error message?

Test payloads in:
- CHIRP RPC error messages
- GraphQL error responses
- Malformed requests
- Exception data fields
```

**GraphQL Endpoint**:
```graphql
# Test reflection in error messages
mutation {
  updateContact(input: {
    firstname: "<script>alert(1)</script>"
  })
}

# Check if error reflects unsanitized input
```

**CHIRP RPC**:
```bash
# From source: Error format is enhanced client-side
# Test if service/method names are reflected

POST /api/chirp-frontend-app/v1/gateway/TEST<script>alert(1)</script>/method
```

### Phase 3: Cookie Counterfeiting Testing

#### Test Scenario 1: GraphQL Mutation
```
Setup:
1. Find XSS on subdomain (from Phase 2)
2. Target: GraphQL contact creation

Attack:
1. XSS payload sets attacker's session cookie
2. Victim creates contact with their info
3. Contact associated with attacker's portal
4. Attacker now has victim's contact data

Impact: Horizontal privilege escalation
```

#### Test Scenario 2: CHIRP RPC Call
```
Setup:
1. XSS on subdomain
2. Target: Internal CHIRP service call

Attack:
1. Cookie counterfeiting
2. Victim's CHIRP request uses attacker's session
3. Data sent to attacker's account

Impact: Data exfiltration
```

#### Test Scenario 3: Presence API
```
Setup:
1. XSS on subdomain
2. Target: PUT /api/presence/v1/presence/...

Attack:
1. Cookie counterfeiting
2. Victim's presence update goes to attacker's portal
3. Attacker tracks victim's activity

Impact: Privacy violation
```

### Phase 4: Documentation & Submission

#### Report Structure:
```markdown
# [CRITICAL] Cookie Counterfeiting via Subdomain XSS → Account Takeover

## Summary
Chained XSS on [subdomain] with cookie counterfeiting to achieve
horizontal privilege escalation on HubSpot CRM.

## Vulnerability Chain

### Component 1: XSS on exceptions.hubspot.com
Severity (standalone): LOW
[Details of XSS]

### Component 2: Unvalidated Cookie Handling
Severity: INFO
Server accepts first cookie with name "hubspotapi" without
validating source/path specificity.
[Source code evidence]

### Component 3: Chained Impact
Severity: CRITICAL
Combined vulnerabilities allow attacker to:
1. Execute JS on subdomain
2. Set attacker's session cookie
3. Victim's GraphQL mutations associate with attacker account
4. Complete data exfiltration of victim's CRM

## Proof of Concept
[Step-by-step with screenshots/video]

## Impact
- Horizontal privilege escalation
- Cross-account data exfiltration
- PII exposure
- CRM data theft
- Affects all HubSpot users

## Remediation
1. Fix XSS on exceptions.hubspot.com
2. Validate cookie source on server-side
3. Implement SameSite=Strict on session cookies
4. Use separate session tokens per subdomain

## CVSS
9.1 (Critical)
```

---

# Tools & Scripts

## AI Analysis Scripts to Build

### 1. `ai_functionality_mapper.ts`
```typescript
// Purpose: Feed source files to AI, get functionality map
// Input: JavaScript file path
// Output: Markdown table of all functions/endpoints
// AI: Claude Sonnet 4.5 or Gemini 2.0
```

### 2. `ai_xss_gadget_hunter.ts`
```typescript
// Purpose: Find all XSS sinks via AI
// Input: JavaScript file path
// Output: List of potential XSS gadgets with line numbers
// AI: Claude (specialized for security)
```

### 3. `cookie_flow_tracer.ts`
```typescript
// Purpose: Trace cookie validation logic
// Input: Source files
// Output: Flow diagram of cookie handling
```

### 4. `hubspot_subdomain_xss_tester.ts`
```typescript
// Purpose: Automated XSS testing on HubSpot subdomains
// Input: List of subdomains, list of payloads
// Output: Report of successful XSS injections
```

### 5. `cookie_counterfeiting_tester.ts`
```typescript
// Purpose: Test if server accepts duplicate cookies
// Input: Target endpoint, session cookies
// Output: Vulnerability confirmation
```

## Manual Testing Checklist

### XSS Discovery Checklist
- [ ] Test all error pages (404, 500, custom)
- [ ] Test GraphQL error messages
- [ ] Test CHIRP RPC error messages
- [ ] Test URL parameter reflection
- [ ] Test header reflection (User-Agent, Referer)
- [ ] Test stored XSS in CRM fields (contact names, etc)
- [ ] Test DOM-based XSS from source gadgets

### Cookie Testing Checklist
- [ ] Identify all authentication cookies
- [ ] Test duplicate cookie behavior
- [ ] Test cookie domain scope (.hubspot.com vs hubspot.com)
- [ ] Test cookie path specificity
- [ ] Test SameSite attribute (if any)
- [ ] Test which cookie server actually validates
- [ ] Document cookie validation flow

### Attack Chain Checklist
- [ ] XSS PoC created and tested
- [ ] Cookie counterfeiting PoC tested
- [ ] Combined attack tested end-to-end
- [ ] Impact clearly demonstrated
- [ ] Business impact documented
- [ ] Remediation steps provided
- [ ] Video PoC recorded

---

# Success Checklist

## Research Phase ✅
- [x] Extract all JavaScript source (47K lines)
- [x] Create AI analysis plan
- [x] Identify XSS gadget patterns
- [ ] Complete AI-powered functionality mapping
- [ ] Complete cookie validation analysis
- [ ] Complete endpoint catalog

## Testing Phase 🎯
- [ ] Find XSS on HubSpot subdomain
- [ ] Confirm cookie counterfeiting is possible
- [ ] Identify high-impact target endpoint
- [ ] Build working exploit chain
- [ ] Record video PoC

## Submission Phase 💰
- [ ] Write comprehensive report
- [ ] Document vulnerability chain
- [ ] Calculate CVSS score
- [ ] Provide remediation recommendations
- [ ] Submit to HubSpot bug bounty
- [ ] Collect $$$$$ bounty

---

# Key Takeaways

## From Cookie Counterfeiting Talk

1. **"Turn crumbs into crits"** - Chain low-severity XSS with cookie attacks for critical impact
2. **Found on EVERY program** - This is underreported and undervalued
3. **$100K in 2 years** - Extremely lucrative when you know the pattern
4. **Subdomain XSS matters** - Don't dismiss XSS on "unimportant" subdomains
5. **Server validation is weak** - Many apps don't validate which cookie they use

## From AI-Assisted Hacking Talk

1. **"Master the app first"** - Don't hunt for bugs until you understand functionality
2. **AI reduces friction** - 10x faster analysis with AI assistance
3. **Use large context models** - Gemini 2.0 can analyze entire 50K line files
4. **Functionality → Gadgets → Exploits** - Work in phases
5. **Combine static + dynamic** - AI for code, manual for testing

## For HubSpot Research

1. **We have the source** - 47K lines of production JavaScript is gold
2. **CHIRP errors are interesting** - Error message manipulation found in code
3. **Cookie patterns exist** - Need to validate if counterfeiting works
4. **GraphQL is a target** - Mutations + cookie counterfeiting = data theft
5. **This is the path** - Follow both methodologies to find critical bug

---

# Timeline

## Week 1 (Current): Intelligence
- Complete AI-powered source analysis
- Map all functionality
- Find all XSS gadgets
- Understand cookie flow

## Week 2: Testing
- Test all subdomains for XSS
- Validate cookie counterfeiting
- Build attack chains
- Create PoCs

## Week 3: Submission
- Write report
- Record video
- Submit bug
- $$$ Profit

---

# Final Wisdom

**From the videos**:
> "I've been farming the heck out of this bug for years. When asked to speak at Namcon, I considered what's the single most valuable thing I could give up - and this was it."

**The opportunity**:
- Most researchers don't chain vulnerabilities
- Most programs undervalue subdomain XSS
- Most testing is automated and surface-level
- Deep manual analysis + chaining = high payouts

**Our advantage**:
- We have the source code (most don't)
- We have AI to speed up analysis (new technique)
- We understand the methodology (from $100K+ earners)
- We have multiple attack surfaces (GraphQL, CHIRP, REST)

**The path forward**:
1. Complete source analysis (AI-assisted)
2. Find XSS on subdomain (manual testing)
3. Chain with cookie counterfeiting (methodology)
4. Target high-impact endpoints (GraphQL mutations)
5. Submit critical finding ($$$$)

---

**Ready to execute. Let's turn these insights into a critical HubSpot finding.**
