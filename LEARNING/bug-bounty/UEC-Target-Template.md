# UEC Target Profile: [TARGET_NAME]

**Date Started:** YYYY-MM-DD
**Program:** HackerOne / Bugcrowd / Intigriti / Other
**Scope:** In-scope / Out-of-scope items
**Reconnaissance Output:** `uec-recon-[domain]-[timestamp]/`

---

## Executive Summary
<!-- Brief 2-3 sentence overview of the target -->
[TARGET_NAME] is a [industry] company that provides [services]. Main attack surface includes [web apps/APIs/mobile apps]. Primary tech stack appears to be [framework/language].

---

## 1. Domain Profile

### Primary Domains
- **Main Domain:** example.com
- **Alternate Domains:** example.io, example.app

### Subdomain Discovery
| Metric | Count |
|--------|-------|
| Total Subdomains | 0 |
| Live Web Hosts | 0 |
| Unique IP Addresses | 0 |

**Key Subdomains:**
```
api.example.com         - API Gateway
app.example.com         - Main Application
staging.example.com     - Staging Environment
admin.example.com       - Admin Panel
jenkins.example.com     - CI/CD (Jenkins)
```

### Network Information
- **ASN:** AS##### ([Organization Name])
- **IP Ranges:**
  - `192.0.2.0/24` (Primary)
  - `198.51.100.0/24` (Secondary)
- **Cloud Provider:** AWS / Azure / GCP / Self-hosted
- **CDN:** Cloudflare / Akamai / Fastly / None

---

## 2. Technology Stack

### Web Technologies
| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| Web Server | Nginx | 1.21.6 | Standard config |
| Application Framework | Django | 4.1 | Python-based |
| Frontend Framework | React | 18.2 | SPA architecture |
| Database | PostgreSQL | 14.x | Detected via error messages |
| Cache | Redis | 6.x | Session storage |

### Third-Party Services
- **Authentication:** Auth0 / Okta / Custom
- **Payment Processing:** Stripe / PayPal / Square
- **Email Service:** SendGrid / Mailgun / AWS SES
- **Analytics:** Google Analytics / Mixpanel / Custom
- **CDN/WAF:** Cloudflare (detected)
- **Hosting:** AWS (EC2, S3, CloudFront)

### JavaScript Libraries & Dependencies
```
React 18.2.0
Axios 1.4.0
Redux 4.2.0
Lodash 4.17.21
Moment.js 2.29.4
```

---

## 3. DevOps Infrastructure Discovery

### Discovered DevOps Tools

#### 🔴 HIGH PRIORITY: Jenkins
- **URL:** https://jenkins.example.com
- **Version:** Jenkins 2.350
- **Status:** 🔴 Exposed to internet
- **Authentication:** Login page present
- **Default Creds Tested:** ❌ admin/admin (failed)
- **Attack Vectors:**
  - Script console access (if authenticated)
  - Build logs may contain secrets
  - Groovy script RCE potential
