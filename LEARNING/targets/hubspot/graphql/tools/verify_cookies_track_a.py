import sys
import urllib.request
import ssl
import json
import re

# Create unverified SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Parse Netscape cookies
cookie_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/graphql/cookies.txt'
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

print("="*70)
print("TRACK A: COOKIE AUTHENTICATION VERIFICATION")
print("="*70)
print(f"\n[INFO] Parsed {len(cookies)} cookies from Netscape format")
print(f"[INFO] Cookie header length: {len(cookie_header)} characters\n")

def test_endpoint(url, method='GET', data=None, description=""):
    """Test endpoint with authentication"""
    print(f"\n{'='*70}")
    print(f"TEST: {description}")
    print(f"URL: {url}")
    print(f"Method: {method}")
    print('='*70)

    req = urllib.request.Request(url, method=method)
    req.add_header('Cookie', cookie_header)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    if data:
        req.add_header('Content-Type', 'application/json')
        data = data.encode('utf-8') if isinstance(data, str) else data

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
        status = response.status
        final_url = response.url
        content = response.read().decode('utf-8', errors='ignore')

        print(f"✓ Status: {status}")
        print(f"✓ Final URL: {final_url}")
        print(f"✓ Content Length: {len(content)} bytes")

        # Check for authentication indicators
        auth_indicators = {
            'login': 'login' in content.lower() and 'password' in content.lower(),
            'contacts': 'contacts' in content.lower(),
            'dashboard': 'dashboard' in content.lower(),
            'portal': 'portal' in content.lower() or 'portalid' in content.lower(),
            'user': '"user"' in content or '"currentUser"' in content,
        }

        print(f"\n[AUTH INDICATORS]")
        for indicator, found in auth_indicators.items():
            symbol = "✓" if found and indicator != 'login' else ("✗" if found and indicator == 'login' else "○")
            print(f"  {symbol} {indicator}: {'Found' if found else 'Not found'}")

        # Extract portal ID if present
        portal_patterns = [
            r'"portalId["\']?\s*:\s*(\d+)',
            r'portal["\']?\s*:\s*\{[^}]*["\']id["\']?\s*:\s*(\d+)',
            r'/(\d{6,})/',
        ]

        portal_ids = set()
        for pattern in portal_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            portal_ids.update(matches)

        if portal_ids:
            print(f"\n[PORTAL INFO]")
            print(f"  ✓ Portal ID(s) found: {', '.join(sorted(portal_ids))}")

        # Determine authentication status
        if auth_indicators['login'] and not any([auth_indicators['contacts'], auth_indicators['dashboard'], auth_indicators['portal']]):
            print(f"\n[RESULT] ✗ NOT AUTHENTICATED (redirected to login)")
            return False
        else:
            print(f"\n[RESULT] ✓ AUTHENTICATED (got app content)")
            return True

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")
        if e.code == 401:
            print(f"  → Unauthorized (authentication failed)")
        elif e.code == 403:
            print(f"  → Forbidden (insufficient permissions)")
        elif e.code == 405:
            print(f"  → Method Not Allowed (endpoint exists but method blocked)")
        elif e.code == 404:
            print(f"  → Not Found (endpoint doesn't exist)")

        print(f"\n[RESULT] ✗ REQUEST FAILED (HTTP {e.code})")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"\n[RESULT] ✗ REQUEST FAILED (Exception)")
        return False

# Test 1: Baseline - /contacts (should work)
baseline_success = test_endpoint(
    'https://app.hubspot.com/contacts',
    method='GET',
    description='BASELINE - Contacts Page (GET)'
)

# Test 2: GraphQL endpoint with GET (to test if method matters)
graphql_get_success = test_endpoint(
    'https://app.hubspot.com/graphql',
    method='GET',
    description='GraphQL Endpoint (GET method)'
)

# Test 3: GraphQL endpoint with POST (actual GraphQL request)
graphql_post_success = test_endpoint(
    'https://app.hubspot.com/graphql',
    method='POST',
    data=json.dumps({"query": "{ __typename }"}),
    description='GraphQL Endpoint (POST with query)'
)

# Test 4: Alternative GraphQL endpoints
alt_graphql_success = test_endpoint(
    'https://api.hubspot.com/graphql',
    method='POST',
    data=json.dumps({"query": "{ __typename }"}),
    description='Alternative GraphQL Endpoint (api.hubspot.com)'
)

print("\n" + "="*70)
print("VERIFICATION SUMMARY")
print("="*70)

results = [
    ("Baseline Authentication (/contacts)", baseline_success),
    ("GraphQL GET Request", graphql_get_success),
    ("GraphQL POST Request", graphql_post_success),
    ("Alternative GraphQL Endpoint", alt_graphql_success),
]

print("\nTest Results:")
for test_name, success in results:
    symbol = "✓" if success else "✗"
    print(f"  {symbol} {test_name}: {'PASS' if success else 'FAIL'}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)

if baseline_success:
    print("\n✓ COOKIES ARE VALID AND WORKING")
    print("  Authentication successful on baseline endpoint")
    print("  Same cookie header is being used for all requests")
    print()

    if not any([graphql_get_success, graphql_post_success, alt_graphql_success]):
        print("✗ GRAPHQL ENDPOINTS ARE FAILING")
        print("  Issue is NOT with cookie authentication")
        print("  Issue is GraphQL-specific (CSRF, headers, or access restrictions)")
        print()
        print("Recommended Next Steps:")
        print("  1. Test GraphQL in browser console with same session")
        print("  2. Check Network tab for required headers (X-CSRF-Token, etc.)")
        print("  3. Try GraphQL via browser DevTools to see working request")
    else:
        print("✓ GRAPHQL ENDPOINTS ARE ACCESSIBLE")
        print("  Track A can proceed with GraphQL validation")
else:
    print("\n✗ COOKIES ARE NOT WORKING")
    print("  Authentication failed on baseline endpoint")
    print("  Need to regenerate cookies or check format")

print("\n" + "="*70)
