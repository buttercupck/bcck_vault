# HubSpot Attack Surface Expansion - Execution Plan
**Date**: 2025-10-23
**Target**: HubSpot infrastructure (1,044 live subdomains)
**Goal**: Find open ports, WebSocket endpoints, and misconfigured cloud storage

---

## Prerequisites

### ✅ Already Have
- 1,044 live subdomains (from subdomain enumeration)
- 511 active web services
- nmap (for port scanning)
- curl (for bucket testing)
- Basic reconnaissance tools

### ❌ Need to Install
- **masscan** - Fast port scanner (faster than nmap for initial sweep)
- **naabu** - Port scanner from Project Discovery
- **s3scanner** - AWS S3 bucket scanner
- **cloud_enum** - Multi-cloud storage enumeration
- **wscat** - WebSocket testing client

---

## Tool Installation (10 minutes)

### Step 1: Install Port Scanning Tools

```bash
# Install masscan (requires sudo)
brew install masscan

# Install naabu (Go-based fast port scanner)
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest

# Verify installations
masscan --version
naabu -version
```

### Step 2: Install Cloud Storage Tools

```bash
# Install s3scanner (Python)
pip3 install s3scanner --break-system-packages

# Install cloud_enum (multi-cloud)
git clone https://github.com/initstring/cloud_enum.git ~/tools/cloud_enum
cd ~/tools/cloud_enum && pip3 install -r requirements.txt --break-system-packages

# Verify
s3scanner --version
python3 ~/tools/cloud_enum/cloud_enum.py -h
```

### Step 3: Install WebSocket Tools

```bash
# Install wscat (Node.js WebSocket client)
npm install -g wscat

# Verify
wscat --version
```

---

## PHASE 1: Port Scanning (2-3 hours)

**Goal**: Find services running on non-standard ports (databases, admin panels, dev servers)

### 1.1: Fast Port Sweep with Naabu

