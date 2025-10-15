# UEC Reconnaissance Workflow - Visual Guide

This diagram shows how each tool in the UEC methodology connects together, from manual execution to full automation.

---

## Phase-by-Phase Tool Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PHASE 1: DISCOVERY                          │
│                  Find all subdomains and domains                    │
└─────────────────────────────────────────────────────────────────────┘

    INPUT: target.com
       ↓
    ┌──────────────┐
    │  subfinder   │ ──→ subfinder.txt (passive subdomain discovery)
    └──────────────┘
       ↓
    ┌──────────────┐
    │    amass     │ ──→ amass.txt (comprehensive subdomain enum)
    └──────────────┘
       ↓
    ┌──────────────┐
    │  merge + sort│ ──→ all-subdomains.txt (47 subdomains)
    └──────────────┘
       ↓
    ┌──────────────┐
    │     anew     │ ──→ Deduplicate results
    └──────────────┘

OUTPUT: all-subdomains.txt
        ├─ api.target.com
        ├─ dev.target.com
        ├─ jenkins.target.com
        └─ staging.target.com

═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                 PHASE 2: TECHNOLOGY IDENTIFICATION                  │
│               Which hosts are live? What tech do they use?          │
└─────────────────────────────────────────────────────────────────────┘

    INPUT: all-subdomains.txt (47 subdomains)
       ↓
    ┌──────────────┐
    │    httpx     │ ──→ Probe HTTP/HTTPS
    │              │     Detect web servers
    │              │     Identify technologies
    └──────────────┘
       ↓
    live-hosts.txt (23 live hosts)
       ↓
    ┌──────────────┐
    │   whatweb    │ ──→ Deep tech fingerprinting
    │              │     Framework versions
    │              │     CMS detection
    └──────────────┘
       ↓
    tech-stack.json

OUTPUT: live-hosts.txt + tech-stack.json
        ├─ https://api.target.com [Nginx, Django, PostgreSQL]
        ├─ https://jenkins.target.com [Jenkins 2.350]
        └─ https://app.target.com [React, Cloudflare]

═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 3: DEVOPS INFRASTRUCTURE DISCOVERY               │
│          Find high-impact targets: CI/CD, repos, secrets            │
└─────────────────────────────────────────────────────────────────────┘

    INPUT: live-hosts.txt (23 hosts)
       ↓
    ┌──────────────┐
    │    nuclei    │ ──→ Scan with exposures/ templates
    │  (exposures) │     Find admin panels
    │              │     Detect DevOps tools
    └──────────────┘
       ↓
    devops-exposures.txt
       ↓
    ┌──────────────┐
    │    nuclei    │ ──→ Test default credentials
    │(default-login)│    admin/admin, jenkins/jenkins
    └──────────────┘
       ↓
    default-creds.txt
       ↓
    ┌──────────────┐
    │     grep     │ ──→ Search for DevOps keywords
    │   (manual)   │     jenkins|gitlab|confluence|grafana
    └──────────────┘
       ↓
    devops-keywords.txt

OUTPUT:
    devops-exposures.txt   → Exposed tools
    default-creds.txt      → Working credentials!
    devops-keywords.txt    → 5 DevOps tools found

REFERENCE: Check github.com/jhaddix/devops-attack-surface
           for each tool's attack vectors

═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                   PHASE 4: URL & ENDPOINT DISCOVERY                 │
│         Find all URLs, APIs, JavaScript files, admin paths          │
└─────────────────────────────────────────────────────────────────────┘

    INPUT: target.com
       ↓
    ┌──────────────┐
    │ waybackurls  │ ──→ Internet Archive historical URLs
    └──────────────┘
       ↓
    ┌──────────────┐
    │     anew     │ ──→ Deduplicate
    └──────────────┘
       ↓
    ┌──────────────┐
    │     gau      │ ──→ Common Crawl URLs
    └──────────────┘
       ↓
    ┌──────────────┐
    │     anew     │ ──→ Deduplicate again
    └──────────────┘
       ↓
    all-urls.txt (1247 URLs)
       ↓
    ┌─────────────────────────────────────────┐
    │    Categorize URLs (grep patterns)      │
    ├─────────────────────────────────────────┤
    │  grep "/api/"      → api-endpoints.txt  │
    │  grep "admin"      → admin-paths.txt    │
    │  grep "\.js$"      → js-files.txt       │
    │  grep "\.json$"    → config-files.txt   │
    └─────────────────────────────────────────┘

    PARALLEL: Web Crawling
    ┌──────────────┐
    │   gospider   │ ──→ Crawl each live host
    │              │     Extract links, forms
    │              │     Find JavaScript files
    └──────────────┘
       ↓
    gospider/ (directory of results)

