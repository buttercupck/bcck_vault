import sys
import urllib.request
import ssl
import json

# Create unverified SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read the recent cookie from cookies.txt
cookie_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/cookies.txt'

print("="*70)
print("ANALYZING cookies.txt - RECENT API CAPTURE")
print("="*70)

with open(cookie_file, 'r') as f:
    content = f.read()

# Parse the captured request
lines = content.split('\n')

print(f"\n[FILE CONTENT ANALYSIS]")
print(f"Total lines: {len(lines)}")

# Find the method/URL line and cookie line
method = None
path = None
cookie_header = None

for i, line in enumerate(lines):
    line = line.strip()
    if line.startswith('PUT ') or line.startswith('POST ') or line.startswith('GET '):
        method_line = line
        if ' ' in method_line:
            parts = method_line.split(' ', 1)
            method = parts[0]
            path = parts[1]
            print(f"[Line {i}] Found method line: {method} {path[:80]}...")
    elif line.startswith('Cookie: '):
        cookie_header = line.replace('Cookie: ', '').strip()
        print(f"[Line {i}] Found cookie header: {len(cookie_header)} chars")

print(f"\n[EXTRACTED DATA]")
print(f"Method: {method}")
print(f"Path: {path[:100] if path else 'None'}...")
print(f"Cookie length: {len(cookie_header) if cookie_header else 0} characters")

# Check if we found the required data
if not method or not path or not cookie_header:
    print(f"\n✗ ERROR: Could not extract required data from cookies.txt")
    print(f"  Method: {'✓' if method else '✗'}")
    print(f"  Path: {'✓' if path else '✗'}")
    print(f"  Cookie: {'✓' if cookie_header else '✗'}")
    sys.exit(1)

# Build full URL
base_url = 'https://app.hubspot.com'
full_url = f"{base_url}{path}"

print(f"\n[REQUEST DETAILS]")
print(f"Full URL: {full_url}")
print(f"Method: {method}")

# Extract portal and user IDs from URL
import re
portal_match = re.search(r'/portal/(\d+)/', path)
user_match = re.search(r'/user/(\d+)', path)

if portal_match:
    portal_id = portal_match.group(1)
    print(f"Portal ID: {portal_id}")

if user_match:
    user_id = user_match.group(1)
    print(f"User ID: {user_id}")

# Make the request
print(f"\n{'='*70}")
print("TESTING PRESENCE API ENDPOINT")
print('='*70)

req = urllib.request.Request(full_url, method=method)
req.add_header('Cookie', cookie_header)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
req.add_header('Content-Type', 'application/json')

# PUT requests usually need a body, try empty JSON
data = json.dumps({}).encode('utf-8')

try:
    response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
    status = response.status
    content = response.read().decode('utf-8', errors='ignore')

    print(f"✓ Status: {status}")
    print(f"✓ Content Length: {len(content)} bytes")

    # Try to parse as JSON
    try:
        json_response = json.loads(content)
        print(f"✓ Response Type: JSON")
        print(f"  Response keys: {list(json_response.keys())}")
        print(f"  Response:\n{json.dumps(json_response, indent=2)}")

        print(f"\n✓✓✓ PRESENCE API ENDPOINT WORKING")
        print(f"✓✓✓ Authentication successful")
        print(f"✓✓✓ Track B Finding #3 (Portal ID in URLs) VALIDATED")

    except json.JSONDecodeError:
        print(f"✓ Response (not JSON): {content[:500]}")

except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error {e.code}: {e.reason}")

    try:
        error_content = e.read().decode('utf-8', errors='ignore')
        print(f"  Error content: {error_content[:500]}")

        try:
            error_json = json.loads(error_content)
            print(f"  Error JSON: {json.dumps(error_json, indent=2)}")
        except:
            pass
    except:
        pass

    if e.code == 401:
        print(f"  → Cookies may be expired")
    elif e.code == 403:
        print(f"  → Insufficient permissions")
    elif e.code == 404:
        print(f"  → Endpoint doesn't exist")

except Exception as e:
    print(f"✗ Error: {e}")

print(f"\n{'='*70}")
print("ANALYSIS COMPLETE")
print('='*70)
