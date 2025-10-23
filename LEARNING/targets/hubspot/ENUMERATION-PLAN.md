# HubSpot Subdomain Enumeration - Execution Plan
**Date**: 2025-10-23
**Target**: hubspot.com
**Goal**: Find XSS on subdomain for cookie counterfeiting attack

---

## Current Tool Status

### ✅ Already Installed
- subfinder (Go) - Multi-source subdomain enumeration
- amass (Go) - OWASP subdomain enumeration suite
- httpx (Go) - Fast HTTP toolkit
- nuclei (Go) - Vulnerability scanner
- anew (Go) - Append new lines to file
- jq - JSON processor
- curl - HTTP client
- python3 - For additional scripts
- go - For installing more tools

### ❌ Need to Install
- dnsx - DNS toolkit (verification)
- assetfinder - Additional passive enumeration
- aquatone - Screenshot tool
- ffuf - Web fuzzer (for later content discovery)

---

## Installation Plan (15 minutes)

### Step 1: Install Missing Go Tools
```bash
# Install dnsx (DNS verification)
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# Install assetfinder (additional passive)
go install github.com/tomnomnom/assetfinder@latest

# Install ffuf (web fuzzer)
go install github.com/ffuf/ffuf/v2@latest

# Install aquatone (screenshots)
go install github.com/michenriksen/aquatone@latest
```

### Step 2: Verify Installation
```bash
# Check all tools work
subfinder -version
amass -version
httpx -version
dnsx -version
assetfinder --help
ffuf -V
```

### Step 3: Create Working Directory
```bash
# Create recon workspace
mkdir -p ~/hubspot_recon/{passive,active,verified,screenshots,priority}
cd ~/hubspot_recon
```

---

## Enumeration Execution Plan (2-3 hours)

### Phase 1: Passive Enumeration (30-45 min)

**Goal**: Collect subdomains WITHOUT alerting HubSpot

#### 1.1: Subfinder (Multi-source passive)
```bash
cd ~/hubspot_recon/passive

# Run subfinder with all sources
subfinder -d hubspot.com -all -recursive -o subfinder.txt

# Expected: 200-500 subdomains
# Time: 5-10 minutes
```

#### 1.2: Amass Passive (OWASP enumeration)
```bash
# Run amass passive mode
amass enum -d hubspot.com -passive -o amass_passive.txt

# Expected: 150-400 subdomains (some overlap with subfinder)
# Time: 10-15 minutes
```

#### 1.3: Assetfinder (Additional passive)
```bash
# Quick passive scan
assetfinder --subs-only hubspot.com > assetfinder.txt

# Expected: 100-300 subdomains
# Time: 2-5 minutes
```

#### 1.4: Certificate Transparency (Direct API)
```bash
# Query crt.sh for certificates
curl -s "https://crt.sh/?q=%25.hubspot.com&output=json" | \
  jq -r '.[].name_value' | \
  sed 's/\*\.//g' | \
  sort -u > crt_sh.txt

# Expected: 100-300 subdomains
# Time: 1-2 minutes
```

#### 1.5: Combine All Passive Results
```bash
# Merge and deduplicate
cat subfinder.txt amass_passive.txt assetfinder.txt crt_sh.txt | \
  sort -u > all_passive.txt

# Count total
wc -l all_passive.txt

# Expected: 500-1000 unique subdomains
```

**Checkpoint 1**: Review `all_passive.txt` - should have hundreds of subdomains

---

### Phase 2: Verification (15-20 min)

**Goal**: Find which subdomains are actually live

#### 2.1: DNS Resolution
```bash
cd ~/hubspot_recon/verified

# Verify which subdomains resolve
cat ~/hubspot_recon/passive/all_passive.txt | \
  dnsx -resp -o live_subdomains.txt

# Get IP addresses too
cat ~/hubspot_recon/passive/all_passive.txt | \
  dnsx -resp -a -o subdomains_with_ips.txt

# Check for CNAMEs (subdomain takeover opportunities)
cat ~/hubspot_recon/passive/all_passive.txt | \
  dnsx -resp -cname -o subdomains_cnames.txt

# Expected: 200-500 live subdomains
# Time: 5-10 minutes
```

#### 2.2: HTTP/HTTPS Probing
```bash
# Probe for web services
cat live_subdomains.txt | \
  httpx -silent -tech-detect -status-code -title -content-length \
  -o web_services.txt

# Count web services
wc -l web_services.txt

# Expected: 100-300 web services
# Time: 5-10 minutes
```

**Checkpoint 2**: Review `web_services.txt` - should show status codes, titles, tech stack

---

### Phase 3: Prioritization (10 min)

**Goal**: Identify high-value targets to test first

#### 3.1: Extract High-Priority Subdomains
```bash
cd ~/hubspot_recon/priority

# Find admin/dev/test/staging subdomains
grep -iE "(admin|dev|test|staging|qa|internal|api|old|beta|alpha|sandbox|vpn|corp)" \
  ~/hubspot_recon/verified/live_subdomains.txt > tier1_priority.txt

# Find medium priority
grep -iE "(mail|smtp|ftp|upload|dashboard|panel|jenkins|gitlab|jira|grafana)" \
  ~/hubspot_recon/verified/live_subdomains.txt > tier2_priority.txt

# Combine priority targets
cat tier1_priority.txt tier2_priority.txt | sort -u > all_priority.txt

# Count priority targets
echo "Tier 1 (High Priority): $(wc -l < tier1_priority.txt)"
echo "Tier 2 (Medium Priority): $(wc -l < tier2_priority.txt)"
echo "Total Priority Targets: $(wc -l < all_priority.txt)"

# Expected: 20-50 priority targets
```