**Why naabu first?**: Fast, accurate, designed for bug bounty (won't trigger aggressive IDS)

```bash
cd ~/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot
mkdir -p ports

# Scan top 1000 ports on all live subdomains
cat verified/live_subdomains.txt | cut -d' ' -f1 | \
  naabu -top-ports 1000 -rate 150 -silent -o ports/naabu_top1000.txt

# Expected: 5-20 minutes
# Output: Subdomain:Port pairs (e.g., admin.hubspot.com:8080)
```

### 1.2: Interesting Ports Only (High-Value Targets)

```bash
# Scan specific high-value ports on priority targets
cat priority/tier1_priority.txt | \
  naabu -p 21,22,23,25,53,80,110,143,443,445,3306,3389,5432,5900,6379,8000,8080,8443,8888,9090,27017 \
  -silent -o ports/naabu_interesting_ports.txt

# Expected: 3-5 minutes
# Ports explained:
# 21 - FTP (file access)
# 22 - SSH (potential credential testing)
# 3306 - MySQL (database exposure)
# 5432 - PostgreSQL (database)
# 6379 - Redis (cache, often no auth)
# 8080,8443,8888 - Alt HTTP ports (admin panels)
# 27017 - MongoDB (often exposed)
```

### 1.3: Service Detection on Open Ports

```bash
# For each open port found, identify the service
cat ports/naabu_top1000.txt | while read line; do
  host=$(echo $line | cut -d: -f1)
  port=$(echo $line | cut -d: -f2)
  echo "Scanning $host:$port..."
  nmap -sV -p $port $host -oN ports/service_${host}_${port}.txt
done > ports/service_detection.log 2>&1 &

# Expected: 20-40 minutes (run in background)
# Output: Detailed service version info
```

**Checkpoint 1**: Review `ports/naabu_top1000.txt` - look for unusual ports

---

## PHASE 2: WebSocket Discovery (30-45 minutes)

**Goal**: Find WebSocket endpoints for testing message injection, auth bypass

### 2.1: Identify WebSocket Endpoints from Web Services

```bash
mkdir -p websockets

# Search for WebSocket indicators in HTTP responses
cat verified/web_services.txt | grep -i "https://" | cut -d' ' -f1 | while read url; do
  echo "Checking $url for WebSocket..."
  curl -s "$url" | grep -iE "(ws://|wss://|websocket|socket\.io)" | \
    tee -a websockets/ws_indicators.txt
done

# Expected: 10-15 minutes
```

### 2.2: Common WebSocket Paths

```bash
# Test common WebSocket paths on high-priority targets
cat priority/tier1_priority.txt | while read subdomain; do
  for path in /ws /websocket /socket.io /realtime /live /notifications /chat; do
    echo "Testing wss://${subdomain}${path}"
    wscat -c "wss://${subdomain}${path}" --no-check 2>&1 | \
      grep -v "error: connect ECONNREFUSED" | \
      tee -a websockets/ws_discovery.txt
  done
done

# Expected: 5-10 minutes
```

### 2.3: Extract WebSocket URLs from JavaScript

```bash
# Download and search JavaScript files for WebSocket URLs
cat verified/web_services.txt | grep "https://" | cut -d' ' -f1 | while read url; do
  echo "Extracting JS from $url..."
  curl -s "$url" | grep -oE 'src="[^"]+\.js"' | cut -d'"' -f2 | while read js; do
    full_js="${url}${js}"
    curl -s "$full_js" | grep -oE '(ws://|wss://)[^"'\'']+' | \
      tee -a websockets/ws_from_js.txt
  done
done

# Expected: 15-20 minutes
```

**Checkpoint 2**: Review `websockets/ws_discovery.txt` for active WebSocket endpoints

---

## PHASE 3: Cloud Storage Discovery (1-2 hours)

**Goal**: Find misconfigured S3 buckets, Azure Blob, GCS buckets

### 3.1: Extract Bucket Names from Subdomains

```bash
mkdir -p buckets

# Generate potential S3 bucket names from subdomains
cat verified/live_subdomains.txt | cut -d' ' -f1 | while read subdomain; do
  # Remove .hubspot.com suffix
  prefix=$(echo $subdomain | sed 's/\.hubspot\.com//')
  
  # Common bucket patterns
  echo "${prefix}"
  echo "${prefix}-prod"
  echo "${prefix}-staging"
  echo "${prefix}-dev"
  echo "${prefix}-backup"
  echo "${prefix}-assets"
  echo "hubspot-${prefix}"
  echo "hubspot-${prefix}-prod"
done | sort -u > buckets/potential_bucket_names.txt

# Expected: Instant
# Output: 5,000-10,000 potential bucket names
```

### 3.2: Test AWS S3 Buckets

```bash
# Test top 500 most likely bucket names
head -500 buckets/potential_bucket_names.txt | while read bucket; do
  echo "Testing s3://${bucket}..."
  
  # Test if bucket exists and is accessible
  aws s3 ls s3://${bucket} --no-sign-request 2>&1 | \
    grep -v "NoSuchBucket" | grep -v "AccessDenied" | \
    tee -a buckets/s3_accessible.txt
    
  # Also test with s3scanner
  s3scanner scan --bucket ${bucket} 2>&1 | \
    grep -iE "(OPEN|WRITABLE|READABLE)" | \
    tee -a buckets/s3scanner_results.txt
done

# Expected: 30-45 minutes
# Rate limit: Don't exceed 100 requests/minute
```

### 3.3: Search for Buckets in Source Code

```bash
# Extract S3 URLs from web responses
cat verified/web_services.txt | grep "https://" | cut -d' ' -f1 | while read url; do
  echo "Searching $url for S3 URLs..."
  curl -s "$url" | grep -oE 'https://[^"'\'']+\.s3[^"'\'']+' | \
    tee -a buckets/s3_urls_from_web.txt
done

# Expected: 15-20 minutes
```

### 3.4: Extract Bucket Names from Previously Found JS

```bash
# Search JavaScript bundles for bucket references
# (Using the source-intel/js_files directory from previous work)
if [ -d source-intel/js_files ]; then
  grep -rh "s3\.amazonaws\.com\|\.s3\." source-intel/js_files/ | \
    grep -oE 'https://[^"'\'']+\.s3[^"'\'']+' | \
    sort -u > buckets/s3_from_source_code.txt
fi

# Expected: 2-3 minutes
```

### 3.5: Test Azure Blob Storage

```bash
# Test Azure blob storage (blob.core.windows.net)
head -200 buckets/potential_bucket_names.txt | while read name; do
  url="https://${name}.blob.core.windows.net/?restype=container&comp=list"
  echo "Testing Azure Blob: $url"
  
  curl -s -I "$url" | grep -iE "(200 OK|Content-Length: [1-9])" | \
    tee -a buckets/azure_accessible.txt
done

# Expected: 10-15 minutes
```

**Checkpoint 3**: Review `buckets/s3_accessible.txt` for exposed storage

---

## PHASE 4: Analysis & Prioritization (15 minutes)

### 4.1: Categorize Open Ports by Risk

```bash
# High-risk ports found
grep -E ":22$|:3306$|:5432$|:6379$|:27017$" ports/naabu_top1000.txt > ports/HIGH_RISK_PORTS.txt

# Medium-risk ports (alt HTTP, admin panels)
grep -E ":8080$|:8443$|:8888$|:9090$" ports/naabu_top1000.txt > ports/MEDIUM_RISK_PORTS.txt

# Count findings
echo "High-risk ports: $(wc -l < ports/HIGH_RISK_PORTS.txt)"
echo "Medium-risk ports: $(wc -l < ports/MEDIUM_RISK_PORTS.txt)"
```

### 4.2: Prioritize WebSocket Endpoints

```bash
# Extract unique WebSocket URLs
cat websockets/ws_*.txt | sort -u > websockets/ALL_WEBSOCKET_ENDPOINTS.txt

# Prioritize by subdomain
grep -E "(exceptions|qa\.|dev\.|staging)" websockets/ALL_WEBSOCKET_ENDPOINTS.txt > \
  websockets/HIGH_PRIORITY_WS.txt
```

### 4.3: Prioritize Cloud Storage Findings

```bash
# Combine all S3 findings
cat buckets/s3_accessible.txt buckets/s3_urls_from_web.txt buckets/s3_from_source_code.txt | \
  sort -u > buckets/ALL_ACCESSIBLE_BUCKETS.txt

# Check for WRITE permissions (critical!)
cat buckets/ALL_ACCESSIBLE_BUCKETS.txt | while read bucket; do
  aws s3 cp test.txt s3://${bucket}/test.txt --no-sign-request 2>&1 | \
    grep -v "AccessDenied" | tee -a buckets/WRITABLE_BUCKETS.txt
done
```

---

## Expected Output Files

```
LEARNING/targets/hubspot/
├── ports/
│   ├── naabu_top1000.txt (all open ports)
│   ├── naabu_interesting_ports.txt (specific high-value ports)
│   ├── service_detection.log (nmap service versions)
│   ├── HIGH_RISK_PORTS.txt (databases, SSH, etc.)
│   └── MEDIUM_RISK_PORTS.txt (alt HTTP ports)
│
├── websockets/
│   ├── ws_indicators.txt (WebSocket references in HTML)
│   ├── ws_discovery.txt (active WebSocket endpoints)
│   ├── ws_from_js.txt (WebSocket URLs from JavaScript)
│   ├── ALL_WEBSOCKET_ENDPOINTS.txt (combined)
│   └── HIGH_PRIORITY_WS.txt (priority targets)
│
└── buckets/
    ├── potential_bucket_names.txt (generated names)
    ├── s3_accessible.txt (readable S3 buckets)
    ├── s3scanner_results.txt (s3scanner findings)
    ├── s3_urls_from_web.txt (S3 URLs from web)
    ├── s3_from_source_code.txt (S3 URLs from JS)
    ├── azure_accessible.txt (Azure Blob findings)
    ├── ALL_ACCESSIBLE_BUCKETS.txt (combined)
    └── WRITABLE_BUCKETS.txt (CRITICAL - writable storage!)
```

---

## Testing Priorities After Discovery

### 🔴 CRITICAL - Test Immediately
1. **Writable S3 Buckets** → File upload, malware hosting, defacement
2. **Open Redis (6379)** → No auth, data exfiltration
3. **Open MongoDB (27017)** → Database access
4. **WebSockets on exceptions/qa subdomains** → Message injection

### 🟠 HIGH PRIORITY
5. **MySQL/PostgreSQL on non-standard hosts** → Credential stuffing
6. **SSH on unusual subdomains** → Credential testing
7. **Alt HTTP ports (8080, 8443)** → Admin panels, debug endpoints
8. **Readable S3 buckets** → Sensitive data exposure

### 🟡 MEDIUM PRIORITY
9. **WebSocket endpoints on production** → CSWSH, auth bypass
10. **Azure Blob accessible** → Check for sensitive data

---

## Safety Considerations

### Rate Limiting
- **Port scans**: Keep rate at 150 packets/second (naabu default)
- **Bucket enumeration**: Max 100 requests/minute
- **WebSocket testing**: 1 request per second

### Legal Boundaries
- ✅ **Allowed**: Port scanning, bucket name enumeration, WebSocket connection attempts
- ⚠️ **Caution**: Reading bucket contents (if accessible, just document)
- ❌ **NEVER**: Write to buckets, DDoS WebSockets, brute force SSH

### Responsible Disclosure
- If you find WRITABLE buckets → Immediate report to HubSpot
- If you find open databases → Do NOT access data, report immediately
- Document everything, take screenshots

---

## Timeline Estimate

**Today (Discovery Phase)**:
- 00:00-00:10 - Install missing tools
- 00:10-00:30 - Port scan with naabu (top 1000 ports)
- 00:30-01:00 - WebSocket discovery
- 01:00-02:00 - S3 bucket enumeration
- 02:00-02:15 - Analysis and prioritization
- 02:15-02:30 - Create testing plan for findings

**Total**: ~2.5-3 hours for complete discovery

**Tomorrow (Testing Phase)**:
- Test identified attack surfaces
- Focus on critical findings first

---

## Success Criteria

### Discovery Complete When:
- [ ] All 1,044 subdomains scanned for top 1000 ports
- [ ] Priority targets scanned for interesting ports
- [ ] Common WebSocket paths tested
- [ ] Top 500 bucket names enumerated
- [ ] Findings categorized by risk level

### High-Value Findings (Report Immediately):
- [ ] Writable S3 buckets
- [ ] Open databases (Redis, MongoDB, MySQL, PostgreSQL)
- [ ] SSH on unusual subdomains
- [ ] WebSocket endpoints on QA/staging

---

**Ready to execute? Reply "proceed" to start with tool installation.**
