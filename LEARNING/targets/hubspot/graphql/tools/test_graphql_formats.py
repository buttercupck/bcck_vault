import sys
import urllib.request
import ssl
import json
import re

# Create unverified SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read headers.md
headers_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/graphql/headers.md'

print("="*70)
print("TRACK A: TESTING DIFFERENT GRAPHQL BODY FORMATS")
print("="*70)

with open(headers_file, 'r') as f:
    content = f.read()

# Extract components (same as before)
url_match = re.search(r'POST ([^\s]+) HTTP', content)
path_with_params = url_match.group(1)

host_match = re.search(r'Host: ([^\n]+)', content)
host = host_match.group(1).strip()

csrf_match = re.search(r'X-HubSpot-CSRF-hubspotapi: ([^\n]+)', content)
csrf_token = csrf_match.group(1).strip() if csrf_match else None

cookie_match = re.search(r'Cookie: ([^\n]+)', content)
cookie_header = cookie_match.group(1).strip()

full_url = f"https://{host}{path_with_params}"

print(f"\n[SETUP]")
print(f"URL: {full_url}")
print(f"CSRF: {'✓' if csrf_token else '✗'}")
print(f"Cookie: {len(cookie_header)} chars")

def test_format(format_name, body_data):
    """Test different body formats"""

    print(f"\n{'='*70}")
    print(f"TEST: {format_name}")
    print('='*70)

    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', cookie_header)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0')
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', f'https://{host}')

    if csrf_token:
        req.add_header('X-HubSpot-CSRF-hubspotapi', csrf_token)

    data = json.dumps(body_data).encode('utf-8')
    print(f"Body format: {json.dumps(body_data, indent=2)[:200]}...")
    print(f"Body length: {len(data)} bytes")

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=15)
        status = response.status
        response_content = response.read().decode('utf-8', errors='ignore')

        print(f"✓ Status: {status}")
        print(f"✓ Content: {len(response_content)} bytes")

        try:
            json_response = json.loads(response_content)
            print(f"✓ JSON Response")

            # Check for GraphQL success
            if isinstance(json_response, list):
                if len(json_response) > 0 and 'data' in json_response[0]:
                    print(f"✓✓✓ SUCCESS - GraphQL data received")
                    print(f"  Keys: {list(json_response[0]['data'].keys())}")
                    return True, json_response
                elif len(json_response) > 0 and 'errors' in json_response[0]:
                    print(f"✓ GraphQL errors: {json_response[0]['errors']}")
                    return False, json_response
            elif isinstance(json_response, dict):
                if 'data' in json_response:
                    print(f"✓✓✓ SUCCESS - GraphQL data received")
                    print(f"  Keys: {list(json_response['data'].keys())}")
                    return True, json_response
                elif 'errors' in json_response:
                    print(f"✓ GraphQL errors: {json_response['errors']}")
                    return False, json_response

            print(f"? Unexpected format: {json.dumps(json_response, indent=2)[:300]}")
            return False, json_response

        except json.JSONDecodeError:
            print(f"✗ Not JSON: {response_content[:200]}")
            return False, None

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {e.reason}")

        try:
            error_content = e.read().decode('utf-8', errors='ignore')
            error_json = json.loads(error_content)
            print(f"  Error: {json.dumps(error_json, indent=2)}")
        except:
            print(f"  Error content: {error_content[:200] if 'error_content' in locals() else 'N/A'}")

        return False, None

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False, None

# Test different body formats
test_cases = [
    ("Format 1: Simple object (standard GraphQL)", {
        "query": "{ __typename }"
    }),

    ("Format 2: Object with operationName", {
        "operationName": "TypenameQuery",
        "query": "{ __typename }"
    }),

    ("Format 3: Array with object (captured format)", [{
        "operationName": "TypenameQuery",
        "variables": {},
        "query": "{ __typename }"
    }]),

    ("Format 4: Object with variables", {
        "operationName": "TypenameQuery",
        "variables": {},
        "query": "{ __typename }"
    }),

    ("Format 5: Array with query only", [{
        "query": "{ __typename }"
    }]),
]

results = []

for format_name, body in test_cases:
    success, response = test_format(format_name, body)
    results.append({
        'name': format_name,
        'success': success,
        'response': response
    })

    # If successful, stop testing
    if success:
        print(f"\n✓✓✓ WORKING FORMAT FOUND!")
        break

print(f"\n{'='*70}")
print("RESULTS")
print('='*70)

successful = [r for r in results if r['success']]

if successful:
    print(f"\n✓✓✓ WORKING FORMAT:")
    for r in successful:
        print(f"  - {r['name']}")
    print(f"\n✓✓✓ TRACK A GRAPHQL VALIDATED")
else:
    print(f"\n✗ No working format found")
    print(f"\n  Tested formats:")
    for r in results:
        print(f"    - {r['name']}: FAIL")

    print(f"\n  Possible issues:")
    print(f"    - Cookies expired (regenerate from browser)")
    print(f"    - CSRF token expired (regenerate from browser)")
    print(f"    - GraphQL endpoint requires specific query structure")
    print(f"    - Endpoint is session-specific")

print(f"\n{'='*70}")