#### 3.2: Extract Known Interesting Subdomains (From Source Code)
```bash
# Based on your source code analysis, look for:
grep -E "(exceptions|qa\.)" ~/hubspot_recon/verified/live_subdomains.txt > known_interesting.txt

# Show them
echo "Known interesting subdomains from source code:"
cat known_interesting.txt
```

**Checkpoint 3**: Review `tier1_priority.txt` - these are your goldmine targets

---

### Phase 4: Screenshots (30 min - OPTIONAL for now)

**Goal**: Visual analysis of subdomains

```bash
cd ~/hubspot_recon/screenshots

# Take screenshots of all web services (may take 20-30 min)
cat ~/hubspot_recon/verified/web_services.txt | \
  aquatone -out ./

# Once complete, open report
open aquatone_report.html
```

**Note**: This is optional for initial enumeration. We can skip this and go straight to manual testing.

---

## Manual Testing Phase (Start After Enumeration)

### Priority Testing Order

#### Round 1: Tier 1 Priority Targets (Focus Here First)
```bash
# Test these manually for XSS:
cat ~/hubspot_recon/priority/tier1_priority.txt
```

**For each subdomain, test**:
1. Visit in browser
2. Look for error pages (404, 500)
3. Test XSS in URL parameters: `?q=<script>alert(1)</script>`
4. Test XSS in search: `"><script>alert(1)</script>`
5. Check for login page (default creds)
6. Check for directory listing
7. Check robots.txt

#### Round 2: Known Interesting (From Your Research)
```bash
# Test these specifically:
- exceptions.hubspot.com (error reporting)
- Any *.qa.hubspot.com subdomains
- Any *.app-*.hubspot.com pattern
```

#### Round 3: Tier 2 If No Success Yet
```bash
cat ~/hubspot_recon/priority/tier2_priority.txt
```

---

## Quick Reference: XSS Test Payloads

**Test these on each subdomain**:

```html
# Basic tests
<script>alert(1)</script>
"><script>alert(1)</script>
'><script>alert(1)</script>

# Event handlers
<img src=x onerror=alert(1)>
<svg/onload=alert(1)>

# URL reflection
?redirect=javascript:alert(1)
?url=javascript:alert(1)

# Parameter reflection
?q="><svg/onload=alert(1)>
?search=<img src=x onerror=alert(1)>
```

---

## Success Criteria

### Enumeration Complete When:
- [x] All passive tools run
- [x] Results combined and deduplicated
- [x] Live subdomains verified
- [x] Web services probed
- [x] Priority targets identified
- [x] Top 20 targets documented

### Testing Complete When:
- [ ] Top 20 tier 1 targets tested
- [ ] Known interesting subdomains tested
- [ ] At least ONE XSS found (even low severity)
- [ ] OR all tier 1 + tier 2 tested (40-50 subdomains)

---

## Expected Timeline

**Today (Installation + Enumeration)**:
- 00:00-00:15 - Install missing tools
- 00:15-01:00 - Run passive enumeration (parallel)
- 01:00-01:20 - Verify live subdomains
- 01:20-01:30 - Prioritize targets
- 01:30-01:45 - Review results, create test list

**Total**: ~1.5-2 hours for complete enumeration

**Tomorrow (Manual Testing)**:
- Test tier 1 priority targets (20-30 subdomains)
- 15-20 minutes per subdomain
- 6-8 hours total testing time

---

## Output Files Reference

```
~/hubspot_recon/
├── passive/
│   ├── subfinder.txt           # Subfinder results
│   ├── amass_passive.txt       # Amass passive results
│   ├── assetfinder.txt         # Assetfinder results
│   ├── crt_sh.txt              # Certificate transparency
│   └── all_passive.txt         # Combined results
├── verified/
│   ├── live_subdomains.txt     # DNS-verified subdomains
│   ├── subdomains_with_ips.txt # With IP addresses
│   ├── subdomains_cnames.txt   # With CNAME records
│   └── web_services.txt        # HTTP-probed services
├── priority/
│   ├── tier1_priority.txt      # HIGH priority targets
│   ├── tier2_priority.txt      # MEDIUM priority targets
│   ├── all_priority.txt        # All priority targets
│   └── known_interesting.txt   # From source code
└── screenshots/
    └── aquatone_report.html    # Visual analysis (optional)
```

---

## Troubleshooting

### If tools are slow:
```bash
# Use fewer DNS resolvers
echo "8.8.8.8
1.1.1.1" > resolvers.txt

# Pass to tools
dnsx -r resolvers.txt
```

### If getting rate limited:
```bash
# Add delays
subfinder -d hubspot.com -all -recursive -t 10 -o subfinder.txt
```

### If missing dependencies:
```bash
# Ensure Go bin in PATH
export PATH=$PATH:~/go/bin
echo 'export PATH=$PATH:~/go/bin' >> ~/.zshrc
```

---

## Next Steps After Enumeration

1. **If XSS Found**:
   - Document it
   - Test cookie counterfeiting
   - Build attack chain
   - Submit bug report

2. **If No XSS Found**:
   - Run content discovery on subdomains (ffuf)
   - Test GraphQL endpoints for injection
   - Check for subdomain takeover (CNAME analysis)
   - Consider active brute forcing

3. **If Still Nothing**:
   - Reassess target difficulty
   - Consider pivoting to easier target
   - Or go deeper with advanced techniques

---

**Ready to execute. Let's start with tool installation.**
