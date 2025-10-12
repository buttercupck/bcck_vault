# UEC Reconnaissance Methodology
**Unified Entity Context (UEC) - Building Complete Target Models**

---

## Core Principle

**Most hard decisions become simple with enough context.**

Traditional bug bounty approach:
```
Find vulnerability → Report → Hope for impact
```

UEC approach:
```
Build target model → Understand relationships → Find vulnerability with context → Report with business impact → Higher severity/payout
```

---

## Reconnaissance Phases

### Phase 1: Domain & Subdomain Discovery
**Goal:** Map the entire attack surface - find all domains, subdomains, and IP ranges

### Phase 2: Technology Stack Identification
**Goal:** Understand what technologies power the target (frameworks, languages, servers, CDNs)

### Phase 3: DevOps Infrastructure Discovery
**Goal:** Find exposed DevOps tools (CI/CD, repos, monitoring, wikis) - HIGH IMPACT targets

### Phase 4: Relationship Mapping
**Goal:** Connect the dots - how do systems interact? What data flows where?

### Phase 5: Vulnerability Discovery with Context
**Goal:** Find bugs that matter based on your complete understanding

---

## Tool-by-Tool Workflow

Each tool below is designed to run **independently first**, then chained together for automation.

---

## PHASE 1: Domain & Subdomain Discovery

### Tool 1: `subfinder`
**Purpose:** Passive subdomain enumeration using multiple data sources

**Installation:**
```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

**Basic Usage:**
```bash
subfinder -d target.com -o subdomains.txt
```

**What it does:**
- Queries 40+ sources (Certificate Transparency logs, DNS databases, search engines)
- Returns list of discovered subdomains
- No active scanning (safe, won't alert target)

**Input:** Domain name (`target.com`)
**Output:** Text file with subdomains (one per line)

**Example Output:**
```
api.target.com
dev.target.com
staging.target.com
jenkins.target.com
confluence.target.com
```

**Why this matters:** Subdomains often reveal:
- Development/staging environments (less secure)
- Internal tools (admin.target.com, vpn.target.com)
- DevOps infrastructure (jenkins.target.com, gitlab.target.com)

---

### Tool 2: `amass`
**Purpose:** Advanced subdomain enumeration with DNS intelligence

**Installation:**
```bash
go install -v github.com/owasp-amass/amass/v4/...@master
```

**Basic Usage:**
```bash
amass enum -passive -d target.com -o amass-subdomains.txt
```

**What it does:**
- More thorough than subfinder (uses DNS brute-forcing, scraping, APIs)
- Finds subdomains that subfinder might miss
- Can discover IP ranges and ASN information

**Input:** Domain name
**Output:** Text file with subdomains + optional IP addresses

**Combine with subfinder:**
```bash
# Merge both tools and deduplicate
cat subdomains.txt amass-subdomains.txt | sort -u > all-subdomains.txt
```

**When to use:** Use BOTH subfinder and amass, then merge results for completeness.

---

### Tool 3: `anew`
**Purpose:** Append new lines to files (deduplication)

**Installation:**
```bash
go install -v github.com/tomnomnom/anew@latest
```

**Basic Usage:**
```bash
cat new-subdomains.txt | anew all-subdomains.txt
```

**What it does:**
- Only adds lines that don't already exist in the file
- Perfect for continuous recon (run tools daily, only save new findings)

**Use case in workflow:**
```bash
# Day 1
subfinder -d target.com | anew subdomains.txt

# Day 2 (only adds NEW subdomains discovered)
subfinder -d target.com | anew subdomains.txt
```

---

## PHASE 2: Technology Stack Identification

### Tool 4: `httpx`
**Purpose:** Validate live hosts + detect web technologies

**Installation:**
```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

**Basic Usage:**
```bash
cat all-subdomains.txt | httpx -o live-hosts.txt
```

**Advanced usage (tech detection):**
```bash
cat all-subdomains.txt | httpx -tech-detect -status-code -title -o live-hosts-detail.txt
```