OUTPUT:
    all-urls.txt       → 1247 total URLs
    api-endpoints.txt  → 89 API endpoints
    admin-paths.txt    → 12 admin panels
    js-files.txt       → 156 JavaScript files
    config-files.txt   → 23 config files

═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 5: VULNERABILITY DISCOVERY                      │
│        Use context from Phases 1-4 to find actual bugs             │
└─────────────────────────────────────────────────────────────────────┘

    INPUT: all-subdomains.txt
       ↓
    ┌──────────────┐
    │   subjack    │ ──→ Check for subdomain takeovers
    │              │     CNAME → dead service?
    └──────────────┘
       ↓
    takeovers.txt (3 candidates!)

    INPUT: live-hosts.txt
       ↓
    ┌──────────────┐
    │    nuclei    │ ──→ Scan for misconfigurations
    │  (misconfig) │     Open S3, CORS, etc.
    └──────────────┘
       ↓
    misconfigs.txt

    INPUT: tech-stack.json (WordPress detected)
       ↓
    ┌──────────────┐
    │    nuclei    │ ──→ WordPress-specific scans
    │  (wordpress) │     Known WP vulns
    └──────────────┘
       ↓
    wordpress-vulns.txt

    INPUT: devops-keywords.txt (Jenkins found)
       ↓
    ┌──────────────┐
    │    nuclei    │ ──→ Jenkins-specific scans
    │   (jenkins)  │     Script console, CVEs
    └──────────────┘
       ↓
    jenkins-vulns.txt

OUTPUT:
    takeovers.txt        → 3 subdomain takeovers
    misconfigs.txt       → 7 misconfigurations
    wordpress-vulns.txt  → 2 WP vulnerabilities
    jenkins-vulns.txt    → 1 exposed script console!

═══════════════════════════════════════════════════════════════════════
```

---

## Tool Dependency Tree

Shows which tools depend on outputs from other tools:

```
target.com (USER INPUT)
    ├── subfinder ────────────┐
    └── amass ────────────────┤
                              ├──> all-subdomains.txt
                              │       ├── httpx ──────────┐
                              │       │                   │
                              │       └── subjack         │
                              │           (takeovers)     │
                              │                           │
                              └── waybackurls ────┐       │
                              └── gau ────────────┤       │
                                                  │       │
                                                  ├──> all-urls.txt
                                                  │    ├── api-endpoints.txt
                                                  │    ├── admin-paths.txt
                                                  │    ├── js-files.txt
                                                  │    └── config-files.txt
                                                  │
                                                  └──> live-hosts.txt
                                                       ├── whatweb
                                                       │   (tech-stack.json)
                                                       │
                                                       ├── nuclei (exposures)
                                                       │   (devops-exposures.txt)
                                                       │
                                                       ├── nuclei (default-logins)
                                                       │   (default-creds.txt)
                                                       │
                                                       ├── nuclei (misconfiguration)
                                                       │   (misconfigs.txt)
                                                       │
                                                       └── gospider
                                                           (crawled-urls)

FINAL OUTPUTS:
    ├── Recon Data (for UEC model building)
    └── Vulnerabilities (for bug reports)
```

---

## Execution Flow: Manual → Semi-Automated → Fully Automated

### Stage 1: Complete Beginner (Week 1)
**Manual Tool-by-Tool Execution**

```
Day 1: Discovery
├─ Run: subfinder -d target.com
├─ Wait: Understand output
├─ Run: amass enum -d target.com
├─ Wait: Understand output
└─ Merge manually: cat sub*.txt | sort -u

