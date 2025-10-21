#!/usr/bin/env python3
"""
HubSpot CHIRP RPC Framework Testing - Low-Privileged Account Template
Tests internal microservices API exposure and service enumeration
"""
import urllib.request
import ssl
import json

# ============================================================================
# CONFIGURATION - REPLACE WITH YOUR VALUES
# ============================================================================

HUBLET = "na2"  # Your hublet (check URL: app-na2.hubspot.com → na2)
PORTAL_ID = "YOUR_PORTAL_ID_HERE"  # Your low-priv portal ID

# Cookies from browser (F12 → Network → any request → Copy as cURL)
COOKIE_HEADER = """
PASTE_YOUR_COOKIES_HERE
""".strip()

# ============================================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================================

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = f"https://app-{HUBLET}.hubspot.com"
chirp_base = "/api/chirp-frontend-app/v1/gateway"

def test_chirp(service, method, test_name, payload=None):
    """Test CHIRP RPC endpoint"""
    # Build URL
    path = f"{chirp_base}/{service}/{method}"
    params = f"?hs_static_app=setup-guide-ui&hs_static_app_version=1.50381&portalId={PORTAL_ID}&clienttimeout=5000"
    full_url = f"{base_url}{path}{params}"

    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"Service: ...{service.split('.')[-1]}")
    print(f"Method: {method}")
    print('='*70)

    # Build request
    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0')
    req.add_header('Origin', base_url)
    req.add_header('Referer', f'{base_url}/contacts/{PORTAL_ID}/objects/0-1/views/all/list')

    # Request body
    data = json.dumps(payload if payload else {}).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
        status = response.status
        content = response.read().decode('utf-8')

        print(f"✓ Status: {status}")

        try:
            json_resp = json.loads(content)
            print(f"✓ JSON Response:")
            print(json.dumps(json_resp, indent=2)[:400])

            if status == 200:
                print(f"\n✓✓✓ CHIRP ENDPOINT WORKING")
                return True, status, json_resp

        except json.JSONDecodeError:
            print(f"✓ Response (not JSON): {content[:200]}")

        return True, status, content

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")

        try:
            error_content = e.read().decode('utf-8')
            error_json = json.loads(error_content)

            print(f"  Error Response:")
            print(f"    {json.dumps(error_json, indent=4)[:400]}")

            # Check for CHIRP-specific error fields
            error_str = json.dumps(error_json)
            if any(keyword in error_str for keyword in ['serviceName', 'methodName', 'chirp', 'rpc']):
                print(f"\n  ✓ CHIRP framework detected in error response")
                print(f"  → This confirms CHIRP RPC is active")

            if e.code == 400:
                print(f"\n  → Bad Request - Invalid payload or parameters")
                print(f"  → Service/method exists but needs correct payload")
            elif e.code == 401:
                print(f"\n  → Unauthorized - Cookies expired, recapture from browser")
            elif e.code == 403:
                print(f"\n  → Forbidden - Service exists but permission denied")
                print(f"  → Low-privileged user lacks access to this service")
            elif e.code == 404:
                print(f"\n  → Not Found - Service/method doesn't exist")
            elif e.code == 500:
                print(f"\n  → Internal Server Error - May leak service info in error")

            return False, e.code, error_json

        except Exception:
            pass

        return False, e.code, None

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False, None, None

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("CHIRP RPC FRAMEWORK TESTING")
    print("="*70)
    print(f"Portal ID: {PORTAL_ID}")
    print(f"Hublet: {HUBLET}")
    print(f"Cookie length: {len(COOKIE_HEADER)} chars")

    # ========================================================================
    # TEST 1: KNOWN CHIRP SERVICE (from method_endpoints.md)
    # ========================================================================
    print(f"\n{'#'*70}")
    print(f"# PHASE 1: KNOWN CHIRP ENDPOINT")
    print(f"{'#'*70}")
    print(f"Testing service discovered in method_endpoints.md")

    test_chirp(
        "com.hubspot.growth.post.purchases.rpc.server.GrowthPostPurchasesChirpService",
        "validatePortalForGrowthProPlusExposure",
        "Known CHIRP Service (Validated)"
    )

    # ========================================================================
    # TEST 2: CHIRP SERVICE ENUMERATION
    # ========================================================================
    print(f"\n{'#'*70}")
    print(f"# PHASE 2: SERVICE ENUMERATION")
    print(f"{'#'*70}")
    print(f"Objective: Discover other CHIRP services accessible to low-priv user")

    # Common service patterns based on CRM objects
    services_to_test = [
        ("com.hubspot.contacts.rpc.server.ContactsChirpService", "get"),
        ("com.hubspot.contacts.rpc.server.ContactsChirpService", "search"),
        ("com.hubspot.contacts.rpc.server.ContactsChirpService", "getById"),
        ("com.hubspot.companies.rpc.server.CompaniesChirpService", "get"),
        ("com.hubspot.companies.rpc.server.CompaniesChirpService", "search"),
        ("com.hubspot.deals.rpc.server.DealsChirpService", "get"),
        ("com.hubspot.deals.rpc.server.DealsChirpService", "search"),
        ("com.hubspot.users.rpc.server.UsersChirpService", "getCurrentUser"),
        ("com.hubspot.users.rpc.server.UsersChirpService", "getById"),
        ("com.hubspot.auth.rpc.server.AuthChirpService", "validate"),
        ("com.hubspot.auth.rpc.server.AuthChirpService", "check"),
        ("com.hubspot.portal.rpc.server.PortalChirpService", "getById"),
        ("com.hubspot.portal.rpc.server.PortalChirpService", "get"),
    ]

    results = []

    for service, method in services_to_test:
        success, code, response = test_chirp(
            service,
            method,
            f"Test: {service.split('.')[-1]}/{method}"
        )

        results.append({
            'service': service,
            'method': method,
            'service_name': service.split('.')[-1],
            'success': success,
            'code': code
        })

    # ========================================================================
    # RESULTS SUMMARY
    # ========================================================================
    print(f"\n{'='*70}")
    print("CHIRP TESTING SUMMARY")
    print('='*70)

    successful = [r for r in results if r['success']]
    errors_400 = [r for r in results if r['code'] == 400]
    errors_403 = [r for r in results if r['code'] == 403]
    errors_404 = [r for r in results if r['code'] == 404]
    errors_500 = [r for r in results if r['code'] == 500]

    print(f"\n[SERVICE ENUMERATION RESULTS]")
    print(f"  Total services tested: {len(results)}")
    print(f"  Successful (200): {len(successful)}")
    print(f"  Bad Request (400): {len(errors_400)}")
    print(f"  Forbidden (403): {len(errors_403)}")
    print(f"  Not Found (404): {len(errors_404)}")
    print(f"  Server Error (500): {len(errors_500)}")

    if successful:
        print(f"\n✓ WORKING CHIRP SERVICES (Accessible to low-priv user):")
        for r in successful:
            print(f"  → {r['service_name']}/{r['method']}")
        print(f"\n  IMPACT: Low-privileged user can access internal services")

    if errors_400:
        print(f"\n⚠️ Services exist but require correct payload (400):")
        for r in errors_400[:5]:
            print(f"  → {r['service_name']}/{r['method']}")
        print(f"  → These services exist and are accessible")
        print(f"  → Need to reverse engineer correct payload from browser requests")

    if errors_403:
        print(f"\n⚠️ Services exist but are forbidden (403):")
        for r in errors_403[:5]:
            print(f"  → {r['service_name']}/{r['method']}")
        print(f"  → Low-privileged user lacks permission")
        print(f"  → Good enumeration: 403 vs 404 reveals valid services")

    if errors_500:
        print(f"\n⚠️ Services exist but have server errors (500):")
        for r in errors_500[:5]:
            print(f"  → {r['service_name']}/{r['method']}")
        print(f"  → May leak information in error messages")

    # ========================================================================
    # FINAL ASSESSMENT
    # ========================================================================
    print(f"\n{'='*70}")
    print("FINAL ASSESSMENT")
    print('='*70)

    print(f"\n[CHIRP FRAMEWORK STATUS]")
    if any([successful, errors_400, errors_403, errors_500]):
        print(f"  ✓✓✓ CHIRP RPC FRAMEWORK CONFIRMED")
        print(f"  ✓ Gateway endpoint accessible: {chirp_base}")
        print(f"  ✓ Services responding to requests")
        print(f"  ✓ Framework is active in production")

        print(f"\n[FINDINGS]")
        findings = []

        if successful:
            findings.append(f"  1. {len(successful)} services fully accessible to low-priv user")

        if errors_400:
            findings.append(f"  2. {len(errors_400)} services exist but need correct payload")
            findings.append(f"     → Can enumerate via 400 vs 404 error codes")

        if errors_403:
            findings.append(f"  3. {len(errors_403)} services exist but forbidden")
            findings.append(f"     → Permission-based access control working")
            findings.append(f"     → Service enumeration possible (403 = exists)")

        if errors_500:
            findings.append(f"  4. {len(errors_500)} services cause server errors")
            findings.append(f"     → Potential information leakage in error messages")

        for finding in findings:
            print(finding)

        print(f"\n[SECURITY IMPLICATIONS]")
        print(f"  → Internal microservices exposed to frontend")
        print(f"  → Service/method enumeration possible via error codes:")
        print(f"    • 404 = Service doesn't exist")
        print(f"    • 400 = Service exists but invalid payload")
        print(f"    • 403 = Service exists but forbidden")
        print(f"    • 500 = Service exists but has error")
        print(f"  → Error responses may leak:")
        print(f"    • Valid service names")
        print(f"    • Required parameters")
        print(f"    • Internal method names")

        if successful or errors_400:
            print(f"\n[EXPLOITATION POTENTIAL]")
            print(f"  → Services accessible to low-privileged user")
            print(f"  → Test for IDOR by changing portalId in URL")
            print(f"  → Reverse engineer payloads from browser Network tab")
            print(f"  → Test business logic vulnerabilities in accessible methods")

    else:
        print(f"  ? CHIRP framework status unclear")
        print(f"  → All services returned 404")
        print(f"  → Possible reasons:")
        print(f"    1. Different service naming convention")
        print(f"    2. CHIRP disabled/restricted for this hublet")
        print(f"    3. Cookies expired (recapture from browser)")

    print(f"\n[NEXT STEPS]")
    if successful or errors_400:
        print(f"  1. Capture working CHIRP requests from browser Network tab")
        print(f"  2. Extract exact payload format for successful services")
        print(f"  3. Test IDOR by changing portalId parameter")
        print(f"  4. Test business logic in accessible methods")
        print(f"  5. Document findings for bug bounty report")
    else:
        print(f"  1. Verify cookies are fresh (recapture from browser)")
        print(f"  2. Check browser Network tab for actual CHIRP requests")
        print(f"  3. Copy exact service/method names from live traffic")
        print(f"  4. Update services_to_test list with real service names")

    print(f"\n{'='*70}")
    print("TESTING COMPLETE")
    print('='*70)
