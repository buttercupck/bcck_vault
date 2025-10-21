#!/bin/bash
# UEC Reconnaissance Master Script
# Purpose: Automated reconnaissance using Unified Entity Context methodology
# Author: Built for bug bounty learning
# Usage: ./uec-recon.sh target.com

set -e  # Exit on error

DOMAIN=$1
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_DIR="uec-recon-$DOMAIN-$TIMESTAMP"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Usage check
if [ -z "$DOMAIN" ]; then
    echo -e "${RED}Usage: $0 target.com${NC}"
    exit 1
fi

# Check if required tools are installed
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}[!] $1 is not installed. Please install it first.${NC}"
        exit 1
    fi
}

echo -e "${BLUE}[*] Checking required tools...${NC}"
check_tool subfinder
check_tool amass
check_tool httpx
check_tool nuclei
check_tool waybackurls
check_tool gau
check_tool anew
check_tool subjack

echo -e "${GREEN}[✓] All required tools are installed${NC}"
echo ""

echo "=========================================="
echo -e "${BLUE}UEC Reconnaissance for: $DOMAIN${NC}"
echo "Output directory: $OUTPUT_DIR"
echo "=========================================="

# Create output directory
mkdir -p $OUTPUT_DIR

# ============================================
# PHASE 1: Domain & Subdomain Discovery
# ============================================
echo -e "\n${YELLOW}[PHASE 1] Domain & Subdomain Discovery${NC}"
echo "[*] Running subfinder..."
subfinder -d $DOMAIN -o $OUTPUT_DIR/subfinder.txt -silent

echo "[*] Running amass..."
amass enum -passive -d $DOMAIN -o $OUTPUT_DIR/amass.txt

echo "[*] Merging results..."
cat $OUTPUT_DIR/subfinder.txt $OUTPUT_DIR/amass.txt 2>/dev/null | sort -u > $OUTPUT_DIR/all-subdomains.txt
SUBDOMAIN_COUNT=$(wc -l < $OUTPUT_DIR/all-subdomains.txt)
echo -e "${GREEN}[✓] Found $SUBDOMAIN_COUNT subdomains${NC}"

# ============================================
# PHASE 2: Technology Stack Identification
# ============================================
echo -e "\n${YELLOW}[PHASE 2] Technology Stack Identification${NC}"
echo "[*] Validating live hosts with httpx..."
cat $OUTPUT_DIR/all-subdomains.txt | httpx -tech-detect -status-code -title -silent -o $OUTPUT_DIR/live-hosts.txt

LIVE_COUNT=$(wc -l < $OUTPUT_DIR/live-hosts.txt)
echo -e "${GREEN}[✓] Found $LIVE_COUNT live hosts${NC}"

# ============================================
# PHASE 3: DevOps Infrastructure Discovery
# ============================================
echo -e "\n${YELLOW}[PHASE 3] DevOps Infrastructure Discovery${NC}"
echo "[*] Scanning for exposed DevOps tools..."
cat $OUTPUT_DIR/live-hosts.txt | nuclei -t exposures/ -silent -o $OUTPUT_DIR/devops-exposures.txt 2>/dev/null || touch $OUTPUT_DIR/devops-exposures.txt

echo "[*] Checking default credentials..."
cat $OUTPUT_DIR/live-hosts.txt | nuclei -t default-logins/ -silent -o $OUTPUT_DIR/default-creds.txt 2>/dev/null || touch $OUTPUT_DIR/default-creds.txt

echo "[*] Searching for DevOps keywords..."
grep -iE "jenkins|gitlab|github|bitbucket|confluence|jira|grafana|kibana|artifactory|nexus|vault|splunk|docker|kubernetes|k8s|travis|circleci" $OUTPUT_DIR/live-hosts.txt > $OUTPUT_DIR/devops-keywords.txt 2>/dev/null || touch $OUTPUT_DIR/devops-keywords.txt

DEVOPS_COUNT=$(wc -l < $OUTPUT_DIR/devops-keywords.txt 2>/dev/null || echo 0)
echo -e "${GREEN}[✓] Found $DEVOPS_COUNT potential DevOps tools${NC}"

# ============================================
# PHASE 4: URL & Endpoint Discovery
# ============================================
echo -e "\n${YELLOW}[PHASE 4] URL & Endpoint Discovery${NC}"
echo "[*] Fetching historical URLs from Wayback Machine..."
waybackurls $DOMAIN 2>/dev/null | anew $OUTPUT_DIR/all-urls.txt > /dev/null || touch $OUTPUT_DIR/all-urls.txt

echo "[*] Fetching URLs from Common Crawl..."
gau $DOMAIN 2>/dev/null | anew $OUTPUT_DIR/all-urls.txt > /dev/null || true

URL_COUNT=$(wc -l < $OUTPUT_DIR/all-urls.txt 2>/dev/null || echo 0)
echo -e "${GREEN}[✓] Found $URL_COUNT unique URLs${NC}"

# Extract interesting endpoints
echo "[*] Categorizing discovered URLs..."
grep -iE "/api/" $OUTPUT_DIR/all-urls.txt > $OUTPUT_DIR/api-endpoints.txt 2>/dev/null || touch $OUTPUT_DIR/api-endpoints.txt
grep -iE "admin|dashboard|panel|console|phpmyadmin|adminer" $OUTPUT_DIR/all-urls.txt > $OUTPUT_DIR/admin-paths.txt 2>/dev/null || touch $OUTPUT_DIR/admin-paths.txt
grep -iE "\.js$" $OUTPUT_DIR/all-urls.txt > $OUTPUT_DIR/js-files.txt 2>/dev/null || touch $OUTPUT_DIR/js-files.txt
grep -iE "\.json$|\.xml$|\.yml$|\.yaml$|\.config$" $OUTPUT_DIR/all-urls.txt > $OUTPUT_DIR/config-files.txt 2>/dev/null || touch $OUTPUT_DIR/config-files.txt