Day 2: Validation
├─ Run: cat subdomains.txt | httpx
├─ Wait: Review live hosts
└─ Document: What tech did you see?

Day 3: DevOps Search
├─ Run: cat live.txt | nuclei -t exposures/
├─ Wait: Did you find Jenkins? GitLab?
└─ Reference: Check devops-attack-surface repo

Day 4: URL Discovery
├─ Run: waybackurls target.com
├─ Wait: Review historical URLs
└─ Document: Interesting endpoints?

Day 5: Vulnerability Testing
├─ Run: subjack on subdomains
├─ Wait: Any takeovers?
└─ Manual testing: Check what you found
```

**Goal:** Understand what each tool does and WHY.

---

### Stage 2: Intermediate (Week 2-3)
**Chain 2-3 Tools Together**

```
Mini-Script 1: Discovery Pipeline
└─ subfinder -d target.com | anew all-subs.txt
└─ amass enum -d target.com | anew all-subs.txt

Mini-Script 2: Validation + Tech Detection
└─ cat all-subs.txt | httpx -tech-detect > live.txt

Mini-Script 3: DevOps Focused Scan
└─ cat live.txt | nuclei -t exposures/,default-logins/ -o findings.txt

Mini-Script 4: URL Collection
└─ waybackurls target.com | anew urls.txt
└─ gau target.com | anew urls.txt
```

**Goal:** Build reusable mini-scripts for repeated tasks.

---

### Stage 3: Advanced (Week 4+)
**Full Automation Script**

```bash
./uec-recon.sh target.com

# This runs ALL phases automatically:
# ✓ Phase 1: Discovery (subfinder + amass)
# ✓ Phase 2: Tech detection (httpx + whatweb)
# ✓ Phase 3: DevOps hunting (nuclei)
# ✓ Phase 4: URL collection (waybackurls + gau + gospider)
# ✓ Phase 5: Vulnerability scanning (subjack + nuclei)
```

**Goal:** Reconnaissance runs automatically. You focus on analysis and exploitation.

---

## Visual: UEC Model Building Process

```
┌────────────────────────────────────────────────────────────────┐
│                    UEC MODEL BUILDING                          │
│                                                                │
│  Raw Recon Data         Context Layer        Final UEC Model  │
│  ───────────────        ─────────────        ───────────────  │
│                                                                │
│  47 subdomains     ──>  Group by function ──>  Attack Surface │
│    │                    (api, dev, admin)       Categories    │
│    └─> live-hosts       Identify roles                        │
│                                                                │
│  23 live hosts     ──>  Map technologies  ──>  Tech Stack Map │
│    │                    (Nginx, Django,         + Versions    │
│    └─> tech-stack       React, AWS)                           │
│                                                                │
│  5 DevOps tools    ──>  Research attack   ──>  High-Priority  │
│    │                    vectors for each       Target List    │
│    └─> devops-keywords  (use Haddix repo)                     │
│                                                                │
│  1247 URLs         ──>  Categorize by     ──>  Endpoint Map   │
│    │                    type (API, admin,     + Data Flows    │
│    └─> all-urls.txt     JS, config)                           │
│                                                                │
│  89 API endpoints  ──>  Map data flows    ──>  Relationship   │
│    │                    (user→order→pay)       Diagram        │
│    └─> api-endpoints                                          │
│                                                                │
│  3 takeovers       ──>  Validate + test   ──>  Vulnerability  │
│  7 misconfigs           business impact        Reports        │
│                                                                │
└────────────────────────────────────────────────────────────────┘

RESULT: Complete understanding of target = Better bugs = Higher payouts
```

---

## Progressive Learning Path

```
┌─────────────┐
│   WEEK 1    │  Learn individual tools
│   Manual    │  - Run each tool separately
│   Mode      │  - Understand output format
└─────┬───────┘  - Document findings manually
      │
      │ ✓ You understand WHAT each tool does
      ↓
