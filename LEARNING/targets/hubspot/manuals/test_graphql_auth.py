import sys
import urllib.request
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

def test_graphql(url, query_name, query):
    """Test GraphQL endpoint with authentication"""
    print(f"\n[TEST] {query_name}")
    print(f"Endpoint: {url}")
    
    req = urllib.request.Request(url, method='POST')
    req.add_header('Cookie', cookie_header)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    
    data = json.dumps({"query": query}).encode('utf-8')
    
    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=10)
        status = response.status
        content = response.read().decode('utf-8', errors='ignore')
        
        print(f"✓ Status: {status}")
        
        # Try to parse as JSON
        try:
            json_response = json.loads(content)
            print(f"✓ Response Type: JSON")
            
            if 'data' in json_response:
                print(f"✓ GRAPHQL SUCCESS - Has 'data' field")
                print(f"  Data: {json.dumps(json_response['data'], indent=2)[:200]}...")
                return True
            elif 'errors' in json_response:
                print(f"✓ GRAPHQL RESPONDED - Has 'errors' field")
                print(f"  Errors: {json_response['errors']}")
                return True
            else:
                print(f"? Unexpected JSON structure: {list(json_response.keys())}")
                return False
        except json.JSONDecodeError:
            print(f"✗ Response is not JSON")
            print(f"  Content preview: {content[:200]}...")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")
        if e.code == 405:
            print(f"  → Method Not Allowed (POST blocked)")
        elif e.code == 401:
            print(f"  → Unauthorized (auth issue)")
        elif e.code == 403:
            print(f"  → Forbidden (insufficient permissions)")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

print("="*70)
print("TRACK A: GRAPHQL ENDPOINT TESTING (AUTHENTICATED)")
print("="*70)

# Test endpoints
endpoints = [
    "https://app.hubspot.com/graphql",
    "https://api.hubspot.com/graphql",
    "https://app.hubspot.com/api/graphql",
]

# Test queries
queries = {
    "Basic typename": "{ __typename }",
    "Introspection": """
    {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
      }
    }
    """,
}

results = {}

for endpoint in endpoints:
    print(f"\n{'='*70}")
    print(f"TESTING: {endpoint}")
    print('='*70)
    
    endpoint_results = []
    
    for query_name, query in queries.items():
        result = test_graphql(endpoint, query_name, query)
        endpoint_results.append(result)
        
        # If basic query fails, no point testing introspection
        if query_name == "Basic typename" and not result:
            print(f"\n→ Skipping introspection test (basic query failed)")
            break
    
    results[endpoint] = any(endpoint_results)

print(f"\n{'='*70}")
print("SUMMARY")
print('='*70)

working_endpoints = [ep for ep, worked in results.items() if worked]
if working_endpoints:
    print(f"\n✓ WORKING GRAPHQL ENDPOINTS:")
    for ep in working_endpoints:
        print(f"  - {ep}")
    print(f"\n✓ GraphQL infrastructure CONFIRMED")
    print(f"✓ Next: Run full schema introspection query")
else:
    print(f"\n✗ NO WORKING GRAPHQL ENDPOINTS FOUND")
    print(f"  All tested endpoints returned errors or non-GraphQL responses")
    print(f"  → GraphQL may use different path or require additional headers")