API_COUNT=$(wc -l < $OUTPUT_DIR/api-endpoints.txt 2>/dev/null || echo 0)
ADMIN_COUNT=$(wc -l < $OUTPUT_DIR/admin-paths.txt 2>/dev/null || echo 0)
JS_COUNT=$(wc -l < $OUTPUT_DIR/js-files.txt 2>/dev/null || echo 0)
CONFIG_COUNT=$(wc -l < $OUTPUT_DIR/config-files.txt 2>/dev/null || echo 0)

echo -e "${GREEN}[✓] Found $API_COUNT API endpoints${NC}"
echo -e "${GREEN}[✓] Found $ADMIN_COUNT admin paths${NC}"
echo -e "${GREEN}[✓] Found $JS_COUNT JavaScript files${NC}"
echo -e "${GREEN}[✓] Found $CONFIG_COUNT config files${NC}"

# ============================================
# PHASE 5: Vulnerability Discovery
# ============================================
echo -e "\n${YELLOW}[PHASE 5] Vulnerability Discovery${NC}"
echo "[*] Checking for subdomain takeovers..."
subjack -w $OUTPUT_DIR/all-subdomains.txt -t 100 -timeout 30 -o $OUTPUT_DIR/takeovers.txt -ssl 2>/dev/null || touch $OUTPUT_DIR/takeovers.txt

TAKEOVER_COUNT=$(wc -l < $OUTPUT_DIR/takeovers.txt 2>/dev/null || echo 0)
if [ $TAKEOVER_COUNT -gt 0 ]; then
    echo -e "${RED}[!] Found $TAKEOVER_COUNT potential subdomain takeovers!${NC}"
else
    echo -e "${GREEN}[✓] No subdomain takeovers found${NC}"
fi

echo "[*] Running misconfiguration scans..."
cat $OUTPUT_DIR/live-hosts.txt | nuclei -t misconfiguration/ -silent -o $OUTPUT_DIR/misconfigs.txt 2>/dev/null || touch $OUTPUT_DIR/misconfigs.txt

MISCONFIG_COUNT=$(wc -l < $OUTPUT_DIR/misconfigs.txt 2>/dev/null || echo 0)
echo -e "${GREEN}[✓] Found $MISCONFIG_COUNT misconfigurations${NC}"

# ============================================
# Generate Summary Report
# ============================================
echo -e "\n=========================================="
echo -e "${GREEN}RECONNAISSANCE SUMMARY${NC}"
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
echo "  - Config Files: $CONFIG_COUNT"
echo "  - Subdomain Takeovers: $TAKEOVER_COUNT"
echo "  - Misconfigurations: $MISCONFIG_COUNT"
echo "=========================================="

# Save summary to file
cat > $OUTPUT_DIR/SUMMARY.txt << EOF
========================================
UEC RECONNAISSANCE SUMMARY
========================================
Target: $DOMAIN
Timestamp: $TIMESTAMP
Output Directory: $OUTPUT_DIR

FINDINGS:
  - Subdomains: $SUBDOMAIN_COUNT
  - Live Hosts: $LIVE_COUNT
  - DevOps Tools: $DEVOPS_COUNT
  - Total URLs: $URL_COUNT
  - API Endpoints: $API_COUNT
  - Admin Paths: $ADMIN_COUNT
  - JavaScript Files: $JS_COUNT
  - Config Files: $CONFIG_COUNT
  - Subdomain Takeovers: $TAKEOVER_COUNT
  - Misconfigurations: $MISCONFIG_COUNT

HIGH-PRIORITY FILES TO REVIEW:
1. $OUTPUT_DIR/devops-keywords.txt (DevOps infrastructure - HIGH IMPACT)
2. $OUTPUT_DIR/takeovers.txt (Subdomain takeovers - QUICK WINS)
3. $OUTPUT_DIR/default-creds.txt (Default credentials found)
4. $OUTPUT_DIR/api-endpoints.txt (Test for IDOR, auth bypass)
5. $OUTPUT_DIR/admin-paths.txt (Admin panels to investigate)
6. $OUTPUT_DIR/misconfigs.txt (Misconfigurations detected)

NEXT STEPS:
1. Review DevOps tools found (reference: https://github.com/jhaddix/devops-attack-surface)
2. Test subdomain takeovers (validate with manual checks)
3. Analyze API endpoints for authentication issues
4. Test default credentials on discovered services
5. Build UEC model documenting relationships between systems

========================================
EOF

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review: $OUTPUT_DIR/devops-keywords.txt (high-impact targets)"
echo "2. Check: $OUTPUT_DIR/takeovers.txt (quick wins)"
echo "3. Analyze: $OUTPUT_DIR/api-endpoints.txt (for IDOR, auth issues)"
echo "4. Inspect: $OUTPUT_DIR/default-creds.txt (test credentials)"
echo "5. Read: $OUTPUT_DIR/SUMMARY.txt (full summary)"
echo ""
echo -e "${GREEN}[✓] Reconnaissance complete!${NC}"
echo "Results saved to: $OUTPUT_DIR/"
