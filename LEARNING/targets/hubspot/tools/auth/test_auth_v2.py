import sys
import urllib.request
import ssl

# Create unverified context for testing
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read Netscape cookie file and convert to Cookie header
cookie_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/cookies.txt'
cookies = []

with open(cookie_file, 'r') as f:
    for line in f:
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Parse Netscape format: domain flag path secure expiry name value
        parts = line.split('\t')
        if len(parts) >= 7:
            name = parts[5]
            value = parts[6]
            cookies.append(f"{name}={value}")

cookie_header = "; ".join(cookies)

print(f"✓ Parsed {len(cookies)} cookies from Netscape format")
print(f"✓ Cookie header length: {len(cookie_header)} chars\n")

req = urllib.request.Request('https://app.hubspot.com/contacts')
req.add_header('Cookie', cookie_header)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    response = urllib.request.urlopen(req, context=ctx)
    print(f"✓ Status: {response.status}")
    print(f"✓ URL: {response.url}")
    content = response.read().decode('utf-8', errors='ignore')
    
    # Check for authentication indicators
    if 'login' in content.lower() and 'password' in content.lower():
        print("\n✗ Result: NOT AUTHENTICATED (redirected to login)")
        sys.exit(1)
    elif 'contacts' in content or 'dashboard' in content or 'portal' in content:
        print("\n✓ Result: AUTHENTICATED (got app content)")
        print("✓ Netscape cookies are working!")
        
        # Look for portal ID in content
        import re
        portal_match = re.search(r'/(\d{6,})/|portalid[=:](\d{6,})', content, re.IGNORECASE)
        if portal_match:
            portal_id = portal_match.group(1) or portal_match.group(2)
            print(f"✓ Found Portal ID: {portal_id}")
    else:
        print("\n? Result: UNKNOWN (check content)")
        print(f"Content preview: {content[:500]}")
        
except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error {e.code}: {e.reason}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