- **Reference:** [DevOps Attack Surface - Jenkins](https://github.com/jhaddix/devops-attack-surface)

#### 🟡 MEDIUM PRIORITY: GitLab
- **URL:** https://gitlab.example.com
- **Version:** GitLab CE 15.8
- **Status:** 🟡 Public repositories visible
- **Public Repos Found:** 12
- **Interesting Repos:**
  - `example-api` (API source code)
  - `infrastructure` (Terraform configs)
  - `deployment-scripts` (might contain secrets)
- **Attack Vectors:**
  - Search for hardcoded credentials in public repos
  - Look for `.env` files, API keys in commit history
  - Check CI/CD variables (if accessible)

#### 🟢 LOW PRIORITY: Grafana
- **URL:** https://monitoring.example.com
- **Version:** Grafana 9.3.2
- **Status:** 🟢 Requires authentication
- **Default Creds Tested:** ✅ admin/admin (WORKED!)
- **Findings:**
  - Internal metrics exposed
  - Database queries visible in dashboards
  - Server names and IPs disclosed
- **Impact:** Information disclosure (medium severity)

### DevOps Tools Checklist
Use this checklist to systematically search for common DevOps tools:

- [ ] **CI/CD Tools**
  - [ ] Jenkins (`jenkins.`, `ci.`, `build.`)
  - [ ] CircleCI (check for public pipelines)
  - [ ] Travis CI
  - [ ] GitHub Actions (check public repos)
  - [ ] GitLab CI

- [ ] **Source Control**
  - [ ] GitHub Enterprise
  - [ ] GitLab
  - [ ] Bitbucket
  - [ ] Gitea

- [ ] **Artifact Repositories**
  - [ ] Artifactory (`artifactory.`, `repo.`)
  - [ ] Nexus (`nexus.`)
  - [ ] Docker Registry (`registry.`, `docker.`)
  - [ ] npm registry

- [ ] **Configuration Management**
  - [ ] Ansible Tower
  - [ ] Terraform Cloud/Enterprise
  - [ ] Puppet Enterprise
  - [ ] Chef Server

- [ ] **Monitoring & Logging**
  - [ ] Grafana (`grafana.`, `monitoring.`)
  - [ ] Kibana (`kibana.`, `logs.`)
  - [ ] Splunk (`splunk.`)
  - [ ] Prometheus (`prometheus.`, `metrics.`)
  - [ ] ELK Stack

- [ ] **Secrets Management**
  - [ ] HashiCorp Vault (`vault.`)
  - [ ] AWS Secrets Manager
  - [ ] CyberArk

- [ ] **Knowledge Bases**
  - [ ] Confluence (`confluence.`, `wiki.`)
  - [ ] SharePoint
  - [ ] Notion (check for public pages)
  - [ ] Jira (`jira.`)

---

## 4. API Endpoints Discovered

### Public APIs

#### Main API (`https://api.example.com`)
**Base URL:** `https://api.example.com/v1/`

| Endpoint | Method | Auth Required | Parameters | Notes |
|----------|--------|---------------|------------|-------|
| `/users` | GET | ✅ Yes | `id`, `limit`, `offset` | Returns user list |
| `/users/{id}` | GET | ✅ Yes | - | **IDOR potential** |
| `/users` | POST | ❌ No | `email`, `password`, `name` | User registration |
| `/orders` | GET | ✅ Yes | `user_id`, `status` | Orders endpoint |
| `/orders/{id}` | GET | ✅ Yes | - | **IDOR potential** |
| `/payments` | POST | ✅ Yes | `order_id`, `amount`, `token` | Stripe integration |

**IDOR Testing Priority:**
1. `/users/{id}` - Can user A access user B's profile?
2. `/orders/{id}` - Can user A access user B's orders?
3. Check if sequential IDs are predictable

### Deprecated APIs (from Wayback Machine)

#### Old API v0 (Still Accessible!)
**Base URL:** `https://api.example.com/v0/`

| Endpoint | Method | Status | Security Issue |
|----------|--------|--------|----------------|
| `/admin` | GET | 200 OK | ⚠️ No auth required! |
| `/admin/users` | GET | 200 OK | Returns ALL users |
| `/internal/debug` | GET | 200 OK | Debug info exposed |

**Critical Finding:** API v0 endpoints still work and lack authentication that v1 has!

---

## 5. Data Relationships & Attack Chains

### System Architecture (Inferred)
```
User Registration Flow:
1. User submits form → POST /api/v1/users
2. User record created (ID: 12345)
3. Confirmation email sent (SendGrid)
4. User can login → JWT token issued

Order Flow:
1. User places order → POST /api/v1/orders
2. Order record created (references user_id)
3. Payment processed → POST /api/v1/payments (calls Stripe)
4. Stripe webhook confirms → /api/webhooks/stripe
5. Order status updated

Admin Access:
1. Admin logs in → admin.example.com
2. JWT token with role="admin"
3. Admin can access Jenkins (SSO integration?)
```

### Critical Data Flows
1. **User → Order → Payment**
   - User IDs link to orders
   - Orders link to payments
   - Payment info stored in database
   - **Risk:** IDOR in orders could expose payment details

2. **Jenkins → Source Code → AWS Credentials**
   - Jenkins builds pull from GitLab
   - Build scripts contain AWS keys (found in public repo!)
   - **Risk:** Jenkins access = AWS access

3. **Grafana → Database Queries**
   - Grafana dashboards show live database metrics
   - SQL queries visible in dashboard configs
   - **Risk:** Information disclosure, potential SQL injection if user input reaches queries

---

## 6. High-Value Targets (Prioritized)

### 🔴 Critical Priority
1. **Jenkins Script Console (if accessible)**
   - **Impact:** Remote Code Execution (RCE)
   - **Severity:** Critical ($5000+)
   - **Status:** Need to authenticate first

2. **Deprecated API v0 (No Auth)**
   - **Impact:** Access to all user data without authentication
   - **Severity:** High ($2000-5000)
   - **Status:** Validated - works!

3. **AWS Keys in Public GitLab Repo**
   - **Impact:** Cloud infrastructure takeover
   - **Severity:** Critical ($5000+)
   - **Status:** Need to verify if keys are still valid

### 🟡 Medium Priority
4. **IDOR in `/api/v1/orders/{id}`**
   - **Impact:** Access other users' order history + payment info
   - **Severity:** Medium-High ($1000-2500)
   - **Status:** Testing in progress

5. **Grafana Default Credentials**
   - **Impact:** Information disclosure (internal metrics)
   - **Severity:** Medium ($500-1000)
   - **Status:** Validated - admin/admin works

6. **Subdomain Takeover Candidates**
   - **Domains:** staging-old.example.com, legacy.example.com
   - **Impact:** Phishing, cookie theft, reputational damage
   - **Severity:** Medium ($500-2000)
   - **Status:** Need to verify if claimable

### 🟢 Low Priority (Long-term Testing)
7. **XSS in User Profile Fields**
   - **Status:** Hypothesis (need to test)
8. **SQL Injection in Search Feature**
   - **Status:** Hypothesis (need to test)

---

## 7. Attack Surface Notes

### Interesting Findings
- Jenkins is internet-facing (unusual - should be behind VPN)
- API v0 still works despite v1 being "current"
- Grafana using default credentials (low-hanging fruit)
- Public GitLab repos contain infrastructure code

### Security Observations
**Good:**
- Cloudflare WAF in place (may block some attacks)
- HTTPS enforced on all endpoints
- Rate limiting on API endpoints (tested)

**Bad:**
- DevOps tools exposed to internet
- Default credentials still work on some services
- Deprecated API endpoints not properly decommissioned
- Secrets in public repositories

### Potential Attack Chains
1. **Chain 1: GitLab → AWS → Data Exfiltration**
   - Access public GitLab repos
   - Extract AWS credentials from commit history
   - Use credentials to access S3 buckets
   - Exfiltrate customer data

2. **Chain 2: Grafana → Database Info → SQL Injection**
   - Login to Grafana with default creds
   - View database queries in dashboards
   - Identify vulnerable query patterns
   - Test SQL injection on main app

3. **Chain 3: IDOR → Payment Info → Account Takeover**
   - Exploit IDOR in `/orders/{id}`
   - Access victim's order history
   - Extract payment methods, addresses
   - Use info for account takeover

---

## 8. Testing Log

### 2025-10-11: Initial Reconnaissance
- Ran UEC recon script
- Discovered 47 subdomains
- Identified Jenkins, GitLab, Grafana
- Found 12 public GitLab repos

### 2025-10-12: DevOps Tool Testing
- [ ] Test Jenkins authentication bypass
- [ ] Download all public GitLab repos
- [ ] Search repos for secrets using `trufflehog`
- [ ] Test Grafana default creds
- [ ] Document internal metrics exposed

### 2025-10-13: API Testing
- [ ] Test IDOR in `/users/{id}`
- [ ] Test IDOR in `/orders/{id}`
- [ ] Test deprecated API v0 endpoints
- [ ] Check rate limiting behavior
- [ ] Test JWT token manipulation

### 2025-10-14: Subdomain Takeover
- [ ] Verify takeover candidates with `subjack`
- [ ] Attempt to claim unclaimed services
- [ ] Document proof-of-concept

---

## 9. Vulnerability Reports

### Report #1: Grafana Default Credentials
**Severity:** Medium
**Status:** Draft
**Details:** [Link to report draft]

### Report #2: Unauthenticated Access to API v0
**Severity:** High
**Status:** Submitted
**Response:** Pending

---

## 10. Resources & References

### Tools Used
- subfinder, amass (subdomain enumeration)
- httpx (live host validation)
- nuclei (vulnerability scanning)
- waybackurls, gau (historical URL discovery)
- subjack (subdomain takeover)

### External References
- [DevOps Attack Surface](https://github.com/jhaddix/devops-attack-surface)
- [King of Bug Bounty Tips](https://github.com/jhaddix/KingOfBugBountyTips)
- [Target's Bug Bounty Policy](https://example.com/security)

### Similar Targets
- [Other company with similar tech stack]
- [Lessons learned from X target]

---

## 11. Next Steps

**Immediate (Next 1-2 days):**
- [ ] Verify AWS keys are valid (from GitLab repo)
- [ ] Test IDOR vulnerabilities in user/order endpoints
- [ ] Attempt Jenkins authentication bypass
- [ ] Write report for API v0 unauthenticated access

**Short-term (Next week):**
- [ ] Deep dive into JavaScript files for API endpoints
- [ ] Test all deprecated API endpoints
- [ ] Search for secrets in all public repos
- [ ] Build automated monitoring for new subdomains

**Long-term (Ongoing):**
- [ ] Monitor for new CVEs affecting their tech stack
- [ ] Re-run recon weekly to find new subdomains
- [ ] Test new features as they're released
- [ ] Build relationship with security team

---

## 12. Lessons Learned

**What Worked:**
- UEC approach revealed DevOps infrastructure quickly
- Automated recon saved hours of manual work
- Focusing on DevOps tools first found high-impact issues

**What Didn't Work:**
- Initial XSS tests all blocked by WAF
- Rate limiting prevented brute-force attempts

**Improvements for Next Target:**
- Start with DevOps recon immediately
- Check for secrets in public repos first (quick wins)
- Document data relationships earlier in process

---

## Notes
<!-- Any additional observations, thoughts, or ideas -->

- Jenkins appears to use SSO (noticed redirect to login.example.com)
- Team seems security-aware (good reporting process)
- Response time to reports: ~48 hours average
- Consider asking for private program invite after a few accepted reports
