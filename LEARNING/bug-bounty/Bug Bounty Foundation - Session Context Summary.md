---
Date: October 11, 2025
Session Goal: Build 5-hour foundation for bug bounty hunting with UEC-driven approach
---
## 🎯 Session Overview

This session established a comprehensive bug bounty learning plan centered around **Unified Entity Context (UEC)** methodology, DevOps reconnaissance, and strategic tool usage. The approach moves beyond random vulnerability scanning toward building complete target models that reveal high-impact attack chains.

---

## 📚 Key Concepts Learned

### **1. Unified Entity Context (UEC) - Daniel Miessler**

**Definition:** A comprehensive, unified model of a target organization that maps relationships between systems, technologies, and infrastructure. The core principle: *most hard decisions become simple with enough context*.

**Core Insight:** 
- Attackers are already building unified world models of their targets using AI
- The more context you have about a problem, the less expertise you need to solve it
- Vulnerability management difficulty stems from lack of organizational knowledge, not security expertise

**UEC Application to Bug Bounty:**
- Traditional approach: Find vulnerability → Report → Hope for impact
- UEC approach: Build target model → Understand relationships → Find vulnerability with full context → Report with business impact → Higher severity/payout

**Example Impact:**
- Without UEC: "Found IDOR in /api/users/{id}"
- With UEC: "Found IDOR in /api/users/{id} that connects to payment processing (Stripe webhooks). Attacker could access 50k+ customer payment info because this endpoint is called during mobile app checkout (discovered via public GitHub Actions workflows)."

### **2. DevOps Attack Surface - Jason Haddix**

**Repository:** github.com/jhaddix/devops-attack-surface

**What It Contains:**
1. **Default Credentials Database** (52+ services)
   - Databases, web apps, CMS, network devices, cloud services, IoT
   - Examples: Jenkins, GitLab, Jira, WordPress, MongoDB, Docker

2. **Service Accounts Reference** (30+ accounts)
   - Windows, Linux, Cloud service accounts
   - Privilege levels, attack techniques, exploitation commands

3. **DevOps Tools Attack Vectors** (60+ tools)
   - Categories: Knowledge bases, source control, CI/CD, repos, config management, secrets managers
   - Each tool includes: attack vectors, default creds, CVEs, OPSEC considerations

**Why DevOps Recon First:**
- DevOps tools are high-impact, low-hanging fruit
- Often poorly secured (default creds, no auth, exposed to internet)
- Provide intelligence goldmine:
  - Source code access → Find bugs in actual app
  - API keys & secrets → AWS creds, database passwords, tokens
  - Infrastructure map → How everything connects
  - Technology stack → Frameworks, versions, dependencies
  - Internal documentation → Wikis, internal APIs

**Common DevOps Tools to Target:**
- **CI/CD:** Jenkins, CircleCI, GitHub Actions, GitLab CI
- **Source Control:** GitHub Enterprise, GitLab, Bitbucket
- **Artifact Repos:** Artifactory, Nexus, Docker Registry
- **Config Management:** Ansible, Terraform, Puppet, Chef
- **Monitoring:** Grafana, Splunk, ELK Stack, Prometheus
- **Secrets:** HashiCorp Vault, AWS Secrets Manager, CyberArk
- **Knowledge:** Confluence, SharePoint, Notion, Jira

### **3. KingOfBugBountyTips - Jason Haddix**

**Repository:** github.com/jhaddix/KingOfBugBountyTips

**What It Is:** Collection of one-liner commands and automation workflows from successful bug bounty hunters. Shows how to chain tools together for maximum efficiency.

**Key Learning:** Not just individual tools, but workflows that combine:
- `subfinder` → subdomain discovery
- `httpx` → live host checking + tech detection
- `gospider` → web crawling
- `nuclei` → vulnerability scanning
- `waybackurls` → historical URL discovery
- `anew` → deduplication
- Tool chaining with pipes for automated recon

*Example Workflow:** ```bash chaos -d target.com | httpx -silent | xargs -I@ gospider -s "@" | grep "\.js$" | anew # Gets subdomains → checks alive → crawls each → finds JS files → deduplicates