**What it does:**
- Tests if subdomain has a live web server (HTTP/HTTPS)
- Detects technologies: WordPress, Django, React, CDN (Cloudflare, Akamai)
- Returns HTTP status codes, page titles, server headers

**Input:** List of subdomains
**Output:** Only live hosts with web servers

**Example Output:**
```
https://api.target.com [200] [nginx] [API Gateway]
https://jenkins.target.com [403] [Jenkins 2.350] [Forbidden]
https://dev.target.com [200] [Apache/2.4.41] [React App]
```

**Why this matters:**
- Filters dead hosts (don't waste time on non-existent targets)
- Identifies tech stack (WordPress = different bugs than React)
- Finds interesting targets (Jenkins, GitLab, admin panels)

---

### Tool 5: `whatweb`
**Purpose:** Deep technology fingerprinting

**Installation:**
```bash
# macOS
brew install whatweb

# Linux
sudo apt install whatweb
```

**Basic Usage:**
```bash
whatweb https://target.com
```

**Batch scan:**
```bash
cat live-hosts.txt | whatweb -i - --log-json=tech-stack.json
```

**What it does:**
- Identifies 1800+ web technologies
- Detects CMS versions, frameworks, analytics, JavaScript libraries
- More detailed than httpx tech detection

**Output example:**
```
https://target.com [200 OK]
- WordPress[6.2.2]
- jQuery[3.6.0]
- Google Analytics[UA-12345678]
- PHP[7.4.33]
- Cloudflare
```

**Why this matters:**
- Version numbers = CVE lookups (WordPress 6.2.2 might have known bugs)
- Framework detection helps target specific vulnerabilities

---

## PHASE 3: DevOps Infrastructure Discovery

**This is HIGH IMPACT reconnaissance - DevOps tools are often:**
- Poorly secured (default credentials, no auth)
- Exposed to internet accidentally
- Contain sensitive data (source code, API keys, credentials)

### Tool 6: `nuclei`
**Purpose:** Automated vulnerability scanning with templates

**Installation:**
```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Download templates (REQUIRED)
nuclei -update-templates
```

**DevOps-focused scanning:**
```bash
# Scan for exposed DevOps tools
cat live-hosts.txt | nuclei -t exposures/ -o devops-exposures.txt

# Scan for misconfigurations
cat live-hosts.txt | nuclei -t misconfiguration/ -o misconfigs.txt

# Scan for default credentials
cat live-hosts.txt | nuclei -t default-logins/ -o default-creds.txt
```

**What it does:**
- Runs 7000+ detection templates
- Checks for exposed admin panels, Git repositories, config files
- Tests default credentials on common services
- Detects CVEs and misconfigurations

**Key template categories for DevOps:**
```bash
nuclei -t exposures/        # Exposed admin panels, dashboards
nuclei -t misconfiguration/ # Open S3 buckets, CORS issues
nuclei -t default-logins/   # Jenkins admin:admin, etc.
nuclei -t technologies/     # Detect specific DevOps tools
nuclei -t cves/             # Known CVEs
```

**Example findings:**
```
[jenkins-exposed] https://jenkins.target.com/login
[gitlab-public-repos] https://gitlab.target.com/explore
[grafana-default-creds] https://monitoring.target.com (admin:admin)
```

---

### Tool 7: Manual DevOps Tool Detection
**Purpose:** Use Jason Haddix's DevOps Attack Surface repo as reference

**Repository:** https://github.com/jhaddix/devops-attack-surface

**Process:**
1. Review your live-hosts.txt for keywords:
   - jenkins, gitlab, github, bitbucket (source control)
   - confluence, jira, notion (knowledge bases)
   - grafana, kibana, splunk (monitoring)
   - artifactory, nexus, registry (artifact repos)
   - vault, secrets (secrets management)

2. For each found tool, check the repo for:
   - Default credentials
   - Common attack vectors
   - Known CVEs
   - Exploitation techniques

**Example workflow:**
```bash
# Search for Jenkins instances
cat live-hosts.txt | grep -i jenkins

# Found: https://jenkins.target.com
# → Look up "Jenkins" in devops-attack-surface repo
# → Try default creds: admin/admin, jenkins/jenkins
# → Check for unauthenticated script console
# → Look for exposed build logs (might contain secrets)
```

---

## PHASE 4: Relationship Mapping

### Tool 8: `gospider`
**Purpose:** Web crawler to discover URLs, endpoints, JavaScript files

**Installation:**
```bash
go install github.com/jaeles-project/gospider@latest
```

**Basic Usage:**
```bash
gospider -s https://target.com -o gospider-output/
```

**Find JavaScript files (often contain API endpoints, secrets):**
```bash
gospider -s https://target.com -o gospider-output/ | grep "\.js$" | anew js-files.txt
```

**What it does:**
- Crawls website and finds all linked pages
- Extracts JavaScript files, API endpoints, forms
- Discovers hidden paths and parameters

**Why this matters for UEC:**
- JavaScript files reveal API endpoints (`/api/users`, `/api/payments`)
- API paths show data relationships (user → orders → payments)
- Forms show data flows (what data gets submitted where)

---

### Tool 9: `waybackurls`
**Purpose:** Extract historical URLs from Wayback Machine

**Installation:**
```bash
go install github.com/tomnomnom/waybackurls@latest
```

**Basic Usage:**
```bash
waybackurls target.com | anew historical-urls.txt
```

**Find old API endpoints:**
```bash
waybackurls target.com | grep -i api | anew api-endpoints.txt
```

**What it does:**
- Queries Internet Archive for all historical URLs
- Finds old endpoints that might still be live
- Discovers deprecated APIs (often less secure)

**Why this matters:**
- Old `/api/v1/` endpoints might not have same security as `/api/v2/`
- Deprecated features still accessible (forgotten attack surface)
- Historical changes show evolution of tech stack

---

### Tool 10: `gau` (Get All URLs)
**Purpose:** Fetch known URLs from multiple sources (Wayback, Common Crawl, etc.)

**Installation:**
```bash
go install github.com/lc/gau/v2/cmd/gau@latest
```

**Basic Usage:**
```bash
gau target.com | anew all-urls.txt
```

**Filter for interesting paths:**
```bash
# Find admin panels
gau target.com | grep -i admin

# Find API endpoints
gau target.com | grep -i api

# Find file uploads
gau target.com | grep -i upload
```

---

## PHASE 5: Vulnerability Discovery with Context

### Tool 11: `subjack`
**Purpose:** Subdomain takeover detection

**Installation:**
```bash
go install github.com/haccer/subjack@latest
```

**Basic Usage:**
```bash
subjack -w all-subdomains.txt -t 100 -timeout 30 -o takeovers.txt -ssl
```

**What it does:**
- Checks if subdomain points to unclaimed service (S3, GitHub Pages, Heroku)
- Detects CNAME records pointing to dead services
- Identifies potential subdomain takeover vulnerabilities

**Why this matters:**
- Medium-to-high severity bug ($500-$2000+)
- Easy to automate
- Clear yes/no result (either vulnerable or not)

---

### Tool 12: `nuclei` (Vulnerability Scanning)
**Purpose:** Automated vulnerability detection

**Focused vulnerability scanning:**
```bash
# After building your UEC model, run targeted scans

# Scan WordPress sites only
cat live-hosts.txt | grep wordpress | nuclei -t wordpress/

# Scan Jenkins instances
cat live-hosts.txt | grep jenkins | nuclei -t jenkins/

# Scan for exposed Git repos
cat live-hosts.txt | nuclei -t exposures/git/
```

**Why context matters:**
- Don't blindly scan everything (wastes time, triggers WAF)
- Target specific tech stack based on Phase 2 discovery
- Higher success rate with focused scanning

---

## Building Your UEC Model: Documentation Template

For each target, document:

### 1. Domain Profile
```
Primary Domain: target.com
Discovered Subdomains: 47
Live Web Hosts: 23
IP Ranges: 192.0.2.0/24, 198.51.100.0/24
ASN: AS12345 (Example Corp)
```

### 2. Technology Stack
```
Web Server: Nginx 1.21.6
Framework: Django 4.1 (Python)
Frontend: React 18.2
CDN: Cloudflare
Cloud Provider: AWS (detected via S3 buckets, CloudFront)
```

### 3. DevOps Infrastructure
```
Found Tools:
- Jenkins (https://jenkins.target.com) - Version 2.350
- GitLab (https://gitlab.target.com) - Public repos visible
- Grafana (https://monitoring.target.com) - Default creds work!
- Confluence (https://wiki.target.com) - Requires auth

Attack Surface:
- Jenkins script console accessible
- GitLab has 12 public repositories
- Grafana exposes internal metrics
```

### 4. API Endpoints Discovered
```
Public APIs:
- /api/v1/users (GET, POST)
- /api/v1/orders (GET, POST, DELETE)
- /api/v2/payments (POST)

Deprecated APIs (from Wayback):
- /api/v0/admin (still accessible!)
```

### 5. Data Relationships
```
User Flow:
1. User registers → /api/v1/users (creates account)
2. User orders → /api/v1/orders (references user_id)
3. Payment processed → /api/v2/payments (calls Stripe webhook)

Critical Path:
- Orders table links to payments
- Payments table contains Stripe customer IDs
- If IDOR in /api/v1/orders/{id}, could access payment info
```

### 6. High-Value Targets (Prioritized)
```
Priority 1: Jenkins (script console = RCE potential)
Priority 2: GitLab public repos (might contain secrets)
Priority 3: Grafana (internal metrics = info disclosure)
Priority 4: Deprecated /api/v0/admin endpoint
Priority 5: Subdomain takeover candidates (3 found)
```

---

## Automation Workflow: Chaining Tools Together

### Stage 1: Discovery Script
```bash
#!/bin/bash
DOMAIN=$1
OUTPUT_DIR="recon-$DOMAIN-$(date +%Y%m%d)"
mkdir -p $OUTPUT_DIR

echo "[*] Running subfinder..."
subfinder -d $DOMAIN -o $OUTPUT_DIR/subfinder.txt

echo "[*] Running amass..."
amass enum -passive -d $DOMAIN -o $OUTPUT_DIR/amass.txt

echo "[*] Merging results..."
cat $OUTPUT_DIR/subfinder.txt $OUTPUT_DIR/amass.txt | sort -u > $OUTPUT_DIR/all-subdomains.txt

echo "[*] Found $(wc -l < $OUTPUT_DIR/all-subdomains.txt) subdomains"
```

**Run:** `./recon-stage1.sh target.com`

---

### Stage 2: Host Validation + Tech Detection
```bash
#!/bin/bash
RECON_DIR=$1  # Pass the recon directory from Stage 1

echo "[*] Validating live hosts..."
cat $RECON_DIR/all-subdomains.txt | httpx -tech-detect -status-code -title -o $RECON_DIR/live-hosts.txt

echo "[*] Running deeper tech detection..."
cat $RECON_DIR/live-hosts.txt | whatweb -i - --log-json=$RECON_DIR/tech-stack.json

echo "[*] Found $(wc -l < $RECON_DIR/live-hosts.txt) live hosts"
```

**Run:** `./recon-stage2.sh recon-target.com-20251011`

---

### Stage 3: DevOps Discovery
```bash
#!/bin/bash
RECON_DIR=$1

echo "[*] Scanning for exposed DevOps tools..."
cat $RECON_DIR/live-hosts.txt | nuclei -t exposures/ -o $RECON_DIR/devops-exposures.txt

echo "[*] Checking default credentials..."
cat $RECON_DIR/live-hosts.txt | nuclei -t default-logins/ -o $RECON_DIR/default-creds.txt

echo "[*] Scanning for misconfigurations..."
cat $RECON_DIR/live-hosts.txt | nuclei -t misconfiguration/ -o $RECON_DIR/misconfigs.txt

# Manual keyword search
echo "[*] Searching for DevOps keywords..."
grep -iE "jenkins|gitlab|github|bitbucket|confluence|jira|grafana|kibana|artifactory|nexus" $RECON_DIR/live-hosts.txt > $RECON_DIR/devops-keywords.txt
```

**Run:** `./recon-stage3.sh recon-target.com-20251011`

---

### Stage 4: URL Discovery + Crawling
```bash
#!/bin/bash
RECON_DIR=$1
DOMAIN=$(basename $RECON_DIR | cut -d'-' -f2)

echo "[*] Fetching historical URLs..."
waybackurls $DOMAIN | anew $RECON_DIR/wayback-urls.txt
gau $DOMAIN | anew $RECON_DIR/all-urls.txt

echo "[*] Crawling live hosts..."
while read url; do
    echo "[*] Crawling $url"
    gospider -s $url -o $RECON_DIR/gospider/ --quiet
done < $RECON_DIR/live-hosts.txt

# Extract JavaScript files
find $RECON_DIR/gospider/ -type f -name "*.txt" -exec cat {} \; | grep "\.js$" | anew $RECON_DIR/js-files.txt

echo "[*] Found $(wc -l < $RECON_DIR/all-urls.txt) total URLs"
echo "[*] Found $(wc -l < $RECON_DIR/js-files.txt) JavaScript files"
```

**Run:** `./recon-stage4.sh recon-target.com-20251011`

---

### Stage 5: Vulnerability Detection
```bash
#!/bin/bash
RECON_DIR=$1

echo "[*] Checking for subdomain takeovers..."
subjack -w $RECON_DIR/all-subdomains.txt -t 100 -timeout 30 -o $RECON_DIR/takeovers.txt -ssl

echo "[*] Running targeted nuclei scans..."

# Check if WordPress sites exist
if grep -qi wordpress $RECON_DIR/tech-stack.json; then
    echo "[*] Found WordPress, running WP-specific scans..."
    cat $RECON_DIR/live-hosts.txt | grep -i wordpress | nuclei -t wordpress/ -o $RECON_DIR/wordpress-vulns.txt
fi

# Check if Jenkins exists
if grep -qi jenkins $RECON_DIR/live-hosts.txt; then
    echo "[*] Found Jenkins, running Jenkins-specific scans..."
    grep -i jenkins $RECON_DIR/live-hosts.txt | nuclei -t jenkins/ -o $RECON_DIR/jenkins-vulns.txt
fi

echo "[*] Running CVE scans on all hosts..."
cat $RECON_DIR/live-hosts.txt | nuclei -t cves/ -severity critical,high -o $RECON_DIR/cves.txt

echo "[*] Vulnerability scanning complete!"
```

**Run:** `./recon-stage5.sh recon-target.com-20251011`

---

## Full Automation: Master Script

```bash
#!/bin/bash
# Master UEC Reconnaissance Script
# Usage: ./uec-recon.sh target.com

DOMAIN=$1
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_DIR="uec-recon-$DOMAIN-$TIMESTAMP"

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 target.com"
    exit 1
fi

echo "=========================================="
echo "UEC Reconnaissance for: $DOMAIN"
echo "Output directory: $OUTPUT_DIR"
echo "=========================================="

# Create output directory
mkdir -p $OUTPUT_DIR

# PHASE 1: Domain Discovery
echo -e "\n[PHASE 1] Domain & Subdomain Discovery"
echo "[*] Running subfinder..."
subfinder -d $DOMAIN -o $OUTPUT_DIR/subfinder.txt -silent

echo "[*] Running amass..."
amass enum -passive -d $DOMAIN -o $OUTPUT_DIR/amass.txt

echo "[*] Merging results..."
cat $OUTPUT_DIR/subfinder.txt $OUTPUT_DIR/amass.txt 2>/dev/null | sort -u > $OUTPUT_DIR/all-subdomains.txt
SUBDOMAIN_COUNT=$(wc -l < $OUTPUT_DIR/all-subdomains.txt)
echo "[✓] Found $SUBDOMAIN_COUNT subdomains"

# PHASE 2: Tech Stack Discovery
echo -e "\n[PHASE 2] Technology Stack Identification"
echo "[*] Validating live hosts with httpx..."
cat $OUTPUT_DIR/all-subdomains.txt | httpx -tech-detect -status-code -title -silent -o $OUTPUT_DIR/live-hosts.txt

LIVE_COUNT=$(wc -l < $OUTPUT_DIR/live-hosts.txt)
echo "[✓] Found $LIVE_COUNT live hosts"

# PHASE 3: DevOps Discovery
echo -e "\n[PHASE 3] DevOps Infrastructure Discovery"
echo "[*] Scanning for exposed DevOps tools..."
cat $OUTPUT_DIR/live-hosts.txt | nuclei -t exposures/ -silent -o $OUTPUT_DIR/devops-exposures.txt

echo "[*] Checking default credentials..."
cat $OUTPUT_DIR/live-hosts.txt | nuclei -t default-logins/ -silent -o $OUTPUT_DIR/default-creds.txt

echo "[*] Searching for DevOps keywords..."
grep -iE "jenkins|gitlab|github|bitbucket|confluence|jira|grafana|kibana|artifactory|nexus|vault|splunk" $OUTPUT_DIR/live-hosts.txt > $OUTPUT_DIR/devops-keywords.txt 2>/dev/null

DEVOPS_COUNT=$(wc -l < $OUTPUT_DIR/devops-keywords.txt 2>/dev/null || echo 0)
echo "[✓] Found $DEVOPS_COUNT potential DevOps tools"

# PHASE 4: URL Discovery
echo -e "\n[PHASE 4] URL & Endpoint Discovery"
echo "[*] Fetching historical URLs from Wayback Machine..."
waybackurls $DOMAIN 2>/dev/null | anew $OUTPUT_DIR/all-urls.txt > /dev/null

echo "[*] Fetching URLs from Common Crawl..."
gau $DOMAIN 2>/dev/null | anew $OUTPUT_DIR/all-urls.txt > /dev/null

URL_COUNT=$(wc -l < $OUTPUT_DIR/all-urls.txt 2>/dev/null || echo 0)
echo "[✓] Found $URL_COUNT unique URLs"

# Extract interesting endpoints
grep -iE "/api/" $OUTPUT_DIR/all-urls.txt > $OUTPUT_DIR/api-endpoints.txt 2>/dev/null
grep -iE "admin|dashboard|panel|console" $OUTPUT_DIR/all-urls.txt > $OUTPUT_DIR/admin-paths.txt 2>/dev/null
grep -iE "\.js$" $OUTPUT_DIR/all-urls.txt > $OUTPUT_DIR/js-files.txt 2>/dev/null

API_COUNT=$(wc -l < $OUTPUT_DIR/api-endpoints.txt 2>/dev/null || echo 0)
ADMIN_COUNT=$(wc -l < $OUTPUT_DIR/admin-paths.txt 2>/dev/null || echo 0)
JS_COUNT=$(wc -l < $OUTPUT_DIR/js-files.txt 2>/dev/null || echo 0)

echo "[✓] Found $API_COUNT API endpoints"
echo "[✓] Found $ADMIN_COUNT admin paths"
echo "[✓] Found $JS_COUNT JavaScript files"

# PHASE 5: Vulnerability Detection
echo -e "\n[PHASE 5] Vulnerability Discovery"
echo "[*] Checking for subdomain takeovers..."
subjack -w $OUTPUT_DIR/all-subdomains.txt -t 100 -timeout 30 -o $OUTPUT_DIR/takeovers.txt -ssl 2>/dev/null

TAKEOVER_COUNT=$(wc -l < $OUTPUT_DIR/takeovers.txt 2>/dev/null || echo 0)
if [ $TAKEOVER_COUNT -gt 0 ]; then
    echo "[!] Found $TAKEOVER_COUNT potential subdomain takeovers!"
else
    echo "[✓] No subdomain takeovers found"
fi

echo "[*] Running misconfiguration scans..."
cat $OUTPUT_DIR/live-hosts.txt | nuclei -t misconfiguration/ -silent -o $OUTPUT_DIR/misconfigs.txt

MISCONFIG_COUNT=$(wc -l < $OUTPUT_DIR/misconfigs.txt 2>/dev/null || echo 0)
echo "[✓] Found $MISCONFIG_COUNT misconfigurations"

# Generate summary report
echo -e "\n=========================================="
echo "RECONNAISSANCE SUMMARY"
echo "=========================================="
echo "Target: $DOMAIN"
echo "Timestamp: $TIMESTAMP"
echo "Output: $OUTPUT_DIR"
echo ""
echo "Findings:"
echo "  - Subdomains: $SUBDOMAIN_COUNT"
echo "  - Live Hosts: $LIVE_COUNT"
echo "  - DevOps Tools: $DEVOPS_COUNT"
echo "  - Total URLs: $URL_COUNT"
echo "  - API Endpoints: $API_COUNT"
echo "  - Admin Paths: $ADMIN_COUNT"
echo "  - JavaScript Files: $JS_COUNT"
echo "  - Subdomain Takeovers: $TAKEOVER_COUNT"
echo "  - Misconfigurations: $MISCONFIG_COUNT"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review: $OUTPUT_DIR/devops-keywords.txt (high-impact targets)"
echo "2. Check: $OUTPUT_DIR/takeovers.txt (quick wins)"
echo "3. Analyze: $OUTPUT_DIR/api-endpoints.txt (for IDOR, auth issues)"
echo "4. Inspect: $OUTPUT_DIR/default-creds.txt (test credentials)"
echo ""
echo "[✓] Reconnaissance complete!"
```

**Save as:** `/Users/itza/Documents/vault_self/bcck_vault/LEARNING/methodologies/bug-bounty/uec-recon.sh`

**Make executable:** `chmod +x uec-recon.sh`

**Run:** `./uec-recon.sh target.com`

---

## Tool Installation Checklist

```bash
# Go-based tools (requires Go installed)
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/owasp-amass/amass/v4/...@master
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/jaeles-project/gospider@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/anew@latest
go install github.com/haccer/subjack@latest

# Update nuclei templates (REQUIRED)
nuclei -update-templates

# macOS-specific (using Homebrew)
brew install whatweb

# Verify installations
subfinder -version
httpx -version
nuclei -version
```

---

## Next Steps for Your Learning Path

### Week 1: Manual Tool Execution
- Run each tool individually against a test target
- Understand what each tool's output means
- Document findings in UEC template

### Week 2: Staged Automation
- Use Stage 1-5 scripts to automate portions
- Still review output manually
- Build your intuition for what's "interesting"

### Week 3: Full Automation
- Run master script on new targets
- Let it run overnight for comprehensive results
- Focus on analyzing output, not running tools

### Week 4: Integrate with DevOps Attack Surface
- When you find Jenkins/GitLab/etc., reference Haddix's repo
- Test default credentials systematically
- Document attack chains (e.g., Jenkins → source code → AWS keys → cloud access)

---

## Key Takeaways

1. **Build context FIRST** before hunting bugs
2. **DevOps infrastructure = high impact** targets (prioritize these)
3. **Automate recon**, not bug discovery (you still need to think)
4. **Document relationships** between systems (this is your competitive advantage)
5. **Start with easy wins** (subdomain takeovers, default creds) while building deeper skills

---

## Resources

- Jason Haddix DevOps Attack Surface: https://github.com/jhaddix/devops-attack-surface
- Jason Haddix KingOfBugBountyTips: https://github.com/jhaddix/KingOfBugBountyTips
- Daniel Miessler UEC Concept: https://danielmiessler.com/p/uec
- Nuclei Templates: https://github.com/projectdiscovery/nuclei-templates
- OWASP Amass Guide: https://github.com/owasp-amass/amass/blob/master/doc/user_guide.md
