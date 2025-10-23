import sys
import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

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
    req = urllib.request.Request(url)
    req.add_header('Cookie', cookie_header)
    req.add_header('User-Agent', 'Mozilla/5.0')
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=15)
        return response.url, response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, str(e)

# Check if we get redirected with portal ID
print("[VALIDATION] Checking for Portal ID in redirect URL...")
final_url, content = fetch_url('https://app.hubspot.com/contacts')

if final_url:
    print(f"Final URL: {final_url}")
    # Extract portal ID from URL
    portal_match = re.search(r'/contacts[/-](\d+)/', final_url)
    if portal_match:
        portal_id = portal_match.group(1)
        print(f"✓ CONFIRMED: Portal ID found in URL: {portal_id}")
    else:
        print(f"✗ No Portal ID in URL path")

# Check for error reporting in head-dlb bundle
print("\n[VALIDATION] Fetching head-dlb.bundle to check error infrastructure...")
bundle_match = re.search(r'(https://[^"]+head-dlb[^"]+\.js)', content)
if bundle_match:
    bundle_url = bundle_match.group(1)
    print(f"Bundle URL: {bundle_url[:80]}...")
    
    _, bundle_content = fetch_url(bundle_url)
    if bundle_content and 'exceptions.hubspot.com' in bundle_content:
        print(f"✓ CONFIRMED: exceptions.hubspot.com found in head-dlb bundle")
        
        # Extract the construction logic
        construction = re.search(r'exceptions[^;]{0,200}hubspot', bundle_content)
        if construction:
            snippet = construction.group(0)[:150]
            print(f"  Code snippet: {snippet}...")
    else:
        print(f"✗ exceptions.hubspot.com not found in bundle")
else:
    print(f"✗ head-dlb bundle URL not found")

