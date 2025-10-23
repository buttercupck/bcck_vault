# Subdomain Reconnaissance Methodology
## Based on Jason Haddix's Bug Hunter's Methodology

**Source**: Jason Haddix (DEFCON, NahamCon, Bug Hunter Methodology)
**Expert**: Jason Haddix (@jhaddix) - CISO, Bug Bounty Legend, Founder of Bug Bounty methodology
**Date Created**: 2025-10-23

**Jason Haddix's Philosophy**: "The best bug hunters find bugs where others don't look. Subdomain enumeration expands your attack surface exponentially."

---

## Table of Contents
1. [Why Subdomain Enumeration Matters](#why-subdomain-enumeration-matters)
2. [The Methodology Overview](#the-methodology-overview)
3. [Passive Enumeration](#passive-enumeration)
4. [Active Enumeration](#active-enumeration)
5. [Permutation and Alteration](#permutation-and-alteration)
6. [Recursive Enumeration](#recursive-enumeration)
7. [Verification and Analysis](#verification-and-analysis)
8. [Content Discovery](#content-discovery)
9. [Port Scanning and Service Discovery](#port-scanning-and-service-discovery)
10. [Prioritization Strategy](#prioritization-strategy)
11. [HubSpot-Specific Application](#hubspot-specific-application)
12. [Tools Arsenal](#tools-arsenal)

---

## Why Subdomain Enumeration Matters

### The Attack Surface Multiplier

**Jason Haddix's Key Insight**: "Most researchers test main domains. Subdomain enumeration can 10x your attack surface."

**Example**:
```
target.com                    → 1 domain
After enumeration:
- api.target.com              → API endpoints
- dev.target.com              → Development environment
- staging.target.com          → Staging (often less secure)
- old.target.com              → Legacy/unmaintained code
- internal.target.com         → Internal tools
- admin.target.com            → Admin panels
- test.target.com             → Testing environments
- qa.target.com               → QA systems
- vpn.target.com              → VPN portals
- mail.target.com             → Email systems
... + 100-1000 more subdomains
```

### Why Subdomains Are Goldmines

**1. Forgotten/Abandoned Subdomains**
- Old applications still running
- Unmaintained code with known vulnerabilities
- No active security monitoring
- Often running outdated frameworks

**2. Development/Staging Environments**
- Less security hardening
- Debug mode often enabled
- Verbose error messages
- Sometimes using production data
- Weak authentication

**3. Different Teams, Different Security Postures**
- Marketing team subdomain vs Security team subdomain
- Third-party integrations
- Acquired companies (different security standards)
- Legacy systems

**4. Hidden Admin Panels**
- Internal tools exposed to internet
- Admin interfaces on non-standard subdomains
- Employee-only applications

**5. Subdomain Takeover Opportunities**
- Dangling DNS records
- Unclaimed cloud resources
- Expired third-party services

---

## The Methodology Overview

### Jason Haddix's 4-Phase Approach

```
Phase 1: PASSIVE Enumeration
↓
Phase 2: ACTIVE Enumeration
↓
Phase 3: PERMUTATION & Recursion
↓
Phase 4: VERIFICATION & Analysis
```

**Time Allocation** (Haddix recommendation):
- Passive: 15-20% of time
- Active: 30-40% of time
- Permutation: 20-30% of time
- Verification: 20-30% of time

**Key Principle**: "Never skip passive enumeration. It's free reconnaissance that won't alert the target."

---

## Passive Enumeration

### What is Passive Enumeration?

**Definition**: Discovering subdomains WITHOUT directly interacting with the target's infrastructure.

**Why Start Here**:
- Won't alert target's security team
- No risk of triggering WAF/IDS
- Discovers historical data
- Free and quiet

### Passive Sources

#### 1. Certificate Transparency Logs

**What**: Public logs of all SSL/TLS certificates issued

**Why it matters**: Companies request certs for subdomains, revealing infrastructure

**Tools**:
```bash
# crt.sh (Web interface or API)
curl -s "https://crt.sh/?q=%25.hubspot.com&output=json" | jq -r '.[].name_value' | sort -u

# subfinder (includes CT logs)
subfinder -d hubspot.com -all -recursive

# certspotter
certspotter hubspot.com
```

**What you get**:
- Current subdomains
- Historical subdomains (even if DNS removed)
- Wildcard certificates (hints at naming patterns)

**Example Output**:
```
api.hubspot.com
app.hubspot.com
*.app.hubspot.com
developers.hubspot.com
old-api-v1.hubspot.com  ← Interesting! Old version
test-internal.hubspot.com  ← Interesting! Test environment
```

#### 2. DNS Aggregators

**Sources**: Services that collect and store DNS data

**Tools**:
```bash
# DNSDumpster (web interface)
# https://dnsdumpster.com/

# SecurityTrails (requires API key)
curl -X GET "https://api.securitytrails.com/v1/domain/hubspot.com/subdomains" \
  -H "APIKEY: YOUR_KEY" | jq -r '.subdomains[]' | sed 's/$/.hubspot.com/'

# VirusTotal (API)
curl -s "https://www.virustotal.com/vtapi/v2/domain/report?apikey=YOUR_KEY&domain=hubspot.com" \
  | jq -r '.subdomains[]'

# Shodan (API)
shodan domain hubspot.com
```

**What you get**:
- Historical DNS records
- Subdomains from passive DNS databases
- IP relationships

#### 3. Search Engine Dorking

**Google Dorks**:
```
site:*.hubspot.com
site:*.hubspot.com -www
site:*.hubspot.com inurl:admin
site:*.hubspot.com inurl:dev
site:*.hubspot.com inurl:test
site:*.hubspot.com inurl:staging
site:*.hubspot.com inurl:api
site:*.hubspot.com intitle:"index of"
site:*.hubspot.com ext:php
site:*.hubspot.com ext:asp
```

**Bing/DuckDuckGo**:
```
domain:hubspot.com
ip:1.2.3.4  (if you know their IP range)
```

#### 4. Web Archives

**Wayback Machine**:
```bash
# Get historical URLs
curl -s "http://web.archive.org/cdx/search/cdx?url=*.hubspot.com/*&output=json&collapse=urlkey" \
  | jq -r '.[] | select(. != null) | .[2]' | unfurl domains | sort -u

# Or use waybackurls tool
waybackurls hubspot.com | unfurl domains | sort -u
```

**What you get**:
- Old subdomains no longer in DNS
- Historical structure
- Removed/forgotten domains

#### 5. GitHub/GitLab Code Search

**Search for**:
```
"hubspot.com" site:github.com
"*.hubspot.com" site:github.com
"api.hubspot.com" site:github.com
```

**What to look for**:
- API endpoints in code
- Configuration files
- Environment variables
- Documentation

#### 6. Social Media & Job Postings

**Sources**:
- LinkedIn (look for engineering posts mentioning infrastructure)
- Twitter (developers talking about tools)
- Job postings (often mention tech stack)
- Conference presentations
- Blog posts by employees

**Example**:
```
"hubspot" "subdomain" site:linkedin.com
"hubspot" "internal tools" site:twitter.com
```

### Passive Enumeration Automation

**Jason Haddix's Recommended Tools**:

```bash
# Amass (Intel gathering)
amass enum -d hubspot.com -passive -o amass_passive.txt

# Subfinder (Multiple sources)
subfinder -d hubspot.com -all -o subfinder.txt

# Assetfinder (Quick passive scan)
assetfinder --subs-only hubspot.com > assetfinder.txt

# Findomain (Fast passive enum)
findomain -t hubspot.com -o

# Combine all results
cat amass_passive.txt subfinder.txt assetfinder.txt | sort -u > passive_all.txt
```

---

## Active Enumeration

### What is Active Enumeration?

**Definition**: Directly querying DNS servers to discover subdomains

**When to use**: After exhausting passive methods

**Trade-off**: More results, but target might notice

### DNS Brute Forcing

**Concept**: Try common subdomain names against DNS

**Tools & Techniques**:

#### 1. Classic DNS Brute Force

```bash
# Using puredns (Jason Haddix recommends)
puredns bruteforce wordlist.txt hubspot.com -r resolvers.txt

# Using massdns
massdns -r resolvers.txt -t A -o S wordlist.txt -w results.txt

# Using dnsx
cat wordlist.txt | dnsx -d hubspot.com -resp -o dnsx_results.txt
```

**Wordlists to Use**:
```bash
# Small (1K-10K): Quick scan
/path/to/subdomains-top1million-5000.txt

# Medium (10K-100K): Standard scan
/path/to/subdomains-top1million-20000.txt

# Large (100K-1M): Comprehensive scan
/path/to/all.txt

# Custom wordlist based on target
# (Generate from passive results + common patterns)
```

#### 2. Smart Brute Forcing

**Generate custom wordlist from passive results**:

```bash
# Extract keywords from discovered subdomains
cat passive_all.txt | sed 's/\.hubspot\.com//' | tr '.-' '\n' | sort -u > keywords.txt

# Common patterns
echo "api
dev
test
staging
prod
qa
uat
admin
internal
vpn
mail
smtp
pop
imap
ftp
ssh
www1
www2
mobile
app
beta
alpha
demo
sandbox" >> keywords.txt

# Generate permutations
while read keyword; do
  echo "$keyword"
  echo "$keyword-api"
  echo "$keyword-dev"
  echo "$keyword-staging"
  echo "$keyword-prod"
  echo "$keyword-test"
  echo "$keyword-qa"
  echo "dev-$keyword"
  echo "test-$keyword"
  echo "staging-$keyword"
  echo "prod-$keyword"
  echo "qa-$keyword"
done < keywords.txt | sort -u > custom_wordlist.txt
```

#### 3. Zone Transfer Attempts

**What**: Requesting full DNS zone file (usually fails, but worth trying)

```bash
# Check if zone transfer is allowed
dig axfr @ns1.hubspot.com hubspot.com
dig axfr @ns2.hubspot.com hubspot.com

# Try all nameservers
host -t ns hubspot.com | cut -d" " -f4 | while read ns; do
  dig axfr @$ns hubspot.com
done
```

**Success rate**: <1%, but when it works, you get EVERYTHING

---

## Permutation and Alteration

### What is Permutation?

**Definition**: Generating variations of discovered subdomains to find related ones

**Jason Haddix**: "If you find 'api-v1.target.com', immediately check 'api-v2', 'api-v3', 'api-staging', etc."

### Permutation Techniques

#### 1. Numerical Permutations

```bash
# If you found: api-v1.hubspot.com

# Generate:
api-v2.hubspot.com
api-v3.hubspot.com
api-v4.hubspot.com
api-v5.hubspot.com
```

#### 2. Environment Permutations

```bash
# If you found: admin.hubspot.com

# Generate:
admin-dev.hubspot.com
admin-staging.hubspot.com
admin-test.hubspot.com
admin-qa.hubspot.com
admin-prod.hubspot.com
dev-admin.hubspot.com
staging-admin.hubspot.com
test-admin.hubspot.com
```

#### 3. Geographic Permutations

```bash
# If you found: api.hubspot.com

# Generate:
api-us.hubspot.com
api-eu.hubspot.com
api-asia.hubspot.com
us-api.hubspot.com
eu-api.hubspot.com
api-east.hubspot.com
api-west.hubspot.com
```

#### 4. Service Permutations

```bash
# If you found: app.hubspot.com

# Generate:
app-api.hubspot.com
app-backend.hubspot.com
app-frontend.hubspot.com
app-db.hubspot.com
app-cache.hubspot.com
```

### Automated Permutation Tools

```bash
# Altdns (Jason Haddix favorite)
altdns -i discovered.txt -o permutations.txt -w permutation_words.txt
cat permutations.txt | dnsx -resp -o resolved_permutations.txt

# Gotator (Go-based, fast)
gotator -sub discovered.txt -perm permutation_words.txt -depth 3 -numbers 10 \
  | dnsx -d hubspot.com -resp -o gotator_results.txt

# dnsgen (Smart permutations)
cat discovered.txt | dnsgen - | dnsx -resp -o dnsgen_results.txt
```

**Permutation Wordlist**:
```
dev
test
staging
prod
qa
uat
admin
api
v1
v2
v3
backend
frontend
internal
external
public
private
north
south
east
west
us
eu
asia
```

---

## Recursive Enumeration

### What is Recursive Enumeration?

**Definition**: Finding subdomains of subdomains (multi-level DNS)

**Example**:
```
hubspot.com
├── app.hubspot.com
│   ├── api.app.hubspot.com         ← Recursive discovery
│   └── internal.app.hubspot.com    ← Recursive discovery
└── dev.hubspot.com
    ├── test.dev.hubspot.com        ← Recursive discovery
    └── staging.dev.hubspot.com     ← Recursive discovery
```

### Recursive Techniques

#### 1. Certificate Transparency Recursion

```bash
# Check each discovered subdomain for wildcard certs
while read subdomain; do
  curl -s "https://crt.sh/?q=%25.$subdomain&output=json" | \
    jq -r '.[].name_value' | sort -u
done < discovered.txt >> recursive_results.txt
```

#### 2. DNS Brute Force Recursion

```bash
# For each discovered subdomain, brute force again
while read subdomain; do
  puredns bruteforce wordlist.txt $subdomain -r resolvers.txt >> recursive_bruteforce.txt
done < discovered.txt
```

#### 3. Amass Recursive Mode

```bash
# Amass automatically does recursive enumeration
amass enum -d hubspot.com -recursive -o recursive_amass.txt
```

**When to Stop Recursion**:
- After 2-3 levels deep
- When you stop finding new subdomains
- When time/scope constraints hit

---

## Verification and Analysis

### Verifying Discovered Subdomains

**Problem**: Not all discovered subdomains are live

**Solution**: Verify which ones actually resolve and are reachable

#### 1. DNS Resolution Verification

```bash
# Check if subdomains resolve
cat all_discovered.txt | dnsx -resp -o live_subdomains.txt

# Get IP addresses
cat all_discovered.txt | dnsx -resp -a -o subdomains_with_ips.txt

# Check for CNAMEs (important for subdomain takeover)
cat all_discovered.txt | dnsx -resp -cname -o subdomains_cnames.txt
```

#### 2. HTTP/HTTPS Probing

```bash
# httpx - Check which subdomains have web services
cat live_subdomains.txt | httpx -silent -o web_services.txt

# Get status codes
cat live_subdomains.txt | httpx -status-code -o status_codes.txt

# Get titles (helps identify what each subdomain is)
cat live_subdomains.txt | httpx -title -o titles.txt

# Get full details
cat live_subdomains.txt | httpx -tech-detect -status-code -title -content-length -o full_probe.txt
```

#### 3. Screenshots (Visual Analysis)

```bash
# Aquatone (Jason Haddix classic tool)
cat live_subdomains.txt | aquatone -out aquatone_results/

# EyeWitness
eyewitness --web -f live_subdomains.txt -d eyewitness_results/

# Gowitness
gowitness file -f live_subdomains.txt -P gowitness_results/
```

**Why screenshots**:
- Quickly identify admin panels visually
- Spot login pages
- Find old/forgotten interfaces
- Identify default pages (nginx, Apache defaults = often vulnerable)

---

## Content Discovery

### After Finding Subdomains, Find Content

**Jason Haddix**: "A subdomain is just the beginning. Now you need to find the endpoints, directories, and files."

### Directory Brute Forcing

```bash
# ffuf (Fast web fuzzer)
ffuf -u https://SUBDOMAIN/FUZZ -w /path/to/wordlist.txt -mc 200,301,302,403

# dirsearch
dirsearch -u https://SUBDOMAIN -e php,asp,aspx,jsp -w /path/to/wordlist.txt

# feroxbuster (Recursive directory scanner)
feroxbuster -u https://SUBDOMAIN -w /path/to/wordlist.txt -x php,html,js
```

### JavaScript Analysis

```bash
# Download all JS files
cat web_services.txt | subjs | httpx -mc 200 -o javascript_files.txt

# Extract endpoints from JS
cat javascript_files.txt | while read url; do
  curl -s $url | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | sort -u
done > endpoints_from_js.txt

# Extract API endpoints
cat javascript_files.txt | while read url; do
  curl -s $url | grep -Eo "/(api|v1|v2|v3|graphql|rest)/[a-zA-Z0-9./?=_-]*" | sort -u
done > api_endpoints.txt
```

### Parameter Discovery

```bash
# Arjun (Parameter discovery)
arjun -u https://subdomain.hubspot.com/endpoint

# x8 (Hidden parameter discovery)
x8 -u https://subdomain.hubspot.com/endpoint -w params.txt
```

---

## Port Scanning and Service Discovery

### Beyond HTTP/HTTPS

**Jason Haddix**: "Don't just test web services. Open ports reveal additional attack surface."

### Port Scanning

```bash
# Nmap (Top ports)
nmap -iL live_subdomains.txt -p- --open -oA nmap_results

# Masscan (Faster for large ranges)
masscan -iL ips.txt -p0-65535 --rate 10000 -oL masscan_results.txt

# Naabu (Fast port scanner)
cat live_subdomains.txt | naabu -p - -o open_ports.txt
```

### Service Identification

```bash
# What's running on open ports?
nmap -sV -p $(cat open_ports.txt | cut -d: -f2 | tr '\n' ',') -iL live_subdomains.txt

# Check for common services:
# - 21 (FTP)
# - 22 (SSH)
# - 25 (SMTP)
# - 443 (HTTPS)
# - 3306 (MySQL)
# - 5432 (PostgreSQL)
# - 6379 (Redis)
# - 8080 (HTTP Alt)
# - 9200 (Elasticsearch)
```

### Non-HTTP Services to Test

```bash
# FTP anonymous login
nmap -p 21 --script ftp-anon -iL ips.txt

# SSH version detection
nmap -p 22 -sV -iL ips.txt

# MySQL anonymous access
nmap -p 3306 --script mysql-enum -iL ips.txt

# Redis unauth access
nmap -p 6379 --script redis-info -iL ips.txt

# Elasticsearch exposure
curl -s http://SUBDOMAIN:9200/_cat/indices
```

---

## Prioritization Strategy

### Not All Subdomains Are Equal

**Jason Haddix's Prioritization**:

#### Tier 1 (Test FIRST) - Highest Value:
```
1. admin.* / administrator.* / manage.*
2. dev.* / development.* / staging.*
3. test.* / qa.* / uat.*
4. api.* / api-v1.* / api-internal.*
5. internal.* / corp.* / vpn.*
6. old.* / legacy.* / v1.* / deprecated.*
7. beta.* / alpha.* / sandbox.*
```

**Why**: Weaker security, forgotten, admin access

#### Tier 2 (Test SECOND) - Medium Value:
```
1. mail.* / smtp.* / webmail.*
2. ftp.* / upload.* / files.*
3. dashboard.* / panel.* / console.*
4. jenkins.* / gitlab.* / jira.*
5. monitoring.* / grafana.* / kibana.*
```

**Why**: Often exposed services, sometimes weak auth

#### Tier 3 (Test LAST) - Lower Value:
```
1. www.* / www1.* / www2.*
2. cdn.* / static.* / assets.*
3. blog.* / news.* / help.*
```

**Why**: Heavily tested, hardened, public-facing

### Red Flags to Look For

**Jason Haddix's "Instant Win" Indicators**:

```
1. Subdomain takeover (CNAME points to unclaimed service)
2. Default credentials (admin:admin, test:test)
3. Directory listing enabled
4. .git directory exposed
5. Verbose error messages (stack traces)
6. phpinfo() pages
7. Admin panels without auth
8. Outdated software (visible in headers)
9. Test/debug mode enabled
10. Elasticsearch/MongoDB exposed
```

---

## HubSpot-Specific Application

### Applying This to HubSpot

#### Phase 1: Passive Enumeration (TODAY)

```bash
# Certificate Transparency
curl -s "https://crt.sh/?q=%25.hubspot.com&output=json" | \
  jq -r '.[].name_value' | sort -u > hubspot_ct.txt

# Subfinder (all sources)
subfinder -d hubspot.com -all -recursive -o hubspot_subfinder.txt

# Amass passive
amass enum -d hubspot.com -passive -o hubspot_amass_passive.txt

# Combine
cat hubspot_ct.txt hubspot_subfinder.txt hubspot_amass_passive.txt | \
  sort -u > hubspot_passive_all.txt

# Count results
wc -l hubspot_passive_all.txt
```

**Expected**: 100-500+ subdomains

#### Phase 2: Verification (TODAY)

```bash
# Resolve live subdomains
cat hubspot_passive_all.txt | dnsx -resp -o hubspot_live.txt

# Probe web services
cat hubspot_live.txt | httpx -tech-detect -status-code -title -o hubspot_web_services.txt

# Take screenshots
cat hubspot_live.txt | aquatone -out hubspot_screenshots/
```

#### Phase 3: Priority Testing (THIS WEEK)

```bash
# Extract high-priority subdomains
grep -E "(admin|dev|test|staging|qa|internal|api|old|beta)" hubspot_live.txt > hubspot_priority.txt

# Test each one manually
# Focus on:
# 1. Login pages (default creds)
# 2. Error pages (XSS)
# 3. API endpoints (injection)
# 4. Upload functionality
# 5. Search features
```

#### Phase 4: Deep Content Discovery (THIS WEEK)

```bash
# For each priority subdomain
while read subdomain; do
  # Directory brute force
  ffuf -u https://$subdomain/FUZZ -w wordlist.txt -mc 200,301,302,403 -o ${subdomain}_dirs.txt

  # Find JS files
  subjs -i $subdomain | httpx -mc 200 > ${subdomain}_js.txt

  # Extract endpoints from JS
  cat ${subdomain}_js.txt | while read js_url; do
    curl -s $js_url | grep -Eo "/(api|graphql|v1|v2)/[a-zA-Z0-9./?=_-]*"
  done > ${subdomain}_endpoints.txt
done < hubspot_priority.txt
```

### HubSpot Subdomain Patterns to Look For

**Based on Source Code Analysis**:
```
From your source intel, look for:
- exceptions.hubspot.com (error reporting)
- *.qa.hubspot.com (QA environments)
- *.app.hubspot.com (app subdomains)
- *.api.hubspot.com (API subdomains)

Common SaaS patterns:
- app-na1.hubspot.com
- app-na2.hubspot.com  ← (you already know this one)
- app-eu1.hubspot.com
- app-staging.hubspot.com
- app-dev.hubspot.com
```

### Testing Checklist per Subdomain

```
For each discovered subdomain:
[ ] Screenshot taken
[ ] Technology detected (httpx)
[ ] Status code noted
[ ] Tested for login page
[ ] Tested for XSS on error pages
[ ] Tested for directory listing
[ ] Checked for .git exposure
[ ] Searched for API endpoints
[ ] Checked for subdomain takeover (CNAME)
[ ] Tested default credentials
[ ] Checked robots.txt
[ ] Checked security.txt
[ ] Port scanned (beyond 80/443)
```

---

## Tools Arsenal

### Jason Haddix's Essential Toolkit

#### Passive Enumeration
```
- Amass: https://github.com/OWASP/Amass
- Subfinder: https://github.com/projectdiscovery/subfinder
- Assetfinder: https://github.com/tomnomnom/assetfinder
- Findomain: https://github.com/Findomain/Findomain
```

#### Active Enumeration
```
- Puredns: https://github.com/d3mondev/puredns
- Massdns: https://github.com/blechschmidt/massdns
- dnsx: https://github.com/projectdiscovery/dnsx
```

#### Permutation
```
- Altdns: https://github.com/infosec-au/altdns
- dnsgen: https://github.com/ProjectAnte/dnsgen
- Gotator: https://github.com/Josue87/gotator
```

#### Verification
```
- httpx: https://github.com/projectdiscovery/httpx
- Aquatone: https://github.com/michenriksen/aquatone
- EyeWitness: https://github.com/FortyNorthSecurity/EyeWitness
```

#### Content Discovery
```
- ffuf: https://github.com/ffuf/ffuf
- feroxbuster: https://github.com/epi052/feroxbuster
- dirsearch: https://github.com/maurosoria/dirsearch
```

#### JavaScript Analysis
```
- subjs: https://github.com/lc/subjs
- LinkFinder: https://github.com/GerbenJavado/LinkFinder
```

### Quick Install (macOS)

```bash
# Install Go (prerequisite for many tools)
brew install go

# Install tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/d3mondev/puredns/v2@latest
go install github.com/ffuf/ffuf@latest

# Install with brew
brew install amass

# Python tools
pip3 install altdns

# Add to PATH
export PATH=$PATH:~/go/bin
```

---

## Practical Exercise: HubSpot Enumeration

### Step-by-Step Walkthrough

**Time**: 2-3 hours
**Goal**: Comprehensive subdomain enumeration of HubSpot

#### Step 1: Passive Collection (30 min)

```bash
# Create working directory
mkdir -p ~/hubspot_recon/passive
cd ~/hubspot_recon/passive

# Run all passive tools in parallel
subfinder -d hubspot.com -all -o subfinder.txt &
amass enum -d hubspot.com -passive -o amass.txt &
assetfinder --subs-only hubspot.com > assetfinder.txt &

# Certificate Transparency
curl -s "https://crt.sh/?q=%25.hubspot.com&output=json" | \
  jq -r '.[].name_value' | sort -u > crt.txt &

# Wait for all to complete
wait

# Combine and deduplicate
cat *.txt | sort -u > all_passive.txt

# Count
echo "Total passive subdomains found: $(wc -l < all_passive.txt)"
```

#### Step 2: Verification (15 min)

```bash
mkdir -p ~/hubspot_recon/verification
cd ~/hubspot_recon/verification

# DNS resolution
cat ~/hubspot_recon/passive/all_passive.txt | \
  dnsx -resp -o live.txt

# HTTP probing
cat live.txt | httpx -silent -tech-detect -status-code -title \
  -content-length -o web_services.txt

# Count
echo "Live subdomains: $(wc -l < live.txt)"
echo "Web services: $(wc -l < web_services.txt)"
```

#### Step 3: Prioritization (10 min)

```bash
# Extract high-value targets
grep -iE "(admin|dev|test|staging|qa|api|internal|old|beta)" live.txt > priority.txt

# Show priority targets
echo "Priority targets to test first:"
cat priority.txt
```

#### Step 4: Screenshots (30 min)

```bash
mkdir -p ~/hubspot_recon/screenshots
cd ~/hubspot_recon/screenshots

# Take screenshots
cat ~/hubspot_recon/verification/web_services.txt | aquatone -out ./
```

#### Step 5: Manual Analysis (60+ min)

```
Open ~/hubspot_recon/screenshots/aquatone_report.html

For each interesting subdomain:
1. Visit in browser
2. Check for login pages
3. Test error pages for XSS
4. Look for directory listing
5. Check source code for API endpoints
6. Test any forms
7. Document findings
```

---

## Common Mistakes to Avoid

**Jason Haddix's Warnings**:

1. **Don't skip passive enumeration**
   - "I've found critical bugs on subdomains that only appeared in CT logs from 2 years ago"

2. **Don't stop at first tool**
   - Each tool finds different subdomains
   - Amass finds some, Subfinder finds others
   - Combine results from ALL tools

3. **Don't forget recursion**
   - api.target.com might have staging.api.target.com
   - Always go 2-3 levels deep

4. **Don't ignore "boring" subdomains**
   - www2.target.com might be running old code
   - blog.target.com might have WordPress vulns

5. **Don't test without screenshots**
   - Visual analysis is FAST
   - Spot patterns quickly
   - Identify login pages at a glance

6. **Don't forget non-HTTP services**
   - Port scan beyond 80/443
   - FTP, SSH, databases might be exposed

---

## Success Metrics

**How to Know You're Done**:

```
✅ Ran 3+ passive enumeration tools
✅ Verified all discovered subdomains
✅ Took screenshots of all web services
✅ Prioritized by value (admin/dev/test first)
✅ Manually tested top 20 priority targets
✅ Documented findings
✅ Found at least ONE potential vulnerability
```

**Realistic Expectations**:

```
Small target (startup): 10-50 subdomains
Medium target (SMB): 50-200 subdomains
Large target (enterprise): 200-1000+ subdomains
HubSpot (enterprise SaaS): Expect 500-2000 subdomains
```

---

## Key Takeaways

**Jason Haddix's Core Principles**:

1. **Subdomain enumeration is not optional** - It's the foundation of recon
2. **Automation + Manual = Success** - Tools find subdomains, humans find bugs
3. **Passive first, active second** - Don't alert target before you have intel
4. **Every tool finds different results** - Use multiple tools, combine output
5. **Old/forgotten = vulnerable** - dev/test/staging subdomains are goldmines
6. **Visual analysis is underrated** - Screenshots save time
7. **Recursion reveals hidden gems** - Don't stop at first level
8. **Prioritize testing** - Admin panels before marketing pages

**Your Advantage**:

You have source code showing:
- Internal subdomain patterns
- Error reporting domains (exceptions.hubspot.com)
- QA environment references
- API structure

Use this intel to GUIDE your subdomain enumeration.

---

## Next Steps

**This Week**:
1. Run complete passive enumeration (2-3 hours)
2. Verify and screenshot all results (1-2 hours)
3. Test top 20 priority subdomains (6-8 hours)
4. Document findings

**Success Criteria**:
- [ ] 100+ subdomains discovered
- [ ] All verified and categorized
- [ ] Priority targets identified
- [ ] At least 5 subdomains manually tested
- [ ] Findings documented

**Ready to begin. Let's find those subdomains and turn them into vulnerabilities.**
