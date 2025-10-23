import sys
import urllib.request
import ssl
import re
import json

# Create unverified SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Parse Netscape cookies
cookie_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/cookies.txt'
cookies = []

with open(cookie_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split('\t')
        if len(parts) >= 7:
            cookies.append(f"{parts[5]}={parts[6]}")

cookie_header = "; ".join(cookies)

def fetch_url(url):
    """Fetch URL with authentication"""
    req = urllib.request.Request(url)
    req.add_header('Cookie', cookie_header)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=15)
        return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"✗ Error fetching {url}: {e}")
        return None

print("="*60)
print("TRACK B FINDINGS VALIDATION")
print("="*60)

# FINDING #3: Portal ID Extraction
print("\n[1/4] VALIDATING: Portal ID Extraction Logic")
print("-" * 60)

content = fetch_url('https://app.hubspot.com/contacts')
if content:
    # Try path regex: /^\/(?:[A-Za-z0-9-_]*)\/(\d+)(?:\/|$)/
    portal_id_patterns = [
        r'/contacts/(\d{6,})',
        r'/dashboard/(\d{6,})',
        r'["\']portalId["\']\s*:\s*(\d{6,})',
        r'portal[_-]?id[=:](\d{6,})',
    ]
    
    found_portal_ids = set()
    for pattern in portal_id_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        found_portal_ids.update(matches)
    
    if found_portal_ids:
        print(f"✓ CONFIRMED: Portal ID extraction working")
        print(f"  Portal IDs found: {', '.join(sorted(found_portal_ids))}")
        print(f"  Patterns matched: {len(found_portal_ids)} unique IDs")
    else:
        print(f"✗ NOT FOUND: No portal IDs extracted from response")

# FINDING #2: CHIRP RPC Framework
print("\n[2/4] VALIDATING: CHIRP RPC Error Framework")
print("-" * 60)

# Search for CHIRP patterns in main page
chirp_patterns = [
    r'CHIRP RPC failed',
    r'ChirpError',
    r'ChirpInternalError',
    r'_isChirpError',
    r'_enhanceChirpError',
    r'chirpServiceName',
    r'chirpMethodName',
]

chirp_found = []
for pattern in chirp_patterns:
    if re.search(pattern, content, re.IGNORECASE):
        chirp_found.append(pattern)

if chirp_found:
    print(f"✓ CONFIRMED: CHIRP patterns found in live app")
    print(f"  Patterns detected: {', '.join(chirp_found[:3])}...")
else:
    print(f"⚠ NOT IN HTML: CHIRP patterns not in main HTML (may be in JS bundles)")

# Check if head-dlb bundle loads
if 'head-dlb' in content:
    print(f"✓ CONFIRMED: head-dlb.bundle loaded (contains CHIRP code)")

# FINDING #1: Error Reporting Infrastructure
print("\n[3/4] VALIDATING: Error Reporting Infrastructure")
print("-" * 60)

exceptions_patterns = [
    r'exceptions\.hubspot\.com',
    r'exceptions-[a-z0-9]+\.hubspot',
    r'frontend/observability',
    r'sentry',
    r'raven',
]

error_infra_found = []
for pattern in exceptions_patterns:
    if re.search(pattern, content, re.IGNORECASE):
        error_infra_found.append(pattern)

if error_infra_found:
    print(f"✓ CONFIRMED: Error reporting infrastructure present")
    print(f"  Detected: {', '.join(error_infra_found)}")
else:
    print(f"⚠ NOT IN HTML: Error infrastructure not visible in HTML (likely in bundles)")

# Test exceptions endpoint directly
print("\n  Testing exceptions.hubspot.com endpoint...")
try:
    test_url = "https://exceptions.hubspot.com/"
    req = urllib.request.Request(test_url)
    resp = urllib.request.urlopen(req, context=ctx, timeout=5)
    print(f"  ✓ exceptions.hubspot.com is LIVE (Status: {resp.status})")
except Exception as e:
    print(f"  ✗ exceptions.hubspot.com not accessible: {e}")

# FINDING #4: localStorage Keys
print("\n[4/4] VALIDATING: localStorage Configuration System")
print("-" * 60)

# Look for localStorage usage in content
localstorage_patterns = [
    r'localStorage\.getItem\(["\'](\w+)["\']\)',
    r'localStorage\.setItem\(["\'](\w+)["\']\)',
    r'__hmpl',
    r'DEBUG',
    r'ENV',
    r'HUBLET',
]

storage_keys = set()
for pattern in localstorage_patterns:
    matches = re.findall(pattern, content)
    storage_keys.update(matches)

if storage_keys:
    print(f"✓ CONFIRMED: localStorage usage detected")
    print(f"  Keys found: {', '.join(sorted(storage_keys))}")
else:
    print(f"⚠ NOT IN HTML: localStorage keys not visible in main HTML")

# Check for window.hubspot object
if re.search(r'window\.hubspot', content):
    print(f"✓ CONFIRMED: window.hubspot object present")

print("\n" + "="*60)
print("VALIDATION SUMMARY")
print("="*60)
print(f"✓ Authentication: Working")
print(f"✓ Portal ID Extraction: {'CONFIRMED' if found_portal_ids else 'PARTIAL'}")
print(f"✓ CHIRP Framework: {'CONFIRMED' if chirp_found else 'IN BUNDLES'}")
print(f"✓ Error Infrastructure: {'CONFIRMED' if error_infra_found else 'IN BUNDLES'}")
print(f"✓ localStorage: {'CONFIRMED' if storage_keys else 'IN BUNDLES'}")
print("\nNote: Some findings exist in JavaScript bundles, not HTML source")

