import sys
import urllib.request
import urllib.parse
import ssl
import json

# Create unverified SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Parse Netscape cookies
cookie_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/cookies.txt'
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
print("TRACK A: GRAPHQL TESTING WITH DISCOVERED PARAMETERS")
print("="*70)
print(f"\n[INFO] Testing GraphQL with parameters from method_endpoints.md")
print(f"[INFO] Portal ID: 242862774")
print(f"[INFO] Using authenticated session (33 cookies)\n")

def test_graphql(base_url, endpoint, params, query_name, query):
    """Test GraphQL endpoint with parameters"""

    # Build URL with query parameters
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}{endpoint}?{query_string}"

    print(f"\n{'='*70}")
    print(f"TEST: {query_name}")
    print(f"Endpoint: {endpoint}")
    print(f"Parameters: {', '.join([f'{k}={v}' for k, v in params.items()])}")
    print('='*70)

    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', cookie_header)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    data = json.dumps({"query": query}).encode('utf-8')

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

            if 'data' in json_response:
                print(f"✓✓✓ GRAPHQL SUCCESS - Has 'data' field")
                print(f"  Data keys: {list(json_response.get('data', {}).keys())}")
                print(f"  Full data: {json.dumps(json_response['data'], indent=2)[:500]}")
                return True, 'SUCCESS'
            elif 'errors' in json_response:
                print(f"✓ GRAPHQL RESPONDED - Has 'errors' field")
                errors = json_response['errors']
                print(f"  Error count: {len(errors)}")
                if errors:
                    print(f"  First error: {errors[0]}")
                return True, 'ERROR_RESPONSE'
            else:
                print(f"? Unexpected JSON structure: {list(json_response.keys())}")
                print(f"  Content preview: {content[:200]}")
                return False, 'UNEXPECTED_JSON'
        except json.JSONDecodeError:
            print(f"✗ Response is not JSON")
            print(f"  Content preview: {content[:200]}")
            return False, 'NOT_JSON'

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")
        if e.code == 405:
            print(f"  → Method Not Allowed (POST blocked)")
            return False, 'METHOD_NOT_ALLOWED'
        elif e.code == 401:
            print(f"  → Unauthorized (auth issue)")
            return False, 'UNAUTHORIZED'
        elif e.code == 403:
            print(f"  → Forbidden (insufficient permissions)")
            return False, 'FORBIDDEN'
        elif e.code == 404:
            print(f"  → Not Found (endpoint doesn't exist)")
            return False, 'NOT_FOUND'
        return False, f'HTTP_{e.code}'
    except Exception as e:
        print(f"✗ Error: {e}")
        return False, 'EXCEPTION'

# Base URL
base_url = 'https://app.hubspot.com'

# Endpoints to test (from method_endpoints.md analysis)
endpoints = [
    '/graphql',
    '/api/graphql',
    '/api/graphql/v1',
]

# Parameter sets to test (from method_endpoints.md patterns)
param_sets = [
    {
        'name': 'Apollo Client Pattern',
        'params': {
            'portalId': '242862774',
            'hs_static_app': 'apollo-client',
            'hs_static_app_version': '3.43',
            'clienttimeout': '10000',
        }
    },
    {
        'name': 'CRM Index UI Pattern',
        'params': {
            'portalId': '242862774',
            'hs_static_app': 'crm-index-ui',
            'hs_static_app_version': '2.46863',
            'clienttimeout': '14000',
        }
    },
    {
        'name': 'Setup Guide UI Pattern',
        'params': {
            'portalId': '242862774',
            'hs_static_app': 'setup-guide-ui',
            'hs_static_app_version': '1.50381',
            'clienttimeout': '5000',
        }
    },
    {
        'name': 'GraphQL Client Pattern',
        'params': {
            'portalId': '242862774',
            'hs_static_app': 'graphql-client',
            'hs_static_app_version': '1.0',
            'clienttimeout': '10000',
        }
    },
    {
        'name': 'Minimal (Portal ID Only)',
        'params': {
            'portalId': '242862774',
        }
    },
]