┌─────────────┐
│   WEEK 2    │  Chain 2-3 tools together
│   Scripting │  - Write simple bash scripts
│   Mode      │  - Pipe outputs between tools
└─────┬───────┘  - Use anew for deduplication
      │
      │ ✓ You understand HOW tools connect
      ↓
┌─────────────┐
│   WEEK 3    │  Build staged automation
│  Semi-Auto  │  - 5 separate phase scripts
│   Mode      │  - Run phases sequentially
└─────┬───────┘  - Review output after each phase
      │
      │ ✓ You understand WHY tools are chained this way
      ↓
┌─────────────┐
│   WEEK 4+   │  Full automation
│   Expert    │  - Master script runs everything
│   Mode      │  - Focus on analysis, not execution
└─────────────┘  - Build UEC models from output
      │
      │ ✓ Recon is automated. You focus on finding bugs.
      ↓
┌─────────────┐
│  ONGOING    │  Continuous improvement
│  Mastery    │  - Add new tools to workflow
│             │  - Optimize for speed
└─────────────┘  - Share findings with community
```

---

## Quick Reference: Tool Chain Cheat Sheet

**1. Discovery Chain**
```bash
subfinder -d target.com | anew subs.txt
amass enum -d target.com | anew subs.txt
```

**2. Validation Chain**
```bash
cat subs.txt | httpx -tech-detect -o live.txt
```

**3. DevOps Discovery Chain**
```bash
cat live.txt | nuclei -t exposures/,default-logins/ -o findings.txt
grep -iE "jenkins|gitlab|grafana" live.txt > devops.txt
```

**4. URL Discovery Chain**
```bash
waybackurls target.com | anew urls.txt
gau target.com | anew urls.txt
grep "/api/" urls.txt > apis.txt
```

**5. Vulnerability Chain**
```bash
subjack -w subs.txt -o takeovers.txt
cat live.txt | nuclei -t misconfiguration/ -o misconfigs.txt
```

---

## Next Steps After Running Recon

```
Recon Complete ✓
    ↓
Review outputs in this order:
    1. devops-keywords.txt     (HIGH IMPACT targets first)
    2. takeovers.txt           (Quick wins - easy to validate)
    3. default-creds.txt       (Test these immediately)
    4. api-endpoints.txt       (Look for IDOR, auth issues)
    5. admin-paths.txt         (Check authentication)
    6. misconfigs.txt          (Validate findings)
    ↓
For each finding:
    ├─ Validate manually (don't trust tools 100%)
    ├─ Document in UEC Target Template
    ├─ Research attack vectors
    ├─ Test for exploitability
    └─ Write bug report
    ↓
Build UEC Model:
    ├─ Map all systems and relationships
    ├─ Document technology stack
    ├─ Identify data flows
    └─ Prioritize high-value targets
    ↓
Find Bugs with Context:
    ├─ Use UEC model to understand impact
    ├─ Chain vulnerabilities together
    └─ Write detailed reports with business impact
```

---

## Remember: Context = Higher Payouts

**Without UEC:**
```
Report: "Found IDOR in /api/users/123"
Severity: Medium
Payout: $500
```

**With UEC:**
```
Report: "Found IDOR in /api/users/123 which connects to payment
processing endpoint /api/payments. This allows attacker to access
50,000+ customer payment information because:

1. /api/users/{id} returns user's order IDs
2. Orders contain payment_method_id references
3. These link to Stripe customer IDs (discovered via public GitLab repo)
4. No authorization check between user access and payment data

Attack chain: IDOR → Order data → Payment IDs → Full Stripe customer access

Business impact: PCI-DSS violation, potential data breach of payment info"

Severity: Critical
Payout: $3000
```

**The difference? You built a complete UEC model first.**

---

## Summary

This workflow transforms you from:
- **Random scanning** → **Systematic reconnaissance**
- **Tool user** → **Tool chain builder**
- **Bug finder** → **Security researcher with context**

Start at Week 1 (manual mode). By Week 4, you'll have automation running while you focus on the high-skill work: analyzing findings and writing impactful bug reports.
