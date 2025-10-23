# HubSpot Attack Surface Discovery - Results
**Date**: 2025-10-23
**Status**: IN PROGRESS

---

## Phase 1: Port Scanning - COMPLETE ✅

### Tier 1 Priority Targets Scanned
- **Targets**: 9 high-priority subdomains
- **Ports Tested**: 21 high-value ports (SSH, databases, alt HTTP)
- **Results**: 36 open ports found

### Key Findings:

#### Alternate HTTP Ports (18 findings)
**Why Important**: Admin panels, debug endpoints, development servers

1. **developers.hubspot.com**
   - :8080 (HTTP alt)
   - :8443 (HTTPS alt)
   
2. **api.hubspot.com** 
   - :8080 (HTTP alt)
   - :8443 (HTTPS alt)

3. **api-na1.hubspot.com**
   - :8080 (HTTP alt)
   - :8443 (HTTPS alt)

4. **qa.growthgrader.hubspot.com** ⚠️ QA ENVIRONMENT
   - :8080 (HTTP alt)
   - :8443 (HTTPS alt)

#### Standard Ports (All targets)
- :80 (HTTP) - All 9 targets
- :443 (HTTPS) - All 9 targets

### No Critical Findings Yet:
- ❌ No exposed databases (3306, 5432, 27017, 6379)
- ❌ No SSH on unusual subdomains (22)
- ❌ No FTP (21)

---

## Phase 2: WebSocket Discovery - IN PROGRESS ⏳

### Status:
- Checked 5 Tier 1 targets for WebSocket indicators
- No WebSocket keywords found in initial HTML responses

### Next Steps:
- Check JavaScript files for ws:// or wss:// URLs
- Test common WebSocket paths (/ws, /websocket, /socket.io)
- Search source code bundles

---

## Phase 3: S3 Bucket Enumeration - STARTING

### Bucket Name Generation:
- Source: 1,044 live subdomains
- Pattern: {subdomain}-{env} (prod/dev/staging)
- Expected: ~5,000-10,000 potential bucket names

### Next Steps:
- Generate full bucket name list
- Test with s3scanner
- Search for S3 URLs in web responses
- Extract from JavaScript bundles

---

## Priority Testing Actions

### 🔴 HIGH PRIORITY - Test Now
1. **qa.growthgrader.hubspot.com:8080**
   - QA environment on alt port
   - May have debug endpoints, exposed APIs
   
2. **developers.hubspot.com:8080**
   - Developer portal on alt port
   - Could have API playgrounds, sandbox

3. **api.hubspot.com:8443**
   - API on alternate HTTPS port
   - May bypass some security controls

### 🟠 MEDIUM PRIORITY
4-9. Test remaining alt HTTP ports on other subdomains

---

## Statistics

| Phase | Status | Findings |
|-------|--------|----------|
| Port Scanning | ✅ Complete | 36 open ports |
| WebSocket Discovery | ⏳ In Progress | 0 found yet |
| S3 Enumeration | 🔄 Starting | Pending |

---

**Next Action**: Test qa.growthgrader.hubspot.com:8080 in browser for exposed debug/admin endpoints