# Test queries
queries = {
    "Basic typename": "{ __typename }",
    "Introspection (Schema)": """{
      __schema {
        queryType { name }
        mutationType { name }
      }
    }""",
}

results = {}

# Test each endpoint with each parameter set
for endpoint in endpoints:
    print(f"\n{'#'*70}")
    print(f"# TESTING ENDPOINT: {endpoint}")
    print(f"{'#'*70}")

    endpoint_results = []

    for param_set in param_sets:
        param_name = param_set['name']
        params = param_set['params']

        print(f"\n[PARAM SET] {param_name}")

        for query_name, query in queries.items():
            success, result_type = test_graphql(
                base_url, endpoint, params,
                f"{param_name} - {query_name}",
                query
            )
            endpoint_results.append({
                'endpoint': endpoint,
                'params': param_name,
                'query': query_name,
                'success': success,
                'type': result_type,
            })

            # If successful, no need to test more queries with this param set
            if success and result_type == 'SUCCESS':
                print(f"\n✓✓✓ FOUND WORKING CONFIGURATION!")
                print(f"    Endpoint: {endpoint}")
                print(f"    Params: {param_name}")
                break

        # If we found a working config, no need to test more param sets
        if endpoint_results and endpoint_results[-1]['success'] and endpoint_results[-1]['type'] == 'SUCCESS':
            break

    results[endpoint] = endpoint_results

print(f"\n{'='*70}")
print("SUMMARY")
print('='*70)

# Analyze results
successful_configs = []
error_responses = []
method_not_allowed = []
not_found = []

for endpoint, endpoint_results in results.items():
    for result in endpoint_results:
        if result['success'] and result['type'] == 'SUCCESS':
            successful_configs.append(result)
        elif result['success'] and result['type'] == 'ERROR_RESPONSE':
            error_responses.append(result)
        elif result['type'] == 'METHOD_NOT_ALLOWED':
            method_not_allowed.append(result)
        elif result['type'] == 'NOT_FOUND':
            not_found.append(result)

if successful_configs:
    print(f"\n✓✓✓ WORKING GRAPHQL CONFIGURATIONS FOUND: {len(successful_configs)}")
    for config in successful_configs:
        print(f"  ✓ {config['endpoint']} with {config['params']}")
        print(f"    Query: {config['query']}")
    print(f"\n✓✓✓ TRACK A COMPLETE - GraphQL infrastructure VALIDATED")
    print(f"✓✓✓ Next: Run full schema introspection")
elif error_responses:
    print(f"\n✓ GRAPHQL RESPONDING (with errors): {len(error_responses)}")
    for config in error_responses:
        print(f"  ✓ {config['endpoint']} with {config['params']}")
    print(f"\n→ GraphQL exists but queries have errors")
    print(f"→ Check error messages for authentication or permission issues")
else:
    print(f"\n✗ NO WORKING GRAPHQL CONFIGURATIONS FOUND")
    print(f"\n  Method Not Allowed (405): {len(method_not_allowed)} tests")
    print(f"  Not Found (404): {len(not_found)} tests")

    if method_not_allowed:
        print(f"\n→ Endpoints that exist but block POST:")
        for config in method_not_allowed[:3]:
            print(f"    - {config['endpoint']} ({config['params']})")

    if not_found:
        print(f"\n→ Endpoints that don't exist:")
        for config in not_found[:3]:
            print(f"    - {config['endpoint']} ({config['params']})")

    print(f"\n→ GraphQL may require:")
    print(f"    - Browser-based testing (CSRF tokens)")
    print(f"    - Different HTTP methods (GET, OPTIONS)")
    print(f"    - Additional headers from source map analysis")

print(f"\n{'='*70}")
